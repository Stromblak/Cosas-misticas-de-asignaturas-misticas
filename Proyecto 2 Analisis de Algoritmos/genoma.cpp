#include <bits/stdc++.h>
using namespace std;
typedef unsigned int uint;

/*
	El archivo .fna se puede colocar como input
	por alguna razon en powershell no pesca el '<', encontre esta solucion
	cmd /c ".\a.exe < GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna"
	no se si conoces alguna mejor

	parece que cuando el p es muy alto deja de funcionar el hashing 

	usar el genoma como input no tengo idea si termina o no el programa
*/ 

class HashPerfecto{
	private:
		string genoma;
		set<int> setKmers;
		multiset<int> multisetKmers;
		vector<vector<int>> tabla;
		int p, k, rep4, rep2;
		int a, b, m, ai, bi, mi;
		int kmerToInt(string kmer);
		int h(int knum);
		int hi(int knum);
		int random();
		void crearTabla();

	public:
		HashPerfecto(string gen);
		int search(string kmer);
		void repeticiones();
};

HashPerfecto::HashPerfecto(string gen){
	srand( time(NULL) );
	rand();
	genoma = gen;
	p = 100003;
	k = 15;
	rep4 = 1;
	rep2 = 1;

	for(int i=0; i<genoma.size()-(k-1); i++){
		int knum = kmerToInt( genoma.substr(i, k) );
		setKmers.insert(knum);
		multisetKmers.insert(knum);
	}
	m = setKmers.size();
	
	crearTabla();
	multisetKmers.clear();
	setKmers.clear();
}

int HashPerfecto::kmerToInt(string kmer){
	uint knum = 0;

	for(int i=0; i<kmer.size(); i++){
		int base;
		if(kmer[i] == 'A') base = 0;
		else if(kmer[i] == 'C') base = 1;
		else if(kmer[i] == 'T') base = 2;
		else if(kmer[i] == 'G') base = 3;

		knum += base << i*2;
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
		for(int knum: setKmers) tablaAux[h(knum)].push_back(knum);
		for(auto a: tablaAux) sum += a.size()*a.size();
		
		if(sum < 4*m) break;
		else rep4++;
	}

	for(int i=0; i<m; i++){
		int col = tablaAux[i].size();
		while(col){
			ai = random()%p;
			bi = random()%p;
			mi = col*col;
			tabla[i] = vector<int>(3 + mi);

			int flag = 0;
			for(int knum: tablaAux[i]){
				if( tabla[i][ 3+hi(knum) ] ) flag = 1;
				else tabla[i][ 3+hi(knum) ] = multisetKmers.count(knum);
			}

			if(!flag){
				tabla[i][0] = mi;
				tabla[i][1] = ai;
				tabla[i][2] = bi;
				break;
			}
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
	int ac = a, bc = b;
	while(true){
		int sum = 0;
		a = random()%p, b = random()%p;	
		int tablaCol[m] = {0};

		for(int i: setKmers) tablaCol[ h(i) ]++;
		for(int i: tablaCol) sum += i*i;

		if(sum < 2*m){
			a = ac;
			b = bc;
			break;
		}
		else rep2++;
	}
	cout << "Repeticiones 4n: " << rep4 << endl;
	cout << "Repeticiones 2n: " << rep2 << endl;
}

int main(){
	string genoma, saux;

	int flag = 0;
	while(cin >> saux && !saux.empty()){
		if(saux[0] == '>') flag = 1;
		if(!flag) genoma += saux;
		if(saux == "sequence") flag = 0;
	}

	HashPerfecto h = HashPerfecto(genoma);


	cout << h.search("GGGGGGGGGGGGGGG") << endl;


	h.repeticiones();




	cout << "fin" << endl;
	return 0;
}


