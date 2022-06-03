#include <iostream>
#include <vector>
#include <unordered_set>
#include <chrono>
#include <random>

using namespace std;
using namespace chrono;

/**
 * @brief Clase que creara la tabla hash, almacenando los k-mers del genoma
 */
class HashPerfecto
{
private:
	vector<vector<int>> tabla;	// tabla hash de 2 niveles
	int k, rep, cota;			// 15, repeticiones, cota 4m/2m
	int a, b, m, ai, bi, mi, p; // a y b son valores aleatorios, m es el numero de buckets y p es un numero primo
	int h(int kmerc);			// hash para la tabla de primer nivel
	int hi(int kmerc);			// hash para la tabla de segundo nivel
	int nextPrime(int n);		// calcular siguiente numero primo a n
	int codificar(string kmer); // codificar el k-mer de string a int
	int procesarkmers(string &genoma, unordered_set<int> &setKmers); // transformar el genoma a k-mers y codificarlos
	void crearTabla(unordered_set<int> &setKmers); // crear la tabla y almacenar los k-mers mediante hashing

public:
	HashPerfecto(string &genoma); // constructor
	bool search(string kmer);	  // buscar si existe el k-mer
	int repeticiones();			  // retornar el numero de repeticiones de busqueda de a y b (rep)
	int memoria();				  // para analisis experimental de la memoria
};