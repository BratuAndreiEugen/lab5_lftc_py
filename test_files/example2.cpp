#include <iostream>
using namespace std;

int main()
{
    int a, b;
    cin >> a >> b;
    int r;
    a =12.34e-5;
    b = 0x123alL;
    while (b!= 0||a == 0) {
        r =132ll%b;
        a = b;
        b = r;
    }

    cout << a;

    return 0;

}