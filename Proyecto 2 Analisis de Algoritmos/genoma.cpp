#include <iostream>
#include <vector>
#include <unordered_map>
#include <chrono>
#include <fstream>  
using namespace std;
using namespace chrono;
typedef unsigned int uint;
typedef pair<int, int> ii;
typedef vector<vector<ii>> vvii;

/*
	me salen las repeticiones de busqueda a y b siempre en 1, ni idea si esta bien
	no te parece raro?

	con nextPrime(m) se queda pegado derrepente
*/ 

class HashPerfecto{
	private:
		vvii tabla;
		string genoma;
		unordered_map<int, int> mapkmers;
		int k, rep, cota;
		int a, b, m, ai, bi, mi, p;
		int h(int kmerc);
		int hi(int kmerc);
		int nextPrime(int n);
		int codificar(string kmer);
		int procesarkmers();
		void crearTabla();

	public:
		HashPerfecto(string *gen);
		int count(string kmer);
		int repeticiones();
};

HashPerfecto::HashPerfecto(string *gen){
	srand( time(NULL) );
	rand();
	genoma = *gen;
	k = 15;
	m = procesarkmers();
	p = nextPrime(2*m);
	rep = 1;
	cota = 4*m;
	crearTabla();
	mapkmers.clear();
}

int HashPerfecto::h(int kmerc){
	return ( (uint)(a*kmerc + b)%p )%m;
}

int HashPerfecto::hi(int kmerc){
	return ( (uint)(ai*kmerc + bi)%p )%mi;
}

int HashPerfecto::nextPrime(int n){
	while(true){
		int flag = 1;
		n++;

		if(n <= 1) continue;
		else if(n <= 3) break;
		else if(n%2 == 0 || n%3 == 0) continue;
		else for(int i=5; i*i<=n; i=i+6){
			if(n%i==0 || n%(i+2) == 0){
				flag = 0;
				break;
			}
		}
		if(flag) break;
	}
	return n;
}

int HashPerfecto::codificar(string kmer){
	int kmerc = 0;
	for(int i=0; i<k; i++){
		if(kmer[i] == 'A') kmerc += 0 << i*2;
		else if(kmer[i] == 'C') kmerc += 1 << i*2;
		else if(kmer[i] == 'T') kmerc += 2 << i*2;
		else if(kmer[i] == 'G') kmerc += 3 << i*2;
		else throw invalid_argument("Nucleotido invalido");
	}
	return kmerc;
}

int HashPerfecto::procesarkmers(){
	for(int i=0; i<genoma.size()-(k-1); i++) 
		mapkmers[ codificar( genoma.substr(i, k) ) ]++;
	return mapkmers.size();
}

void HashPerfecto::crearTabla(){
	vvii tablaAux(m);
	tabla = vvii(m);

	while(true){
		int c = 0;
		a = (rand() + rand()<<15)%p;
		b = (rand() + rand()<<15)%p;	
		for(ii kmer: mapkmers) tablaAux[ h(kmer.first) ].push_back(kmer);
		for(auto a: tablaAux) c += a.size()*a.size();
		if(c < cota) break;
		else rep++;
	}

	for(int i=0; i<m; i++){
		int col = tablaAux[i].size(), flag = 0;
		mi = col*col;

		while(col){
			ai = (rand() + rand()<<15)%p;
			bi = (rand() + rand()<<15)%p;
			tabla[i] =  vector<ii>(3 + mi);

			for(ii kmer: tablaAux[i]){
				if( tabla[i][ 3+hi(kmer.first) ].first ){
					flag = 1;
					break;
				}else tabla[i][ 3+hi(kmer.first) ] = kmer;
			}

			if(!flag){
				tabla[i][0] = {mi, 0};
				tabla[i][1] = {ai, 0};
				tabla[i][2] = {bi, 0};
				break;
			}else flag = 0;
		}
	}
}

int HashPerfecto::count(string kmer){
	if(kmer.size() != k) return -1;

	int kmerc = codificar(kmer);
	int pos1 = h(kmerc);

	if(tabla[pos1].empty()) return 0;

	mi = tabla[pos1][0].first;
	ai = tabla[pos1][1].first;
	bi = tabla[pos1][2].first;

	ii parKmer = tabla[pos1][3 + hi(kmerc)];
	if(parKmer.first == kmerc) return parKmer.second;
	else return 0;
}

int HashPerfecto::repeticiones(){
	return rep;
}

int main(){
	string nombre;
	string polynesia = "GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna";

	cout << "1: " << polynesia << endl;
	cout << "2: t.txt" << endl;
	cout << "Ingresar numero o nombre del archivo: ";
	cin >> nombre;

	if(nombre == "1") nombre = polynesia;
	if(nombre == "2") nombre = "t.txt";

	ifstream archivo(nombre);
	string genoma;
	int copiar = 1;
	while(true){
		string data;
		archivo >> data;
		if(data.empty()) break;

		if(data[0] == '>') copiar = 0;
		if(copiar) genoma += data;
		if(data == "sequence") copiar = 1;
	}
	
	archivo.close();
	HashPerfecto h = HashPerfecto(&genoma);

	cout << "Repeticiones: " << h.repeticiones() << endl;


	string kmer;
	cout << "Ingresar 15-mer a buscar, 0 para salir" << endl;
	while(true){
		cin >> kmer;
		if(kmer == "0") break;
		cout << "Cantidad: " << h.count(kmer) << endl;
	}

	cout << "Fin main()" << endl;
	return 0;
}