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
	string genoma;
	map<int, int> mapkmers;
	vector<vector<int>> tabla;
	int p, k, rep4, rep2, pc; // primo, 15, repeticiones 4n, repeticiones 2n
	int a, b, m, ai, bi, mi;
	int h(int knum);
	int hi(int knum);
	int kmerToInt(string kmer);
	void procesarkmers();
	void crearTabla();
	void porcentaje(int i, int j);
	void tabla2n();

public:
	HashPerfecto(string *gen);
	int search(string kmer);
};
/**
 * @brief Construct a new Hash Perfecto:: Hash Perfecto object
 *
 * @param gen genoma
 */
HashPerfecto::HashPerfecto(string *gen)
{
	srand(time(NULL));
	rand();
	genoma = *gen;
	p = 7595479;
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
 * @brief Hashing perfecto primera tabla
 *
 * @param knum (int)kmer
 * @return bucket
 */
int HashPerfecto::h(int knum)
{
	return ((uint)(a * knum + b) % p) % m;
}
/**
 * @brief Hashing perfecto segunda tabla
 *
 * @param knum (int)kmer
 * @return bucket, donde se almacenara el kmer
 */
int HashPerfecto::hi(int knum)
{
	return ((uint)(ai * knum + bi) % p) % mi;
}
/**
 * @brief Transformar el string kmer a int
 *
 * @param kmer kmer en string
 * @return (int)kmer
 */
int HashPerfecto::kmerToInt(string kmer)
{
	int knum = 0;
	for (int i = 0; i < k; i++)
	{
		if (kmer[i] == 'A')
			knum += 0 << i * 2;
		else if (kmer[i] == 'C')
			knum += 1 << i * 2;
		else if (kmer[i] == 'T')
			knum += 2 << i * 2;
		else if (kmer[i] == 'G')
			knum += 3 << i * 2;
	}
	return knum;
}
/**
 * @brief Mapear todos los 15-mers
 * Se elige parte del string genoma para el 15-mer y luego se transforma a int.
 * Despues, se almacena el 15-mer (int) en un map
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
 *
 */
void HashPerfecto::crearTabla()
{
	auto start = chrono::high_resolution_clock::now();

	vector<vector<int>> tablaAux(m); // tabla de tamaño m
	tabla = vector<vector<int>>(m);

	cout << "Creando tabla de primer nivel" << endl;
	while (true)
	{
		a = (rand() + rand() << 15) % p; // valor aleatorio entre [0..p − 1]
		b = (rand() + rand() << 15) % p; // valor aleatorio entre [0..p − 1]
		for (auto kmer : mapkmers)
			tablaAux[h(kmer.first)].push_back(kmer.first); // hash kmer e insertarlo en la tabla
		int sum = 0;									   // sumatoria de i = 0 hasta m-1 de ci^2
		for (auto c : tablaAux)							   // 0 hasta m-1
			sum += c.size() * c.size();					   // ci^2
		if (sum < 4 * m)								   // funcion hash buena
			break;
		else
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

			for (int knum : tablaAux[i])
			{
				if (tabla[i][3 + hi(knum)])
				{
					flag = 1;
					break;
				}
				else
					tabla[i][3 + hi(knum)] = mapkmers[knum];
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
	string genoma, saux;
	int flag = 0;

	cout << "Leyendo genoma" << endl;
	while (cin >> saux && !saux.empty())
	{
		if (saux[0] == '>')
			flag = 1;
		if (!flag)
			genoma += saux;
		if (saux == "sequence")
			flag = 0;
	}

	HashPerfecto h = HashPerfecto(&genoma);

	cout << h.search("GGGGGGGGGGGGGGG") << endl;

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