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
	int edges, vertices;
	cout << "Insertar numero aristas y numero vertices. Ej: 3 4" << endl;
	cin >> edges >> vertices;
	cout << "Insertar vertices. Ej: 1 2" << endl;

	vvi adj(edges+1);
	for(int i=0; i<vertices; i++){
		int a, b;
		cin >> a >> b;
		adj[a].push_back(b);
	}

	vector<int> sol = AproxVertexCover(adj);

	for(int v: sol) cout << v << ' ';
	cout << endl;

	return 0;
}