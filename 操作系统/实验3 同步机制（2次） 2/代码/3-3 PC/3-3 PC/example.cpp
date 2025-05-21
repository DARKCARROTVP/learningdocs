
#include <windows.h>
#include <process.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

const int BUFFER_NUM = 5;               /* ����������*/
int ROUND;                    /* ÿ�������߻����������е�����*/
int TIME;//����ÿ�����������ѵ�ʱ��

char *fruit[10] = { "����", "ƻ��", "�㽶", "����", "��ݮ", "��֦", "ӣ��", "����", "����", "Ѽ��" };

struct Buffer
{
	int buf[BUFFER_NUM]; //������
	int out, in; //����ָ��
}pub_buf;

HANDLE empty, full, mutex;

//�������߳�
unsigned __stdcall Consumer(void* para)
{
	//i ��ʾ��i ��������
	int i = *((int *)para);
	int ptr; //�����ѵ����ݵ�ָ��
	int fruitIndex;
	int count = ROUND;
	int t = TIME;

	while (count--)
	{
		printf("������%d: ��Ҫ��...\n", i);
		WaitForSingleObject(full, INFINITE);       //�ȴ���Ʒ
		WaitForSingleObject(mutex, INFINITE);        //�в�Ʒ, ����ס������pub_buf
		ptr = pub_buf.out;    //��¼���ѵ���Ʒ
		pub_buf.out = (pub_buf.out + 1) % BUFFER_NUM;        //���ƶ�������ָ��
		fruitIndex = pub_buf.buf[ptr];

		printf("������%d: ��ʼ��λ��λ��buf[%d]��ˮ����%s\n", i, ptr, fruit[fruitIndex]);
		ReleaseSemaphore(mutex, 1, NULL);
		ReleaseSemaphore(empty, 1, NULL);            //�������, ���ͷ�һ������

		Sleep(t);

	}

	return 0;
}

//�������߳�
unsigned __stdcall Producer(void* para)
{
	int i = *((int *)para);
	int ptr;
	int data; //��Ʒ
	int count = ROUND;
	int t = TIME;

	srand((unsigned int)i);

	printf("������%d������...�ܹ�Ҫ����%d��\n", i, count);

	while (count--)
	{
		Sleep(t);
		data = rand() % 10;
		printf("������%d: ����һ��ˮ��:%s\n", i, fruit[data]);
		WaitForSingleObject(empty, INFINITE);
		WaitForSingleObject(mutex, INFINITE); //�еط�, ����ס������pub_buf
		ptr = pub_buf.in; //��¼���ѵ���Ʒ
		pub_buf.in = (pub_buf.in + 1) % BUFFER_NUM;

		printf("������%d: ��ʼ��λ��buf[%d]����ˮ����%s\n", i, ptr, fruit[data]);
		pub_buf.buf[ptr] = data;

		ReleaseSemaphore(mutex, 1, NULL);  //�����������߻�������ʹ��pub_buf
		ReleaseSemaphore(full, 1, NULL); //�ź������, �ͷ�һ����Ʒ
	}

	return 0;
}

int main()
{

	//�̼߳���, ǰ��Ϊ�������߳�, ����Ϊ�������߳�
	HANDLE hThreadGroup[30];
	int ThreadNum[30]; //����̵߳��ڲ����
	unsigned tid;
	int i, threadnumber, totalThreads = 0;

	//��ʼ���ź���
	mutex = CreateSemaphore(NULL, 1, 1, NULL);
	empty = CreateSemaphore(NULL, BUFFER_NUM, BUFFER_NUM, NULL);  //�ź���empty�ĳ�ֵΪBUFFER_NUM�����ֵΪBUFFER_NUM
	full = CreateSemaphore(NULL, 0, BUFFER_NUM, NULL);  //�ź���full�ĳ�ֵΪ0�����ֵΪBUFFER_NUM
	if (!empty || !full || !mutex)
	{
		printf("Create Semaphone Error!\n");
		return -1;
	}

	//��ʼ����������in��outָ�����
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

	//�ȴ����е������ߺ�������ִ�����
	WaitForMultipleObjects(totalThreads, hThreadGroup, true, INFINITE);

	//�ر����д򿪵ľ��
	for (i = 0; i<totalThreads; i++) CloseHandle(hThreadGroup[i]);
	CloseHandle(mutex);
	CloseHandle(empty);
	CloseHandle(full);

	printf("�����������Ͼ�Ҫ�����ˡ�\n");
	getchar();
	return 0;

}

