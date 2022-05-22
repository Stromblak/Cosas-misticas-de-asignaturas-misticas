#include <iostream>
#include <vector>
#include <map>
#include <chrono>

using namespace std;
using namespace chrono;
typedef unsigned int uint;

/*
	El archivo .fna se puede colocar como input
	por alguna razon en powershell no pesca el '<', encontre esta solucion
	cmd /c ".\a.exe < GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna"
	no se si conoces alguna mejor

	parece que cuando el p es muy alto deja de funcionar el hashing 

	si se busca un kmer que no existe es posible que no devuelva 0, 
	supongo que es naturaleza del hash y no algun bug xD

	me salen las repeticiones de busqueda a y b, casi siempre en 1, ni idea si esta bien
*/ 

class HashPerfecto{
	private:
		string genoma;
		map<int, int> mapkmers;
		vector<vector<int>> tabla;
		int p, k, rep4, rep2, pc;
		int a, b, m, ai, bi, mi;
		int h(int knum);
		int hi(int knum);
		int kmerToInt(string kmer);
		void procesarkmers();
		void crearTabla();
		void porcentaje(int i, int j);
		void tabla2n();

	public:
		HashPerfecto(string *gen);
		int search(string kmer);
};

HashPerfecto::HashPerfecto(string *gen){
	srand( time(NULL) );
	rand();
	genoma = *gen;
	p = 7595479;
	k = 15;
	rep4 = 1;
	rep2 = 1;
	pc = 10;

	procesarkmers();
	crearTabla();
	mapkmers.clear();
	
	cout << "Repeticiones 4n: " << rep4 << endl;
	cout << "Repeticiones 2n: " << rep2 << endl;
}

int HashPerfecto::h(int knum){
	return ( (uint)(a*knum + b)%p )%m;
}

int HashPerfecto::hi(int knum){
	return ( (uint)(ai*knum + bi)%p )%mi;
}

int HashPerfecto::kmerToInt(string kmer){
	int knum = 0;
	for(int i=0; i<k; i++){
		if(kmer[i] == 'A') knum += 0 << i*2;
		else if(kmer[i] == 'C') knum += 1 << i*2;
		else if(kmer[i] == 'T') knum += 2 << i*2;
		else if(kmer[i] == 'G') knum += 3 << i*2;
	}
	return knum;
}

void HashPerfecto::procesarkmers(){
	cout << "Procesando k-mers" << endl;
	auto start = high_resolution_clock::now();

	for(int i=0; i<genoma.size()-(k-1); i++){
		porcentaje(i, genoma.size()-(k-1));
		mapkmers[ kmerToInt( genoma.substr(i, k) ) ]++;
	}
	m = mapkmers.size();

	cout << "Tiempo requerido: " << duration_cast<seconds> (high_resolution_clock::now() - start).count() << "s" << endl << endl;;
}

void HashPerfecto::crearTabla(){
	auto start = chrono::high_resolution_clock::now();

	vector<vector<int>> tablaAux(m);
	tabla = vector<vector<int>>(m);

	cout << "Creando tabla de primer nivel" << endl;
	while(true){
		int sum = 0;
		a = (rand() + rand()<<15)%p;
		b = (rand() + rand()<<15)%p;	
		for(auto kmer: mapkmers) tablaAux[ h(kmer.first) ].push_back(kmer.first);
		for(auto a: tablaAux) sum += a.size()*a.size();
		if(sum < 4*m) break;
		else rep4++;
	}

	cout << "Creando tabla de segundo nivel" << endl;
	for(int i=0; i<m; i++){
		porcentaje(i, m);
		int col = tablaAux[i].size(), flag = 0;
		mi = col*col;

		while(col){
			ai = (rand() + rand()<<15)%p;
			bi = (rand() + rand()<<15)%p;
			tabla[i] = vector<int>(3 + mi);

			for(int knum: tablaAux[i]){
				if( tabla[i][ 3+hi(knum) ] ){
					flag = 1;
					break;
				}else tabla[i][ 3+hi(knum) ] = mapkmers[knum];
			}

			if(!flag){
				tabla[i][0] = mi;
				tabla[i][1] = ai;
				tabla[i][2] = bi;
				break;
			}else flag = 0;
		}  
	}

	cout << "Tiempo requerido: ";
	cout << duration_cast<seconds> (high_resolution_clock::now() - start).count() << "s" << endl << endl;
}

void HashPerfecto::porcentaje(int i, int j){
	if((100.0*i)/j >= pc){
		cout << "[]";
		pc += 10;
	}
	if(i == j-1){
		cout << "[]" << endl;
		pc = 10;
	}
}

void HashPerfecto::tabla2n(){
	vector<vector<int>> tablaAux(m);
	uint ac = a, bc = b;

	while(true){
		int sum = 0;
		a = (rand() + rand()<<15)%p;
		b = (rand() + rand()<<15)%p;
		for(auto kmer: mapkmers) tablaAux[ h(kmer.first) ].push_back(kmer.first);
		for(auto a: tablaAux) sum += a.size()*a.size();
		if(sum < 2*m){
			a = ac;
			b = bc;
			break;
		}else rep2++;
	}
}

int HashPerfecto::search(string kmer){
	int knum = kmerToInt(kmer);
	int pos = h(knum);

	if(tabla[pos].empty()) return 0;

	mi = tabla[pos][0];
	ai = tabla[pos][1];
	bi = tabla[pos][2];

	return tabla[pos][3 + hi(knum)];
}

int main(){
	string genoma, saux;
	int flag = 0;

	cout << "Leyendo genoma" << endl;
	while(cin >> saux && !saux.empty()){
		if(saux[0] == '>') flag = 1;
		if(!flag) genoma += saux;
		if(saux == "sequence") flag = 0;
	}

	HashPerfecto h = HashPerfecto(&genoma);


	cout << h.search("GGGGGGGGGGGGGGG") << endl;

	cout << "Fin main()" << endl;
	return 0;
}

	/*	
	procesar k-mers
	esta opcion me ahorra 3.5 segundos, pero es mas bastante mas larga
	
	string kmer = genoma.substr(0, k);
	mapkmers[ kmerToInt( genoma.substr(0, k) ) ]++;
	int knum = kmerToInt(kmer);

	for(int i=1; i<genoma.size()-(k-1); i++){
		knum = knum >> 2;
		if(genoma[i+k-1] == 'A') knum += 0 << 28;
		else if(genoma[i+k-1] == 'C') knum += 1 << 28;
		else if(genoma[i+k-1] == 'T') knum += 2 << 28;
		else if(genoma[i+k-1] == 'G') knum += 3 << 28;
		mapkmers[knum]++;
	}
	
	*/