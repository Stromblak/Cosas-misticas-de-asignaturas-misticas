#include <bits/stdc++.h>
using namespace std;
typedef unsigned uint;

/*
	El archivo .fna se puede colocar como input
	por alguna razon en powershell no pesca el '<', encontre esta solucion
	cmd /c ".\a.exe < GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna"
	no se si conoces alguna mejor

	max int = 4294967295, primo anterior = 4294967291
	ante anterior = 4294967279
*/ 

class Hash{
	private:
		string genoma;
		uint p, a, b, m, k;
		int h(string kmer);
		int kmers();
		uint kmerToUint(string kmer);

	public:
		Hash(string gen);
};

Hash::Hash(string gen){
	srand( time(NULL) );
	p = 4294967291;
	a = rand()%p, b = rand()%p, k = 15;
	genoma = gen;

	m = kmers();
}

int Hash::h(string kmer){
	uint knum = kmerToUint(kmer);
	return ( (a*knum + b)%p )%m;
}

uint Hash::kmerToUint(string kmer){
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

int Hash::kmers(){
	priority_queue<int> pq;
	for(int i=0; i<genoma.size() - (k-1); i++) pq.push( kmerToUint( genoma.substr(i, k) ) );

	int kmers = 1, aux = pq.top();
	pq.pop();

	while(!pq.empty()){
		if(aux == pq.top()) pq.pop();
		else{
			aux = pq.top();
			pq.pop();
			kmers++;
		}
	}
	return kmers;
	//	que tan trucho seria usar un set para contar los kmers distintos?
}

int main(){
	string genoma, saux;

	int flag = 0;
	while(cin >> saux && !saux.empty()){
		if(saux[0] == '>') flag = 1;
		if(!flag) genoma += saux;
		if(saux == "sequence") flag = 0;
	}

	Hash h = Hash(genoma);








	cout << "fin" << endl;
	return 0;
}


