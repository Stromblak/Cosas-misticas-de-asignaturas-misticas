#include <bits/stdc++.h>

using namespace std;

int M = INT_MIN; // max
int n = 20;
/**
 * @brief funcion para asignar un bucket a un elemento del arreglo
 *
 * @param num elemento del arreglo
 * @param k numero de buckets
 * @return alguna posicion in
 */
int assign(int num, int k)
{
	return num / k;
}

/**
 * @brief
 *
 * @param arr
 * @param k
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
	for (int i = 0; i < n; i++)
		for (int j = 0; j < buckets[i].size(); j++)
		{
			arr[index] = buckets[i][j];
			index++;
		}
}

/* Driver program to test above function */
int main()
{
	srand(time(NULL));
	int arr[n];
	cout << "Elementos: \n";
	for (int i = 0; i < n; i++)
	{
		arr[i] = rand() % 100;
		cout << arr[i] << " ";
		if (arr[i] > M)
			M = arr[i];
	}
	int k = 10;
	// hay un error aqui creo ._.
	bucketSort(arr, k);
	cout << " \nOrdenados: \n";
	for (int i = 0; i < n; i++)
		cout << arr[i] << " ";
	return 0;
}
