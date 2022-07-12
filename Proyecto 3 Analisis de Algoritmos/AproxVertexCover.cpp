#include <bits/stdc++.h>
using namespace std;
typedef vector<vector<int>> vvi;


vector<int> AproxVertexCover(vvi adj){
	vector<int> sol;

	for(int i=0; i<adj.size(); i++){
		if(!adj[i].empty()){
			int u = i, v = adj[i][0];

			adj[u].clear();
			adj[v].clear();
			sol.push_back(u);
			sol.push_back(v);
		}
	}

	return sol;
}


int main(){
	int vertices, aristas;
	cout << "Insertar numero vertices y aristas. Ej: 3 4" << endl;
	cin >> vertices >> aristas;
	cout << "Insertar aristas. Ej: 1 2" << endl;

	vvi adj(vertices+1);
	for(int i=0; i<aristas; i++){
		int a, b;
		cin >> a >> b;
		adj[a].push_back(b);
	}

	vector<int> sol = AproxVertexCover(adj);

	cout << "Solucion aproximada (Vertices): ";
	for(int v: sol) cout << v << ' ';
	cout << endl;

	return 0;
}