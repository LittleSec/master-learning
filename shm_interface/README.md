## shm_interface
1. operation(interface) of share memory(shm) for `C/C++` and `Python3`  
2. [Share Memory](https://en.wikipedia.org/wiki/Shared_memory), here just for **Linux**
    + size: defaulty 4MB, hard code in `shm_interface.c`(`#define SHM_SIZE (1 << 22)`), so you can modify it and re-compile!
    + date structure: ***queue***
3. key: use C/C++ to code the operation of shm(included create, destory, enqueue/write, dequeue/read), and compile a share object(`.so`) while Python can use `ctype` module to enjoy it.

#### [`shm_interface.c`](./shm_interface.c)
1. as the above description, compile this file to a share obj: `gcc shm_interface.c -fPIC -shared -o shm_interface.so`
2. function interfaces:
    ```c
    int destory_shm(int shmid);
    void read_and_pop_shm(int shmid, u8_t* retbuf, size_t *len);
    void write_shm(int shmid, u8_t* buf, size_t *buf_len);
    int create_shm();
    ```
3. some macro definitions
    ```c
    #define SHM_TAIL ((size_t)sizeof(size_t))
    #define SHM_SIZE (1 << 22) // 4MB the first sizeof(size_t) bytes store the tail
    typedef unsigned char u8_t;
    ```
4. *tips*: remember the shm here is a **queue**, so **write in tail, read from head**, and the tail store in the first `sizeof(size_t) bytes` of shm, so actually the size of shm is 4MB + sizeof(size_t) bytes.
5. `int test()` show an example for using above functions

#### [`shm_interface.py`](./shm_interface.py)
1. `class NetShmInterface()`, so can import this py file to use, example in `if __name__ == "__main__":` code block.
2. Before run/use shm_interface.py, please compile `shm_interface.c` to `shm_interface.so` file. And modify the `/path/to/shm_interface.so`.
3. interface in class:
    ```python
    def __init__(self, so_path)
    def getShmId(self, shm_id_file)
    def writeShm(self, wri_buf, len_buf)
    def readShm(self, len_buf)
    def freeShm(self, shmid=None)
    ```
4. in function `getShmId(shm_id_file))`, if shm_id_file exist, read shm_id from it, else crate shm and store shm_id in it.
5. corresponding ctype and python type in function `__init__()`
6. because we think the content in shm is binary, so it is not friendly in python, the interface in python(especially read and write shm) don't friendly.
7. if we think contents in shm is char, it is easier to code not only c/c++, but also in python(more friendly, too).