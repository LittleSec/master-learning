#include <sys/shm.h>
#include <sys/ipc.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SHM_TAIL ((size_t)sizeof(size_t))
#define SHM_SIZE (1 << 22) // 4MB the first sizeof(size_t) bytes store the tail
#define CONNECT_FAIL -1
#define CREATE_FAIL -2
#define DESTORY_FAIL -3
#define SUCCESS 1

typedef unsigned char u8_t;

int destory_shm(int shmid)
{
    struct shmid_ds sds;
    
    // PC_STAT: sds = shm's sds
    // IPC_SET: shm's sds = sds(if perm)
    // IPC_RMID: delete
    if (shmctl(shmid, IPC_RMID, &sds) != 0)
    {
        // printf("destory shm failed!\n");
        return DESTORY_FAIL;
    }
    else
    {
        return SUCCESS;
    }
}

void read_and_pop_shm(int shmid, u8_t* retbuf, size_t *len)
{
    size_t tail = 0;
    u8_t *ptr;

    ptr = (u8_t *)shmat(shmid, NULL, 0);
    if (atoi((char*)ptr) == -1)
    {
        printf("conn shm failed!\n");
        return;
    }

    memcpy(&tail, ptr, SHM_TAIL);
    u8_t* shmbuf = ptr + SHM_TAIL;
    size_t shm_len = tail;
    size_t n = 0;
    if (shm_len < *len)
    {
        printf("[!] The shm only has %dB, but the reading buf is %dB\n", shm_len, *len);
        printf(" |  This will read all shm.\n");
        n = shm_len;
    }
    else
    {
        n = *len;
    }

    memcpy(retbuf, shmbuf, n);
    *len = n;

    if (shm_len > *len)
    {
        u8_t *lastbuf = shmbuf + n;
        memcpy(shmbuf, lastbuf, shm_len - n); 
        tail = tail - *len;
    }
    else
    {
        tail = 0;
    }
    
    memcpy(ptr, &tail, SHM_TAIL);
    // printf("(after reading)Now shm is %s\n", ptr);
    shmdt(ptr);
    // printf("tail=%d\n", tail);
}

void write_shm(int shmid, u8_t* buf, size_t *buf_len)
{
    size_t tail = 0;
    u8_t *ptr;
    ptr = (u8_t *)shmat(shmid, NULL, 0);
    if (atoi((char*)ptr) == -1)
    {
        printf("conn shm failed!\n");
        return;
    }

    memcpy(&tail, ptr, SHM_TAIL);
    u8_t* shmbuf = ptr + SHM_TAIL;
    size_t shm_len = tail;
    // printf("buflen = %d, shm_len = %d\n", buf_len, shm_len);
    // int n = (SHM_SIZE - shm_len  > buf_len) ? (buf_len) : (SHM_SIZE - shm_len);
    size_t n = 0;
    if (SHM_SIZE - shm_len  > *buf_len)
    {
        n = *buf_len;
    }
    else
    {
        printf("[!] The shm only last %dB, but the writing buf is %dB\n", (SHM_SIZE - shm_len), *buf_len);
        printf(" |  This will cut the tail of writing buf!\n");
        n = SHM_SIZE - shm_len;
    }
    // printf("n=%d\n", n);
    memcpy((shmbuf + shm_len), buf, n);
    *buf_len = n;
    tail += n;
    memcpy(ptr, &tail, SHM_TAIL);
    shmdt(ptr);
    // printf("tail=%d\n", tail);
}

int create_shm()
{
    int shm_id;
    char *ptr;
    printf("creating shm....\n");
    // create shm, return shm_id(fail is -1), SHM_SIZE bytes
    shm_id = shmget(IPC_PRIVATE, SHM_SIZE+1, IPC_CREAT | 0600);
    if (shm_id < 0)
    {
        printf("create shm failed\n");
        // exit(1);
        return CREATE_FAIL; // by default, impossible -x if create succ.
    }
    else
    {
    }

    // success: return address of first byte; 
    // fail: return -1
    ptr = (char *)shmat(shm_id, NULL, 0);
    if (atoi(ptr) == -1)
    {
        printf("conn shm failed!\n");
        return CONNECT_FAIL;
    }
    size_t tail = 0;
    memcpy(ptr, &tail, SHM_TAIL);

    shmdt(ptr);

    return shm_id;
}

int test()
{
    int shm_id = create_shm();
    printf("shm_id=%d\n", shm_id);
    // destory_shm(2162703);
    // write_shm(shm_id, "\0");
    u8_t a[40];
    memcpy(a, "iotfuzz,", 8);
    size_t len = 8;
    write_shm(shm_id, a, &len);
    printf("Actual writing len=%d\n", len);
    u8_t ret[40];
    len = 5;
    read_and_pop_shm(shm_id, ret, &len);
    printf("Actual reading len=%d\n", len);
    memcpy(a, "iotfirmware.", 12);
    len = 12;
    write_shm(shm_id, a, &len);
    printf("Actual writing len=%d\n", len);
    len = 15;
    read_and_pop_shm(shm_id, ret, &len);
    printf("Actual reading len=%d\n", len);
    len = 10;
    read_and_pop_shm(shm_id, ret, &len);
    printf("Actual reading len=%d\n", len);
    memcpy(a, "helle world. nju seg hjx..........", 34);
    len = 34;
    write_shm(shm_id, a, &len);
    printf("Actual writing len=%d\n", len);
    destory_shm(shm_id);
    return 0;
}
