#include <bits/stdc++.h>

using namespace std;

int M = INT_MIN; // max
int n;

/**
 * @brief funcion para asignar un bucket a un elemento del arreglo
 *
 * @param num elemento del arreglo
 * @param k numero de buckets
 * @return alguna posicion int
 */
int assign(int num, int k)
{
	return (k - 1) * num / M;
}

/**
 * @brief Bucket Sort
 * 1. Crea k buckets vacios
 * 2. Asignar los n elementos del arreglo a un bucket con alguna funcion
 * 3. Ordenar los k buckets con alguna funcion
 * 4. Concatenar los buckets en el arreglo
 *
 * @param arr arreglo que se desea ordenar
 * @param k numero de buckets
 */
void bucketSort(int arr[], int k)
{
	// Crear k buckets vacios
	vector<int> buckets[k];
	// Usar una funcion para asignar cada elemento del arreglo a su bucket correspondiente
	for (int i = 0; i < n; i++)
	{
		int c = assign(arr[i], k);
		buckets[c].push_back(arr[i]);
	}
	// Ordenar los k buckets
	for (int i = 0; i < k; i++)
		sort(buckets[i].begin(), buckets[i].end());
	// Concatenar los buckets en el arreglo
	int index = 0;
	for (int i = 0; i < k; i++)
		for (int j = 0; j < buckets[i].size(); j++)
			arr[index++] = buckets[i][j];
}

/* Driver program to test above function */
int main()
{
	srand(time(NULL));
	cout << "Ingrese el numero de elementos (n) y el numero de buckets (k): \n";
	int k;
	cin >> n >> k;

	int arr[n];
	cout << "Elementos: \n";
	for (int i = 0; i < n; i++)
	{
		arr[i] = rand() % 100;
		cout << arr[i] << " ";
		if (arr[i] > M) // mayor
			M = arr[i];
	}

	bucketSort(arr, k);
	cout << " \nOrdenados: \n";
	for (int i = 0; i < n; i++)
		cout << arr[i] << " ";
	return 0;
}
