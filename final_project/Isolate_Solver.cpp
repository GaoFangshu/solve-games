// Isolate_Solver.cpp: 
// https://en.wikipedia.org/wiki/Isolation_(board_game)
//
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
typedef LL Position; // 32 bits
typedef int Location; // 5 bits
typedef int GameBoard; // n*m bits
typedef char int8;
typedef pair<pii, pii> Move;
typedef pair<int8, int8> pcc;

// Following are the game parameters
#define N 4
#define M 4
const int SIZE = N * M;
const LL BASE[2] = { 1 << SIZE, (1 << SIZE) * SIZE };
const LL TOTAL_POSITION = (1ll << SIZE) * SIZE * SIZE;
const int dx[9] = { -1, -1, -1, 0, 0, 1, 1, 1 }, dy[9] = { -1, 0, 1, -1, 1, -1, 0, 1 };
LL cnt_true_postion = 0, cnt_primitive_position = 0, cnt_win_position = 0, cnt_lose_position = 0, cnt_total_children;

/*
Use mix-based number to represent a position(game map + players location + turn)

Game board grids were numbered as following, for an example of 4 * 5: 
0  1  2  3  4
5  6  7  8  9
10 11 12 13 14
15 16 17 18 19

lowest n*m is binary bit, represent the game board
then is two digit of base-(n*m), represent the location of player0 and player1
*/
inline Position getPosition(int turn, Location l0, Location l1, GameBoard g)
{
	return (l0 << SIZE) + (l1 << SIZE) * SIZE + g;
}

inline int count_one(unsigned int x)
{
	// no __builtin_popcount in microsoft c++, only in gcc.
	int cnt = 0;
	while(x)
	{
		if (x & 1)
			cnt++;
		x >>= 1;
	}
	return cnt;
}

inline int getTurn(Position p)
{
	return count_one(p & ((1 << SIZE) -1)) & 1;
}

inline pii getCoordinate(Location l)
{
	return MP(l / M, l % M);
}
/*
inline Location calLocation(int i, int j)
{
	return i * M + j;
}*/
inline Location calLocation(pii c)
{
	return c.fi * M + c.se;
}

inline int getLocation(Position p, int player)
{
	p = p >> SIZE;
	if (player == PLAYER0)
		return p % SIZE;
	else
		return p / SIZE;
}

inline GameBoard getGameBoard(Position p)
{
	return p & ((1 << SIZE) - 1);
}
/*
inline int getState(GameBoard g, int i, int j)
{
	return g & (1 << (i*M + j));
}*/

inline int getState(GameBoard g, pii c)
{
	return (g & (1 << calLocation(c))) >> calLocation(c);
}

inline int getState(GameBoard g, Location l)
{
	return (g & (1 << l)) >> l;
}

inline Position setLocation(Position p, pii c)
{
	int turn = getTurn(p), last_loc = getLocation(p, turn);
	p = p - last_loc * BASE[turn] + calLocation(c) * BASE[turn];
	return p;
}

Position initStart()
{
	Position start_p = getPosition(0, calLocation(MP(0, (M - 1) / 2)), calLocation(MP(N - 1, M / 2)), 0);
	return start_p;
}

int8 *rel;

bool check_Valid1(Position& p, pii c, Location l, Location& other)
{
	if (c.first < 0 || c.first >= N || c.second < 0 || c.second >= M)
		return 0;
	//debug(c.first);
	//debug(c.second);
	if (getState(p, l) != DELETED && other!= l)
		return 1;
	else
		return 0;
}

bool check_Valid2(Position& p, Location l, Location& l0, Location& l1)
{
	//if (c.first < 0 || c.first >= N || c.second < 0 || c.second >= M)
		//return 0;
	//debug(c.first);
	//debug(c.second);
	if (getState(p, l) != DELETED && l0 != l && l1 != l)
		return 1;
	else
		return 0;
}
// a Move is a Jump + a Delete

vector<pii> genJump(Position p)
{
	vector<pii> jump;
	int turn = getTurn(p), gameboard = getGameBoard(p);
	Location other = getLocation(p, turn ^ 1);
	pii c = getCoordinate(getLocation(p, turn));
	for (int k = 0; k < 8; k++)
	{
		pii new_c = MP(c.first + dx[k], c.second + dy[k]);
		if (check_Valid1(p, new_c, calLocation(new_c), other))
			jump.push_back(new_c);
	}
	//debug(jump.size());
	return jump;
}

Position doJump(Position p, pii c)
{
	return setLocation(p, c);
}

bool isPrimitive(Position p)
{
	return genJump(p).size() == 0;
}

inline Position doDelete(Position& p, Location& l)
{
	return p | (1 << l);
}

Position doDelete(Position p, pii c)
{
	return p | (1 << calLocation(c));
}

Position swapTurn(Position p)
{
	return p;
	//return p ^ (1 << TURN_BIT);
}

Position doMove(Position p, Move m)
{
	return swapTurn(doDelete(doJump(p, m.first), m.second));
}

vector<Move> genMove(Position p)
{
	auto jumps = genJump(p);
	Position p_mid;
	vector<Move> mv;
	for (int i = 0; i < jumps.size(); i++)
	{
		p_mid = doJump(p, jumps[i]);
		Location l0 = getLocation(p_mid, 0), l1 = getLocation(p_mid, 1);
		for (int j = 0; j < SIZE; j++)
		{
			if (check_Valid2(p_mid, j, l0, l1))
				mv.push_back(MP(jumps[i], getCoordinate(j)));
		}
	}
	return mv;
}

vector<Position> genChildren(Position p)
{
	auto jumps = genJump(p);
	Position p_mid;
	vector<Position> chl;
	for (int i = 0; i < jumps.size(); i++)
	{
		p_mid = doJump(p, jumps[i]);
		Location l0 = getLocation(p_mid, 0), l1 = getLocation(p_mid, 1);
		for (int j = 0; j < SIZE; j++)
		{
			if (check_Valid2(p_mid, j, l0, l1))
				chl.push_back(doDelete(p_mid, j));
		}
	}
	return chl;
}

void printPosition(Position p)
{
	printf("turn = %d, l0 = %d, l1 = %d\n", getTurn(p), getLocation(p, 0), getLocation(p, 1));
}

int8 makeResult(int val, int rmt)
{
	return (val << 7) | rmt;
}

int8 solve(Position p)
{
	//printPosition(p);
	if (rel[p] != -1)
		return rel[p];
	cnt_true_postion++;
	if (cnt_true_postion % 1000000 == 0)
		debug(cnt_true_postion);
	if (isPrimitive(p))
	{
		rel[p] = makeResult(LOSE, 0);
		cnt_primitive_position++;
		return rel[p];
	}
	//auto moves = genMove(p);
	auto children = genChildren(p);
	cnt_total_children += children.size();
	int flag = LOSE, remote = 0;
	for (auto new_p : children)
	{
		//Position new_p = doMove(p, m);
		int8 rel = solve(new_p);
		int curr_val = int(rel & (1<<7)) >> 7, curr_rmt = int(rel) & ((1 << 7) - 1);
		if (flag == LOSE)
			if (curr_val == LOSE)
			{
				flag = WIN;
				remote = curr_rmt;
			}
			else
				remote = max(remote, curr_rmt);
		else
			if(curr_val == LOSE)
				remote = min(remote, curr_rmt);
	}
	
	rel[p] = makeResult(flag, remote + 1);
	if (flag == WIN)
		cnt_win_position++;
	else
		cnt_lose_position++;

	return rel[p];
}

void printFile()
{
	string filename = "database_" + to_string(N) + "_" + to_string(M) + ".db";
	FILE* fp;
	fp = fopen(filename.c_str(), "wb");
	fwrite(rel, sizeof(int8), TOTAL_POSITION, fp);
}

void printAnalysis()
{
	Position start_p = initStart();
	int8 rel = solve(start_p);
	int curr_val = int(rel & (1 << 7)) >> 7, curr_rmt = int(rel) & ((1 << 7) - 1);
	string filename = "log_" + to_string(N) + "_" + to_string(M) + ".txt";
	FILE* fp;
	fp = fopen(filename.c_str(), "w");
	fprintf(fp, "Upper bound is %I64d, actual position is %I64d\n", TOTAL_POSITION, cnt_true_postion);
	fprintf(fp, "Start position's value is %d, remoteness is %d\n", curr_val, curr_rmt);
	fprintf(fp, "Primitive position is %I64d\n", cnt_primitive_position);
	fprintf(fp, "Win position is %I64d, Lose position is %I64d\n", cnt_win_position, cnt_lose_position);
	fprintf(fp, "Average children is %.3f\n", (double)cnt_total_children / cnt_true_postion);
}

int main()
{	
	LL st_time = clock();
	rel = new int8[TOTAL_POSITION];
	debug(TOTAL_POSITION);
	memset(rel, -1, TOTAL_POSITION);
	Position start_p = initStart();
	cout << "start solving!" << endl;
	solve(start_p);
	LL sol_time = clock();
	debug(sol_time - st_time);
	//debug(rel.size());
	//printJson();
	printAnalysis();
	printFile();
	LL ed_time = clock();
	debug(ed_time - st_time);
	debug(cnt_true_postion);
    return 0;
}
/*
TOTAL_POSITION=419430400
sol_time - st_time=356120
ed_time - st_time=363891
cnt_true_postion=97976968
*/