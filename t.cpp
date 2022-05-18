#include <bits/stdc++.h>

using namespace std;

int main()  
{
  int t, s, a, f;
  cin >> t;
  while (t--)
  {
    cin >> s >> a >> f;
    int street[f];
    int avenue[f];
    for (int i = 0; i < f; i++)
      cin >> street[i] >> avenue[i];
    sort(street, street + f);
    sort(avenue, avenue + f);
    int mid;
    if (f % 2 == 0)
     asd
    else
      mid = (f + 1) / 2 - 1;
    cout << "(Street: " << street[mid] << ", Avenue: " << avenue[mid] << ")" << endl;
  }
  return 0;
}
