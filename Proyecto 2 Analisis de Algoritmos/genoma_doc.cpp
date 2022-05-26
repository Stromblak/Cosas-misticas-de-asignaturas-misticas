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

class HashPerfecto
{
private:
	string genoma;			   // GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna
	map<int, int> mapkmers;	   // map kmer y numero de repeticiones
	vector<vector<int>> tabla; // tabla hash de 2 niveles
	int p, k, rep4, rep2, pc;  // primo, 15, repeticiones 4n, repeticiones 2n
	int a, b, m, ai, bi, mi;
	int h(int knum);			// hash tabla de primer nivel
	int hi(int knum);			// hash tabla de segundo nivel
	int kmerToInt(string kmer); // 15-mer a int
	void procesarkmers();		// crear los kmers a partir del genoma
	void crearTabla();			// hashing a la tabla
	void porcentaje(int i, int j);
	void tabla2n(); // hashing a la tabla, condicion 2n

public:
	HashPerfecto(string *gen); // Constructor
	int search(string kmer);   // buscar la posicion????? del kmer
};

/**
 * @brief Construct a new Hash Perfecto:: Hash Perfecto object
 * Para empezar, primero se deben inicializar todos los valores necesarios.
 * Luego, se deben crear los kmers que seran almacenados mediante hashing a una tabla
 * Finalmente, se hace hash a los kmers y se crea la tabla hash
 * @param gen genoma
 */
HashPerfecto::HashPerfecto(string *gen)
{
	srand(time(NULL));
	rand();
	genoma = *gen;
	p = 7595479; // primo mas despues de .....?
	k = 15;
	rep4 = rep2 = 1;
	pc = 10;

	procesarkmers();
	crearTabla();
	mapkmers.clear();

	cout << "Repeticiones 4n: " << rep4 << endl;
	cout << "Repeticiones 2n: " << rep2 << endl;
}

/**
 * @brief Hashing tabla de primer nivel
 * Usar la siguiente familia de funciones hash universales. Donde
 * p es un numero primo, a y b son valores aleatorios en el rango [0..p − 1],
 * y m el numero de buckets de la tabla.
 * h(k) = ((a × k + b)mod p)mod m)

 * @param knum (int)kmer
 * @return bucket, primer nivel
 */
int HashPerfecto::h(int knum)
{
	return ((uint)(a * knum + b) % p) % m;
}

/**
 * @brief Hashing tabla de segundo nivel
 *
 * @param knum (int)kmer
 * @return bucket, segundo nivel, donde se almacenara el kmer
 */
int HashPerfecto::hi(int knum)
{
	return ((uint)(ai * knum + bi) % p) % mi;
}

/**
 * @brief Transformar el string kmer a int
 *
 * @param kmer kmer en string
 * @return kmer como int
 */
int HashPerfecto::kmerToInt(string kmer)
{
	int knum = 0;
	for (int i = 0; i < k; i++)
	{
		/*
		if (kmer[i] == 'A')
			knum += 0 << i * 2;
		else if (kmer[i] == 'C')
			knum += 1 << i * 2;
		else if (kmer[i] == 'T')
			knum += 2 << i * 2;
		else if (kmer[i] == 'G')
			knum += 3 << i * 2;
		*/
		// le puse un case switch pa que se viera mas bonito, no se si lo queri dejar asi o como antes
		// (no lo he probrado)
		switch (kmer[i])
		{
		case 'A':
			knum += 0 << i * 2;
			break;
		case 'C':
			knum += 1 << i * 2;
			break;
		case 'T':
			knum += 2 << i * 2;
			break;
		case 'G':
			knum += 3 << i * 2;
			break;
		}
	}
	return knum;
}

/**
 * @brief Mapear todos los 15-mers
 * Se elige un pedazo de largo 15 del string genoma para el 15-mer, y luego se transforma a int.
 * Despues, se almacena el 15-mer (int) en un map.
 * Se utiliza la funcion substr(i, k), ya que el 15-mer empiza en la posicion i, tiene un largo k = 15
 */
void HashPerfecto::procesarkmers()
{
	cout << "Procesando k-mers" << endl;
	auto start = high_resolution_clock::now();

	for (int i = 0; i < genoma.size() - (k - 1); i++)
	{
		porcentaje(i, genoma.size() - (k - 1));
		mapkmers[kmerToInt(genoma.substr(i, k))]++;
	}
	m = mapkmers.size();

	cout << "Tiempo requerido: " << duration_cast<seconds>(high_resolution_clock::now() - start).count() << "s" << endl
		 << endl;
	;
}

/**
 * @brief Creacion de las 2 tablas
 * Tabla de primer nivel: Para determinar funcion hash, h, de primer nivel.
 * Elegir m = n, p > |S|, y a y b aleatoriamente en un rango [0..p − 1].
 */
void HashPerfecto::crearTabla()
{
	auto start = chrono::high_resolution_clock::now();

	vector<vector<int>> tablaAux(m); // tabla, primer nivel tamaño m
	tabla = vector<vector<int>>(m);

	cout << "Creando tabla de primer nivel" << endl;
	while (true)
	{
		a = (rand() + rand() << 15) % p; // valor aleatorio entre [0..p − 1]
		b = (rand() + rand() << 15) % p; // valor aleatorio entre [0..p − 1]

		for (auto kmer : mapkmers)
			// hash kmer e insertarlo en una tabla de 2 niveles auxiliar
			tablaAux[h(kmer.first)].push_back(kmer.first);

		// Condicion de sumatoria de i = 0 hasta m-1 de ci^2 < 4n
		int sum = 0;					// sumatoria de i = 0 hasta m-1 de ci^2
		for (auto c : tablaAux)			// 0 hasta m-1
			sum += c.size() * c.size(); // ci^2
		if (sum < 4 * m)				// funcion hash buena
			break;
		else // repetir y aumentar contador
			rep4++;
	}

	cout << "Creando tabla de segundo nivel" << endl;
	for (int i = 0; i < m; i++)
	{
		porcentaje(i, m);
		int c = tablaAux[i].size(), flag = 0;
		mi = c * c; // mi = ci^2

		while (c)
		{
			ai = (rand() + rand() << 15) % p;
			bi = (rand() + rand() << 15) % p;
			tabla[i] = vector<int>(3 + mi); // 3 espacios para almacenar ai, bi, mi

			// recorrer tabla auxiliar de segundo nivel (del bucket i de la tabla de primer niveL)
			// hacer hash a los elementos de esta tabla, a la tabla real
			// el hash de primer nivel se hizo anteriormente, obteniendo i 
			// ahora se debe hacer hash a los elementos en la tabla de segundo nivel
			for (int knum : tablaAux[i]) 
			{	
				// si ya existe un elemento (colision)
				if (tabla[i][3 + hi(knum)])
				{
					flag = 1;
					break;
				}
				else
					tabla[i][3 + hi(knum)] = mapkmers[knum]; // deberiamos almacenar el kmer aqui o no??
					// sgun tengo entendido, se almacena el elemento con el hash
					// para dps usar search() y buscar la posicion de ese elemento
					// asi queda con tiempo O(1)
			}
			// tripleta ai, bi, mi
			if (!flag)
			{
				tabla[i][0] = mi;
				tabla[i][1] = ai;
				tabla[i][2] = bi;
				break;
			}
			else
				flag = 0;
		}
	}

	cout << "Tiempo requerido: ";
	cout << duration_cast<seconds>(high_resolution_clock::now() - start).count() << "s" << endl
		 << endl;
}

void HashPerfecto::porcentaje(int i, int j)
{
	if ((100.0 * i) / j >= pc)
	{
		cout << "[]";
		pc += 10;
	}
	if (i == j - 1)
	{
		cout << "[]" << endl;
		pc = 10;
	}
}
/**
 * @brief Tabla, con cota 2n
 *
 */
void HashPerfecto::tabla2n()
{
	vector<vector<int>> tablaAux(m);
	uint ac = a, bc = b;

	while (true)
	{
		int sum = 0;
		a = (rand() + rand() << 15) % p;
		b = (rand() + rand() << 15) % p;
		for (auto kmer : mapkmers)
			tablaAux[h(kmer.first)].push_back(kmer.first);
		for (auto c : tablaAux)
			sum += c.size() * c.size();
		if (sum < 2 * m)
		{
			a = ac;
			b = bc;
			break;
		}
		else
			rep2++;
	}
}
/**
 * @brief Dado un x a buscar, se aplica h(x) y se obtiene el bucket y en tabla de primer nivel.
 * El bucket y tiene almacenado la tripleta (my, ay, by) asociada a hy,
 * luego se aplica hy(x) y se encuentra el elemento que se busca en la tabla de segundo nivel correspondiente.
 *
 * @param kmer x
 * @return numero de veces que se repite el elemento que se busca
 */
int HashPerfecto::search(string kmer)
{
	if (kmer.size() != k)
		return -1;
	int knum = kmerToInt(kmer); // x
	int pos = h(knum);			// h(x)

	if (tabla[pos].empty()) // colision
		return 0;

	mi = tabla[pos][0];
	ai = tabla[pos][1];
	bi = tabla[pos][2];

	return tabla[pos][3 + hi(knum)];
}

int main()
{
	string nombre;
	cout << "1: GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna" << endl;
	cout << "2: t.txt" << endl;
	cout << "Ingresar numero o nombre del archivo: ";
	cin >> nombre;

	if (nombre == "1")
		nombre = "GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna";
	if (nombre == "2")
		nombre = "t.txt";

	ifstream archivo(nombre);
	string genoma;
	int copiar = 1;
	while (true)
	{
		string data;
		archivo >> data;
		if (data.empty())
			break;

		if (data[0] == '>')
			copiar = 0;
		if (copiar)
			genoma += data;
		if (data == "sequence")
			copiar = 1;
	}

	archivo.close();
	HashPerfecto h = HashPerfecto(&genoma);

	string kmer;
	cout << "Ingresar 15-mer a buscar, 0 para salir" << endl;
	while (kmer != "0")
	{
		cin >> kmer;
		cout << "Cantidad: " << h.search(kmer) << endl;
	}

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