#include "HashPerfecto.h"
#include <iostream>
#include <vector>
#include <unordered_set>
#include <chrono>
#include <fstream>
#include <random>

using namespace std;
using namespace chrono;

/**
 * @brief Construct a new Hash Perfecto:: Hash Perfecto object
 * Antes de crear la tabla hash se deben inicializar y validar todos los valores necesarios.
 * Luego, se deben crear los k-mers del genoma (se almacenaran en un set temporalmente) y que seran almacenados mediante hashing a una tabla.
 * Finalmente, se hace hash a los k-mers y se crea la tabla hash.
 * @param genoma genoma
 */
HashPerfecto::HashPerfecto(string &genoma)
{
	k = 15;
	if (genoma.size() < k)
		throw invalid_argument("Genoma de largo insuficiente");

	unordered_set<int> setKmers;
	m = procesarkmers(genoma, setKmers);
	p = nextPrime(10 * m);

	rep = 1;
	cota = 4 * m;
	crearTabla(setKmers);
}

/**
 * @brief Hashing tabla de primer nivel
 * Usar la siguiente familia de funciones hash universales. Donde
 * p es un numero primo, a y b son valores aleatorios en el rango [0..p − 1],
 * y m el numero de buckets de la tabla.
 * h(k) = ((a × k + b)mod p)mod m)

 * @param kmerc (int)kmer
 * @return posicion tabla de primer nivel
 */
int HashPerfecto::h(int kmerc)
{
	return abs(((a * kmerc + b) % p) % m);
}

/**
 * @brief Hashing tabla de segundo nivel
 *
 * @param kmerc (int)kmer
 * @return posicion tabla de segundo nivel, donde se almacenara el kmer
 */
int HashPerfecto::hi(int kmerc)
{
	return abs(((ai * kmerc + bi) % p) % mi);
}

/**
 * @brief Encontrar el siguiente numero primo despues de n
 *
 * @param n valor al cual se desea buscar su proximo primo
 * @return int, proximo primo
 */
int HashPerfecto::nextPrime(int n)
{
	while (true)
	{
		int flag = 1;
		n++;

		if (n <= 1)
			continue;
		else if (n <= 3)
			break;
		else if (n % 2 == 0 || n % 3 == 0)
			continue;
		else
			for (int i = 5; i * i <= n; i = i + 6)
			{
				if (n % i == 0 || n % (i + 2) == 0)
				{
					flag = 0;
					break;
				}
			}
		if (flag)
			break;
	}
	return n;
}

/**
 * @brief Codificar el string kmer a int
 *
 * @param kmer kmer en string
 * @return kmer como int
 */
int HashPerfecto::codificar(string kmer)
{
	int kmerc = 0;
	for (int i = 0; i < k; i++)
	{
		if (kmer[i] == 'A')
			kmerc += 0 << i * 2;
		else if (kmer[i] == 'C')
			kmerc += 1 << i * 2;
		else if (kmer[i] == 'T')
			kmerc += 2 << i * 2;
		else if (kmer[i] == 'G')
			kmerc += 3 << i * 2;
		else
			throw invalid_argument("Nucleotido invalido");
	}
	return kmerc;
}

/**
 * @brief Conseguir todos los 15-mers
 * Se elige un substring de largo 15 del string genoma para el 15-mer, y luego se llama a la funcion codificar para retornar un int.
 * Despues, se almacena el 15-mer (int) en el set.
 * Se utiliza la funcion substr(i, k), ya que el 15-mer empieza en la posicion i, tiene un largo k = 15
 * @param genoma el genoma (string)
 * @param setKmers set que almacenara los 15-mers
 * @return int, numero de k-mers no distintos, tamano del set
 */
int HashPerfecto::procesarkmers(string &genoma, unordered_set<int> &setKmers)
{
	for (int i = 0; i < genoma.size() - (k - 1); i++)
		setKmers.insert(codificar(genoma.substr(i, k)));
	return setKmers.size();
}

/**
 * @brief Creacion de las 2 tablas
 * Tabla de primer nivel:
 * Creamos una tabla auxiliar tabla1 de tamaño m, para almacenar los k-mers con el hash h.
 * Esa misma tabla, se va convertir en la tabla real, pero le falta el hash del segundo nivel.
 * Tabla de segundo nivel:
 * Para cada bucket de la tabla de primer nivel, creamos un vector temporal tabla2,
 * que almacenara los elementos de ese bucket.
 * Almacenamos los elementos de ese bucket mediante el hash hi en la tabla2,
 * y al terminar de almacenarlos todos, la tabla2 se convierte en ese bucket, que es lo que queriamos.
 * Repetir con cada bucket de la tabla de primer nivel.
 * @param setKmers set que contiene los k-mers
 */
void HashPerfecto::crearTabla(unordered_set<int> &setKmers)
{
	minstd_rand rng(time(NULL));

	while (true)
	{
		a = rng() % p;				   // valor aleatorio entre [0..p − 1]
		b = rng() % p;				   // valor aleatorio entre [0..p − 1]
		vector<vector<int>> tabla1(m); // tabla de primer nivel, tamaño m
		for (int kmer : setKmers)
			// hash k-mer e insertarlo en su tabla de segundo nivel respectiva, tabla de segundo nivel auxiliar
			tabla1[h(kmer)].push_back(kmer);
		// Condicion de sumatoria de i = 0 hasta m-1 de ci^2 < 4n
		int c = 0;					  // sumatoria de i = 0 hasta m-1 de ci^2
		for (vector<int> v : tabla1)  // 0 hasta m-1
			c += v.size() * v.size(); // ci^2
		if (c < cota)				  // funcion hash buena
		{
			tabla = tabla1;
			break;
		}
		else // repetir y aumentar contador
			rep++;
	}

	for (int i = 0; i < m; i++)
	{
		mi = tabla[i].size() * tabla[i].size(); // mi = ci^2

		while (mi)
		{
			bool colision = false;
			ai = rng() % p;
			bi = rng() % p;
			vector<int> tabla2(3 + mi); // tabla de segundo nivel, 3 espacios extras para almacenar ai, bi, mi

			// recorrer todos los elementos de un bucket de la tabla de primer nivel,
			// ya que los elementos solo fueron insertados, sin hash
			// hacerles hash a la tabla de segundo nivel recien creada
			// la nueva tabla se convertira en la tabla real de ese bucket
			for (int kmer : tabla[i])
			{
				int pos = 3 + hi(kmer); // hash
				if (!tabla2[pos])
					tabla2[pos] = kmer;
				// si ya existe un elemento (colision)
				else
				{
					colision = true;
					break;
				}
			}
			if (!colision)
			{
				// tripleta ai, bi, mi
				tabla2[0] = mi;
				tabla2[1] = ai;
				tabla2[2] = bi;
				// la nueva tabla se convertira en la tabla real de ese bucket
				tabla[i] = tabla2;
				break;
			}
		}
	}
}

/**
 * @brief Dado un x a buscar, se aplica h(x) y se obtiene la tabla de segundo nivel.
 * La tabla de segundo nivel tiene almacenado la tripleta (my, ay, by) asociada a hi,
 * luego se aplica hi(x) y se encuentra el elemento que se busca en la tabla de segundo nivel correspondiente.
 *
 * @param kmer x
 * @return true, si se encuentra el k-mer
 * @return false, en otro caso
 */
bool HashPerfecto::search(string kmer)
{
	if (kmer.size() != k)
		return false;

	int kmerc = codificar(kmer); // x
	int pos1 = h(kmerc);		 // h(x)

	if (tabla[pos1].empty()) // colision
		return false;

	mi = tabla[pos1][0];
	ai = tabla[pos1][1];
	bi = tabla[pos1][2];

	int kmerTabla = tabla[pos1][3 + hi(kmerc)];
	if (kmerTabla == kmerc)
		return true;
	else
		return false;
}

/**
 * @brief Retornar las repeticiones necesarias para encontrar a y b
 *
 * @return int, repeticiones
 */
int HashPerfecto::repeticiones()
{
	return rep;
}

/**
 * @brief Funcion para calcular la memoria utilizada
 *
 * @return int
 */
int HashPerfecto::memoria()
{
	int mem = 0;
	mem += sizeof(HashPerfecto);
	mem += sizeof(int) * 10;
	mem += sizeof(vector<vector<int>>);
	for (vector<int> v : tabla)
		mem += sizeof(vector<int>) + sizeof(int) * v.capacity();
	return mem;
};