#include <stdio.h>
#include<iostream>
#include<algorithm>
#include<cstring>
#include<cmath>
#include<vector>
#include<queue>
#include<map>
#include<set>
#include<stack>
#include<cstdlib>
#include<string>
#include<bitset>
#include<iomanip>
#include<deque>
#include<utility>
#include<functional>
#include<sstream>
#include<ctime>
#include<unordered_map>
#include<fstream>
#define INF 1000000000
#define fi first
#define se second
#define debug(x) cerr<<#x<<"="<<x<<endl
#define MP(x,y) make_pair(x,y)
#define WIN 0
#define LOSE 1
#define PLAYER0 0
#define PLAYER1 1
#define DELETED 1
using namespace std;
typedef long long LL;
typedef pair<int, int> pii;

/*
Hash rule:
Use mix-based number to represent a position(game map + players location)

Game board grids were numbered as following, for an example of 4 * 5:
0  1  2  3  4
5  6  7  8  9
10 11 12 13 14
15 16 17 18 19

lowest n*m is binary bit, represent the game board
then is two digit of base-(n*m), represent the location of player0 and player1

For example, a gameboard like this: '.' is valid grid, 'x' is deleted grid, 0 is player0, 1 is player1
0...
...x
.x..
...1
then hash values can be calculate as:
(2^7 + 2^9) + (2^16 * 0) + (2^16*16 * 15)

Reader usage: reader.exe database_filename position_hashvalue

Return value is a 8 bit integer(you should only consider the binary representation), the highest bit means win/lose (win is 0, lose is 1), other 7 bits is the remoteness.
For example: (10001110)_2 means: LOSE and 14 remoteness.

May have some bug...
*/

LL get_p(char *str)
{
	int n = strlen(str);
	LL p = 0;
	for (int i = 0; i < n; i++)
		p = p * 10 + str[i] - 48;
	return p;
}

unsigned char buf[10];
int main(int argc, char **argv)
{
	if (argc != 3)
	{
		cout << "usage: reader.exe database_filename position_hashvalue" << endl;
		return 0;
	}
	char *filename = argv[1];
	//debug(argv[1]);
	//debug(argv[2]);
	LL p = get_p(argv[2]);
	//debug(p);
	FILE *fp = fopen(filename, "rb");
	// If you are not using VS, you should try fseek instead
	//fseek(fp, (int)p, SEEK_SET);
	_fseeki64(fp, p, SEEK_SET);
	//lseek(fp, p, SEEK_SET);
	//debug("after fseek");
	fread(buf, 1, 1, fp);
	//debug(int(buf[0]));
	return int(buf[0]);
}
//

