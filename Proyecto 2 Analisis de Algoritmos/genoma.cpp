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
		vector<vector<int>> tabla;
		int k, rep, cota;
		int a, b, m, ai, bi, mi, p;
		int h(int kmerc);
		int hi(int kmerc);
		int nextPrime(int n);
		int codificar(string kmer);
		int procesarkmers(string &genoma, unordered_set<int> &setKmers);
		void crearTabla(unordered_set<int> &setKmers);

	public:
		HashPerfecto(string &genoma);
		bool search(string kmer);
		int repeticiones();
		int memoria();
};

HashPerfecto::HashPerfecto(string &genoma){
	k = 15;
	if(genoma.size() < k) throw invalid_argument("Genoma de largo insuficiente");

	unordered_set<int> setKmers;
	m = procesarkmers(genoma, setKmers);
	p = nextPrime(10*m);

	rep = 1;
	cota = 4*m;
	crearTabla(setKmers);
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

int HashPerfecto::procesarkmers(string &genoma, unordered_set<int> &setKmers){
	for(int i=0; i<genoma.size()-(k-1); i++)
		setKmers.insert( codificar( genoma.substr(i, k) ) );
	return setKmers.size();
}

void HashPerfecto::crearTabla(unordered_set<int> &setKmers){
	minstd_rand rng(time(NULL));

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

int HashPerfecto::memoria(){
	int mem = 0;
	mem += sizeof(HashPerfecto);
	mem += sizeof(int)*10;
	mem += sizeof(vector<vector<int>>);
	for(vector<int> v: tabla) mem += sizeof(vector<int>) + sizeof(int)*v.capacity();
	return mem;
};

int stats(){
	int iter = 15, rep = 10, ts = 100, busq = 10000;
	minstd_rand rng(time(NULL));

	vector<int> repeticiones(iter), memoria(iter), tCrearTabla(iter), tBusqueda(iter), tam(iter);

	for(int i=0; i<iter; i++){
		for(int j=0; j<rep; j++){	

			string s;
			tam[i] = ts*(i+1);
			for(int k=0; k<ts*(i+1); k++){
				int r = rng()%4;
				if(r == 0) s += 'A';
				if(r == 1) s += 'C';
				if(r == 2) s += 'T';
				if(r == 3) s += 'G';
			}
			auto start = high_resolution_clock::now();
			HashPerfecto h = HashPerfecto(s);
			auto finish = high_resolution_clock::now();
			tCrearTabla[i] += duration_cast<microseconds> (finish - start).count();

			string b;
			for(int k=0; k<15; k++){
				for(int m=0; m<15; m++){
					int r = rng()%4;
					if(r == 0) b += 'A';
					if(r == 1) b += 'C';
					if(r == 2) b += 'T';
					if(r == 3) b += 'G';
				}
			}
			start = high_resolution_clock::now();
			for(int k=0; k<busq; k++) h.search(b);
			finish = high_resolution_clock::now();
			tBusqueda[i] += duration_cast<nanoseconds> (finish - start).count();

			repeticiones[i] += h.repeticiones();
			memoria[i] += h.memoria();
		}
	}
	cout << endl << "Tam" << endl;
	for(auto a: tam) cout << a << endl;

	cout << endl << "Rep" << endl;
	for(auto a: repeticiones) cout << (float)a / rep << endl;

	cout << endl << "Mem" << endl;
	for(auto a: memoria) cout << (float)a / rep << endl;

	cout << endl << "T crear" << endl;
	for(auto a: tCrearTabla) cout << (float)a / rep << endl;

	cout << endl << "T busqueda" << endl;
	for(auto a: tBusqueda) cout << (float)a / (rep*busq) << endl;
}

int main(){
	cout << "1: Ingreso de archivo" << endl;
	cout << "2: Ingreso manual de string" << endl;
	int n;
	cin >> n;
	cout << endl;

	string genoma;
	if(n == 1){
		string nombre;
		string polynesia = "GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna";
		cout << "1: " << polynesia << endl;
		cout << "2: t.txt" << endl;
		cout << "Ingresar numero o nombre del archivo: ";
		cin >> nombre;

		if(nombre == "1") nombre = polynesia;
		if(nombre == "2") nombre = "t.txt";

		ifstream archivo(nombre);
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

	}else{
		cout << "Ingresar string" << endl;
		cin >> genoma;
	}

	HashPerfecto h = HashPerfecto(genoma);
	
	cout << endl << "Ingresar 15-mer a buscar, 0 para salir" << endl;
	while(true){
		string kmer;
		cin >> kmer;
		if(kmer == "0") break;
		if(h.search(kmer)) cout << "Presente en el genoma" << endl;
		else cout << "No presente en el genoma" << endl;
	}

	return 0;
}