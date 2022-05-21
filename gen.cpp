#include <bits/stdc++.h>
using namespace std;


int main(){
	int x, y, z = 0;
	cin >> x >> y;
	while( x > 0){
		cout << x << " " << z << " " << y << endl;
		if (x & 1) z = z + y;	
		x = x>>1;		
		y = y<<1;	
	}	
	
	cout << z << endl;
	
	return 0;
	
}


