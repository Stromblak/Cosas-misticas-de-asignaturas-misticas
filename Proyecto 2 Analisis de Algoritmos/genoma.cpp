#include <iostream>
#include <vector>
#include <unordered_set>
#include <chrono>
#include <fstream>  
#include <random>

using namespace std;
using namespace chrono;

class HashPerfecto{
	private:
		minstd_rand rng;
		string genoma;
		unordered_set<int> setKmers;
		vector<vector<int>> tabla;
		int k, rep, cota;
		int a, b, m, ai, bi, mi, p;
		int h(int kmerc);
		int hi(int kmerc);
		int nextPrime(int n);
		int codificar(string kmer);
		int procesarkmers();
		void crearTabla();

	public:
		HashPerfecto(string gen);
		bool search(string kmer);
		int repeticiones();
};

HashPerfecto::HashPerfecto(string gen){
	rng.seed(time(NULL));
	k = 15;

	if(gen.size() < k) throw invalid_argument("Genoma de largo insuficiente");

	genoma = gen;
	m = procesarkmers();
	p = nextPrime(10*m);

	rep = 1;
	cota = 4*m;
	crearTabla();

	genoma.clear();
	setKmers.clear();
}

int HashPerfecto::h(int kmerc){
	return abs( ((a*kmerc + b)%p )%m );
}

int HashPerfecto::hi(int kmerc){
	return abs( ((ai*kmerc + bi)%p )%mi );
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
		setKmers.insert( codificar( genoma.substr(i, k) ) );
	return setKmers.size();
}

void HashPerfecto::crearTabla(){
	while(true){
		int c = 0;
		a = rng()%p;
		b = rng()%p;	
		vector<vector<int>> tabla1(m);
		for(int kmer: setKmers) tabla1[ h(kmer) ].push_back(kmer);
		for(vector<int> v: tabla1) c += v.size()*v.size();
		if(c < cota){
			tabla = tabla1;
			break;
		}else rep++;
	}

	for(int i=0; i<m; i++){
		mi = tabla[i].size() * tabla[i].size();

		int count = 0;
		while(mi){
			bool colision = false;
			ai = rng()%p;
			bi = rng()%p;
			vector<int> tabla2(3 + mi);

			for(int kmer: tabla[i]){
				int pos = 3 + hi(kmer);
				if(tabla2[pos] == 0) tabla2[pos] = kmer;
				else{
					colision = true;
					break;
				}
			}

			if(colision == false){
				tabla2[0] = mi;
				tabla2[1] = ai;
				tabla2[2] = bi;
				tabla[i] = tabla2;
				break;
			}
			//-------------
			count++;
			if(count > 1000000){

				cout << endl;
				cout << "Fallo Tabla 2" << endl;
				cout << "p " << p << endl;
				cout << "ai "<< ai << endl;
				cout << "bi "<< bi << endl;
				cout << "mi "<< mi << endl;

				cout << "kmers codificados" << endl;
				for(auto a: tabla[i]) cout << a << endl;
				cout << endl;
				return;
			}
		}
	}
}

bool HashPerfecto::search(string kmer){
	if(kmer.size() != k) return false;

	int kmerc = codificar(kmer);
	int pos1 = h(kmerc);

	if(tabla[pos1].empty()) return false;

	mi = tabla[pos1][0];
	ai = tabla[pos1][1];
	bi = tabla[pos1][2];

	int kmerTabla = tabla[pos1][3 + hi(kmerc)];
	if(kmerTabla == kmerc) return true;
	else return false;
}

int HashPerfecto::repeticiones(){
	return rep;
}

int main(){

	int n = 50, ts = 150;
	minstd_rand rng(time(NULL));

	for(int i=0; i<n; i++){
		string s;
		for(int j=0; j<ts; j++){
			int r = rng()%4;
			if(r == 0) s += 'A';
			if(r == 1) s += 'C';
			if(r == 2) s += 'T';
			if(r == 3) s += 'G';
		}

		HashPerfecto h = HashPerfecto(s);
		printf("Repeticiones %d: %d \n", i+1, h.repeticiones());
	}
}

int main2(){
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
	HashPerfecto h = HashPerfecto(genoma);

	cout << "Repeticiones: " << h.repeticiones() << endl;

	string kmer;
	cout << "Ingresar 15-mer a buscar, 0 para salir" << endl;
	while(true){
		cin >> kmer;
		if(kmer == "0") break;
		cout << "Existe: " << h.search(kmer) << endl;
	}

	cout << "Fin main()" << endl;
	return 0;
}