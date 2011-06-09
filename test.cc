#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

int main()
{
	vector<int> v;

	v.push_back(1);
	v.push_back(2);

	if (find(v.begin(), v.end(), 1) != v.end())
		cout << "found" << endl;
	else
		cout << "not found" << endl;

	if (find(v.begin(), v.end(), 3) != v.end())
		cout << "found" << endl;
	else
		cout << "not found" << endl;
}
