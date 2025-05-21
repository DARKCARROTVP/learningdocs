#include <windows.h>
#include <process.h>
#include <stdio.h>

struct ProcParam {
	int wait_time;
	int goods_num;
	int threadid;
};

unsigned __stdcall FirstThreadFunc(void * arg){
	ProcParam *param;
	param = (ProcParam*)arg;
	printf("%d %d %d\n", param->wait_time, param->goods_num, param->threadid);
	return 0;
}

int  main ( ) {
	const int THREADNUM = 10;
	int i;
	ProcParam *param = new ProcParam[THREADNUM];
		
	HANDLE hThread[THREADNUM];
	unsigned int threadID[THREADNUM];
	for(i=0;i<THREADNUM;i++){
		param[i].wait_time = (i+1)*10;
		param[i].goods_num = (i+1)*2;
		param[i].threadid = i+1;
		hThread[i] = (HANDLE)_beginthreadex(NULL, 0, FirstThreadFunc, (void*)&param[i], 0, &threadID[i]);
	}
	WaitForMultipleObjects(THREADNUM,hThread,TRUE,INFINITE);
	getchar();
	return 0;
}
