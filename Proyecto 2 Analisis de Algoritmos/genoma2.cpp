#include <bits/stdc++.h>
using namespace std;
typedef unsigned int uint;


/*
	El archivo .fna se puede colocar como input
	por alguna razon en powershell no pesca el '<', encontre esta solucion
	cmd /c ".\a.exe < GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna"
	no se si conoces alguna mejor

	parece que cuando el p es muy alto deja de funcionar el hashing 

	que tan legal es usar un mapa pa hacer otro hash? xD

	descubri que el cout y printf consume mucho tiempo, de un minuto sin ningun cout a tal vez media hora con el
*/ 

class HashPerfecto{
	private:
		string genoma;
		map<int, int> mapkmers;
		vector<vector<int>> tabla;
		int p, k, rep4, rep2;
		int a, b, m, ai, bi, mi;
		int kmerToInt(string kmer);
		int h(int knum);
		int hi(int knum);
		int random();
		void crearTabla();

	public:
		HashPerfecto(string *gen);
		int search(string kmer);
		void repeticiones();
};

HashPerfecto::HashPerfecto(string *gen){
	srand( time(NULL) );
	rand();
	genoma = *gen;
	p = 7595479;
	k = 15;
	rep4 = 1;
	rep2 = 1;


	cout << "Procesando k-mers" << endl;	//	15 segundos
	for(int i=0; i<genoma.size()-(k-1); i++) mapkmers[ kmerToInt( genoma.substr(i, k) ) ]++;


	m = mapkmers.size();

	cout << "Creando tabla" << endl;	// 23 segundos

	auto start = chrono::high_resolution_clock::now();
	crearTabla();
	auto finish = chrono::high_resolution_clock::now();
	cout << "Segundos: " << chrono::duration_cast<chrono::nanoseconds> (finish - start).count()/1000000000.0 << endl;

	cout << "Tabla creada" << endl;

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

int HashPerfecto::random(){
	return (rand() + rand()<<15);		//	rand tiene de maximo 32k
}

int HashPerfecto::h(int knum){
	return ( (uint)(a*knum + b)%p )%m;
}

int HashPerfecto::hi(int knum){
	return ( (uint)(ai*knum + bi)%p )%mi;
}

void HashPerfecto::crearTabla(){
	vector<vector<int>> tablaAux(m);
	tabla = vector<vector<int>>(m);
	
	while(true){
		int sum = 0;
		a = random()%p;
		b = random()%p;	
		for(auto kmer: mapkmers) tablaAux[ h(kmer.first) ].push_back(kmer.first);
		for(auto a: tablaAux) sum += a.size()*a.size();
		if(sum < 4*m) break;
		else rep4++;
	}

	for(int i=0; i<m; i++){
		int col = tablaAux[i].size(), flag = 0;
		mi = col*col;

		while(col){
			ai = random()%p;
			bi = random()%p;
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

void HashPerfecto::repeticiones(){
	vector<vector<int>> tablaAux(m);
	int ac = a, bc = b;

	while(true){
		int sum = 0;
		a = random()%p;
		b = random()%p;	
		for(auto kmer: mapkmers) tablaAux[ h(kmer.first) ].push_back(kmer.first);
		for(auto a: tablaAux) sum += a.size()*a.size();
		if(sum < 2*m){
			a = ac;
			b = bc;
			break;
		}else rep2++;
	}

	cout << "Repeticiones 4n: " << rep4 << endl;
	cout << "Repeticiones 2n: " << rep2 << endl;
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


	h.repeticiones();


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