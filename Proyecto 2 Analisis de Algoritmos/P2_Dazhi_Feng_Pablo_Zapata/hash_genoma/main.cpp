#include "HashPerfecto.h"
#include <iostream>
#include <chrono>
#include <fstream>
#include <random>

using namespace std;
using namespace chrono;

/**
 * @brief Analisis experimental
 *
 * @return int
 */
void stats()
{
	int iter = 15, rep = 10, ts = 100, busq = 10000;
	minstd_rand rng(time(NULL));

	vector<int> repeticiones(iter), memoria(iter), tCrearTabla(iter), tBusqueda(iter), tam(iter);

	for (int i = 0; i < iter; i++)
	{
		for (int j = 0; j < rep; j++)
		{

			string s;
			tam[i] = ts * (i + 1);
			for (int k = 0; k < ts * (i + 1); k++)
			{
				int r = rng() % 4;
				if (r == 0)
					s += 'A';
				if (r == 1)
					s += 'C';
				if (r == 2)
					s += 'T';
				if (r == 3)
					s += 'G';
			}
			auto start = high_resolution_clock::now();
			HashPerfecto h = HashPerfecto(s);
			auto finish = high_resolution_clock::now();
			tCrearTabla[i] += duration_cast<microseconds>(finish - start).count();

			string b;
			for (int k = 0; k < 15; k++)
			{
				for (int m = 0; m < 15; m++)
				{
					int r = rng() % 4;
					if (r == 0)
						b += 'A';
					if (r == 1)
						b += 'C';
					if (r == 2)
						b += 'T';
					if (r == 3)
						b += 'G';
				}
			}
			start = high_resolution_clock::now();
			for (int k = 0; k < busq; k++)
				h.search(b);
			finish = high_resolution_clock::now();
			tBusqueda[i] += duration_cast<nanoseconds>(finish - start).count();

			repeticiones[i] += h.repeticiones();
			memoria[i] += h.memoria();
		}
	}
	cout << endl
		 << "Tam" << endl;
	for (auto a : tam)
		cout << a << endl;

	cout << endl
		 << "Rep" << endl;
	for (auto a : repeticiones)
		cout << (float)a / rep << endl;

	cout << endl
		 << "Mem" << endl;
	for (auto a : memoria)
		cout << (float)a / rep << endl;

	cout << endl
		 << "T crear" << endl;
	for (auto a : tCrearTabla)
		cout << (float)a / rep << endl;

	cout << endl
		 << "T busqueda" << endl;
	for (auto a : tBusqueda)
		cout << (float)a / (rep * busq) << endl;
}

int main()
{
	cout << "1: Ingreso de archivo" << endl;
	cout << "2: Ingreso manual de string" << endl;
	int n;
	cin >> n;
	cout << endl;

	string genoma;
	if (n == 1)
	{
		string nombre;
		string polynesia = "GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna";
		cout << "1: " << polynesia << endl;
		cout << "2: t.txt" << endl;
		cout << "Ingresar numero o nombre del archivo: ";
		cin >> nombre;

		if (nombre == "1")
			nombre = polynesia;
		if (nombre == "2")
			nombre = "t.txt";

		ifstream archivo(nombre);
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
	}
	else
	{
		cout << "Ingresar string" << endl;
		cin >> genoma;
	}

	HashPerfecto h = HashPerfecto(genoma);

	cout << endl
		 << "Ingresar 15-mer a buscar, 0 para salir" << endl;
	while (true)
	{
		string kmer;
		cin >> kmer;
		if (kmer == "0")
			break;
		if (h.search(kmer))
			cout << "Presente en el genoma" << endl;
		else
			cout << "No presente en el genoma" << endl;
	}

	return 0;
}
