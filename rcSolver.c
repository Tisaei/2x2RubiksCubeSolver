#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// 参照↓ (PDFファイルがダウンロードされる)
// https://uec.repo.nii.ac.jp/?action=repository_action_common_download&item_id=6803&item_no=1&attribute_id=20&file_no=1

#define SIZE_OF_ARRAY(array) (sizeof(array)/sizeof(array[0]))
#define INVALID 9
#define SOLVED 1
#define NOT_SOLVED 0
#define CPCO_NUM 8
#define MAX_DEPTH 11
#define MAX_WAYS_SIZE MAX_DEPTH * 3

const char* path = "solve_way.txt";

typedef struct{
	char cp[CPCO_NUM];
	char co[CPCO_NUM];
} state_t;

void print_array(const char*, int);
state_t twist(state_t, int);
int distance(state_t);
int search_tree(state_t, int, int[]);
char* solve(state_t);

const state_t solvedState = {{0,1,2,3,4,5,6,7}, {0,0,0,0,0,0,0,0}};
const state_t numMove[] = {
	{{3,0,1,2,4,5,6,7}, {0,0,0,0,0,0,0,0}},
	{{2,3,0,1,4,5,6,7}, {0,0,0,0,0,0,0,0}},
	{{1,2,3,0,4,5,6,7}, {0,0,0,0,0,0,0,0}},
	{{0,1,3,7,4,5,2,6}, {0,0,1,2,0,0,2,1}},
	{{0,1,7,6,4,5,3,2}, {0,0,0,0,0,0,0,0}},
	{{0,1,6,2,4,5,7,3}, {0,0,1,2,0,0,2,1}},
	{{0,2,6,3,4,1,5,7}, {0,1,2,0,0,2,1,0}},
	{{0,6,5,3,4,2,1,7}, {0,0,0,0,0,0,0,0}},
	{{0,5,1,3,4,6,2,7}, {0,1,2,0,0,2,1,0}}
};
const char* numChar[] = {"U","U2","U3","F","F2","F3","R","R2","R3"};

size_t split(char* s, const char* separator, char** result, size_t result_size){
	assert(s != NULL);
	assert(separator != NULL);
	assert(result != NULL);
	assert(result_size > 0);

	size_t i = 0;

	char* p = strtok(s, separator);
	while (p != NULL) {
		assert(i < result_size);
		result[i] = p;
		++i;

		p = strtok(NULL, separator);
	}

	return i;
}

int main(int argc, char *argv[]){
	if(argc < 3){
		printf("Usage: ./rcSolver.out (cp) (co)\n");
		printf("Example: ./rcSolver.out 0,1,2,3,4,5,6,7 0,0,0,0,0,0,0,0\n");
		exit(1);
	}

	/*
	 * テスト用データ.
	 * 5,2,6,3,4,7,1,0 0,0,0,0,0,0,2,1 → U' F U R2 F2 R' F' U F U'
	 */

	char* cpS[CPCO_NUM];
	char* coS[CPCO_NUM];
	split(argv[1], ",", cpS, CPCO_NUM);
	split(argv[2], ",", coS, CPCO_NUM);

	state_t initCube;
	for(int i = 0; i < CPCO_NUM; i++){
		initCube.cp[i] = atoi(cpS[i]);
		initCube.co[i] = atoi(coS[i]);
	}

	printf("cp : ");
	print_array(initCube.cp, CPCO_NUM);
	printf("  co : ");
	print_array(initCube.co, CPCO_NUM);
	printf("\n");

	char* ways = solve(initCube);
	printf("Result : %s\n", ways);
	FILE* fp = fopen(path, "w");
	if(fp == NULL){
		printf("Oops! Cannot open file!\n");
		exit(1);
	}
	fprintf(fp, "%s", ways);
	fclose(fp);
	free(ways);

	return 0;
}

char* solve(state_t scrambledState){
	int result[MAX_DEPTH];
	for(int i = 0; i < MAX_DEPTH; i++) result[i] = -1;
	int goal;
	char* ways;

	for(int i = 0; i <= MAX_DEPTH; i++){
		goal = search_tree(scrambledState, i, result);
		if(goal) break;
	}

	if(goal){
		ways = (char *)malloc(sizeof(char) * MAX_WAYS_SIZE); //ローカル変数を返すのはマズイのでmallocで領域確保してから返す.
		memset(ways, '\0', sizeof(char) * MAX_WAYS_SIZE);
		if(result[0] != -1) sprintf(ways, "%s", numChar[result[0]]); else return "Already_Solved!";
		for(int i = 1; i < MAX_DEPTH; i++){
			if(result[i] == -1) break;
			assert(strlen(ways) + strlen(",") + strlen(numChar[result[i]]) + 1 <= MAX_WAYS_SIZE);
			sprintf(ways, "%s,%s", ways, numChar[result[i]]);
		}
		return ways;
	}else{
		return "Cannot_Solve!";
	}
}

int array_equal(const char* array1, const char* array2, int size){ //char型の配列の引数は関数内から配列の長さを求められない
	assert(array1 != NULL); assert(array2 != NULL);
	for(size_t i = 0; i < size; ++i) if(array1[i] != array2[i]) return 0;
	return 1;
}

void print_array(const char* array, int size){
	assert(array != NULL);
	for(int i = 0; i < size - 1; i++) printf("%d, ", array[i]);
	printf("%d", array[size - 1]);
}

typedef struct{
	state_t cube;
	int remainDepth;
	int moveN;
	int move;
} searchNode_t;

const int preUMoveList[] = {3,4,5,6,7,8};
const int preFMoveList[] = {0,1,2,6,7,8};
const int preRMoveList[] = {0,1,2,3,4,5};
const int NPreMoveList[] = {0,1,2,3,4,5,6,7,8};
const int* limitedMove[] = {
	preUMoveList,
	preFMoveList,
	preRMoveList,
	NPreMoveList
};
const int limitedMoveN[] = {
	SIZE_OF_ARRAY(preUMoveList),
	SIZE_OF_ARRAY(preFMoveList),
	SIZE_OF_ARRAY(preRMoveList),
	SIZE_OF_ARRAY(NPreMoveList)
};

int search_gvdfxbctree(const state_t cube, int searchDepth, int result[MAX_DEPTH]){
	searchNode_t* pNode;
	searchNode_t nodeArray[MAX_DEPTH + 1];
	int tw;

	nodeArray[0].cube = cube;
	nodeArray[0].moveN = -1;
	nodeArray[0].move = INVALID;
	nodeArray[1].moveN = -1;

	pNode = nodeArray;

	pNode[0].remainDepth = searchDepth;

	while(pNode >= nodeArray){
		if(pNode[0].remainDepth == 0){
			if(array_equal(pNode[0].cube.cp, solvedState.cp, CPCO_NUM) && array_equal(pNode[0].cube.co, solvedState.co, CPCO_NUM)){
				for(int i = 0; i < searchDepth; ++i) result[i] = nodeArray[i+1].move;
				double sec = (double)clock() / CLOCKS_PER_SEC;
				printf("Solved!    at %2d\ntime : %f\n\n", searchDepth, sec);
				for(int i = 0; i < searchDepth; i++){
					printf("cp : ");
					print_array(nodeArray[i + 1].cube.cp, CPCO_NUM);
					printf("  co : ");
					print_array(nodeArray[i + 1].cube.co, CPCO_NUM);
					printf("\n");
				}
				printf("\n");
				return SOLVED;
			}
			pNode--;
		}else{
			const int* moveList = limitedMove[pNode[0].move / 3];
			int cycleN = limitedMoveN[pNode[0].move / 3];

			for(tw = pNode[1].moveN + 1; tw < cycleN; tw++){
				pNode[1].remainDepth = pNode[0].remainDepth - 1;
				pNode[1].cube = twist(pNode[0].cube, moveList[tw]);
				if(pNode[1].remainDepth < distance(pNode[1].cube)) continue;
				pNode[1].moveN = tw;
				pNode[1].move = moveList[tw];
				break;
			}

			if(tw == cycleN){
				pNode--;
			}else{
				pNode++;
				pNode[1].moveN = -1;
			}
		}
	}

	printf("Not Solved at %2d\n", searchDepth);
	return NOT_SOLVED;
}

state_t twist(const state_t cube, int move){
	state_t new_cube;
	state_t moveS = numMove[move];
	for(int i = 0; i < CPCO_NUM; i++){
		new_cube.cp[i] = cube.cp[moveS.cp[i]];
		new_cube.co[i] = (cube.co[moveS.cp[i]] + moveS.co[i]) % 3;
	}
	return new_cube;
}

int distance(const state_t cube){
	int whiteN = 0;
	int yellowN = 0;
	for(int i = 0; i < 4; i++){
		if(cube.cp[i] >= 0 && cube.cp[i] < 4 && cube.co[i] == 0) whiteN++;
	}

	switch(whiteN){
		case 0:
			for(int i = 4; i < 8; i++){
				if(cube.cp[i] >= 4 && cube.cp[i] < 8 && cube.co[i] == 0) yellowN++;
			}
			switch(yellowN){
				case 1:
				case 2:
					return 3;
				default:
					return 5;
			}

		case 1:
			for(int i = 4; i < 8; i++){
				if(cube.cp[i] >= 4 && cube.cp[i] < 8 && cube.co[i] == 0) yellowN++;
			}
			switch(yellowN){
				case 1:
					return 2;
				case 2:
				case 3:
					return 3;
				default:
					return 6;
			}

		case 2:
			for(int i = 4; i < 8; i++){
				if(cube.cp[i] >= 4 && cube.cp[i] < 8 && cube.co[i] == 0) yellowN++;
			}
			switch(yellowN){
				case 1:
				case 3:
					return 3;
				case 2:
					return 1;
				default:
					return 6;
			}

		case 3:
			return 3;

		default:
			for(int i = 4; i < 8; i++){
				if(cube.cp[i] >= 4 && cube.cp[i] < 8 && cube.co[i] == 0) yellowN++;
			}
			switch(yellowN){
				case 1:
				case 2:
					return 6;
				default:
					{
						int solvedC = 0;
						for(int i = 0; i < CPCO_NUM; i++) if(cube.cp[i] == i && cube.co[i] == 0) solvedC++;
						if(solvedC < 4) return 1;
					}
					return 0;
			}
	}
}
