
#include <windows.h>
#include <process.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

const int BUFFER_NUM = 5;               /* 缓冲区个数*/
int ROUND;                    /* 每个生产者或消费者运行的轮数*/
int TIME;//定义每次生产或消费的时间

char *fruit[10] = { "桔子", "苹果", "香蕉", "菠萝", "草莓", "荔枝", "樱桃", "葡萄", "桃子", "鸭梨" };

struct Buffer
{
	int buf[BUFFER_NUM]; //缓冲区
	int out, in; //两个指针
}pub_buf;

HANDLE empty, full, mutex;

//消费者线程
unsigned __stdcall Consumer(void* para)
{
	//i 表示第i 个消费者
	int i = *((int *)para);
	int ptr; //待消费的内容的指针
	int fruitIndex;
	int count = ROUND;
	int t = TIME;

	while (count--)
	{
		printf("消费者%d: 我要吃...\n", i);
		WaitForSingleObject(full, INFINITE);       //等待产品
		WaitForSingleObject(mutex, INFINITE);        //有产品, 先锁住缓冲区pub_buf
		ptr = pub_buf.out;    //记录消费的物品
		pub_buf.out = (pub_buf.out + 1) % BUFFER_NUM;        //再移动缓冲区指针
		fruitIndex = pub_buf.buf[ptr];

		printf("消费者%d: 开始吃位于位置buf[%d]的水果：%s\n", i, ptr, fruit[fruitIndex]);
		ReleaseSemaphore(mutex, 1, NULL);
		ReleaseSemaphore(empty, 1, NULL);            //消费完毕, 并释放一个缓冲

		Sleep(t);

	}

	return 0;
}

//生产者线程
unsigned __stdcall Producer(void* para)
{
	int i = *((int *)para);
	int ptr;
	int data; //产品
	int count = ROUND;
	int t = TIME;

	srand((unsigned int)i);

	printf("生产者%d生产中...总共要生产%d个\n", i, count);

	while (count--)
	{
		Sleep(t);
		data = rand() % 10;
		printf("生产者%d: 送来一个水果:%s\n", i, fruit[data]);
		WaitForSingleObject(empty, INFINITE);
		WaitForSingleObject(mutex, INFINITE); //有地方, 先锁住缓冲区pub_buf
		ptr = pub_buf.in; //记录消费的物品
		pub_buf.in = (pub_buf.in + 1) % BUFFER_NUM;

		printf("生产者%d: 开始在位置buf[%d]放置水果：%s\n", i, ptr, fruit[data]);
		pub_buf.buf[ptr] = data;

		ReleaseSemaphore(mutex, 1, NULL);  //让其他消费者或生产者使用pub_buf
		ReleaseSemaphore(full, 1, NULL); //放好了完毕, 释放一个产品
	}

	return 0;
}

int main()
{

	//线程计数, 前面为消费者线程, 后面为生产者线程
	HANDLE hThreadGroup[30];
	int ThreadNum[30]; //存放线程的内部编号
	unsigned tid;
	int i, threadnumber, totalThreads = 0;

	//初始化信号量
	mutex = CreateSemaphore(NULL, 1, 1, NULL);
	empty = CreateSemaphore(NULL, BUFFER_NUM, BUFFER_NUM, NULL);  //信号量empty的初值为BUFFER_NUM，最大值为BUFFER_NUM
	full = CreateSemaphore(NULL, 0, BUFFER_NUM, NULL);  //信号量full的初值为0，最大值为BUFFER_NUM
	if (!empty || !full || !mutex)
	{
		printf("Create Semaphone Error!\n");
		return -1;
	}

	//初始化缓冲区的in和out指针变量
	pub_buf.in = 0;
	pub_buf.out = 0;

	TIME = 90;
	ROUND = 3;
	threadnumber = 0;
	totalThreads = 0;

	for (i = 0; i<5; i++){
		totalThreads++;
		ThreadNum[threadnumber] = i + 1;
		hThreadGroup[threadnumber] = (HANDLE)_beginthreadex(NULL, 0, Producer, &ThreadNum[threadnumber], 0, &tid);
		threadnumber++;
	}

	for (i = 0; i<5; i++){
		totalThreads++;
		ThreadNum[threadnumber] = i + 1;
		hThreadGroup[threadnumber] = (HANDLE)_beginthreadex(NULL, 0, Consumer, &ThreadNum[threadnumber], 0, &tid);
		threadnumber++;
	}

	//等待所有的生产者和消费者执行完毕
	WaitForMultipleObjects(totalThreads, hThreadGroup, true, INFINITE);

	//关闭所有打开的句柄
	for (i = 0; i<totalThreads; i++) CloseHandle(hThreadGroup[i]);
	CloseHandle(mutex);
	CloseHandle(empty);
	CloseHandle(full);

	printf("程序运行马上就要结束了。\n");
	getchar();
	return 0;

}

