#!/usr/bin python3
# gcc shm_interface.c -fPIC -shared -o shm_interface.so
# ipcs -m
from ctypes import *
import os

class NetShmInterface():
    __is_load = False
    __so_path = None
    __shm_id_file = None

    __shm_interface = None
    __create_shm = None
    __destory_shm = None
    __read_and_pop_shm = None
    __write_shm = None

    __shmid = -1

    def __init__(self, so_path):
        self.__so_path = so_path
        if not os.path.exists(so_path):
            print("[-] please compile the shm_interface.so:")
            print("    g++ shm_interface.cpp -fPIC -shared -o shm_interface.so")
            self.__is_load = False
        else:
            print("[+] shm_interface.so is loaded!")
            self.__shm_interface = CDLL(so_path)

            self.__create_shm = self.__shm_interface.create_shm
            self.__create_shm.restype = c_int

            self.__destory_shm = self.__shm_interface.destory_shm
            self.__destory_shm.argtypes = [c_int]
            self.__destory_shm.restype = c_int

            self.__read_and_pop_shm = self.__shm_interface.read_and_pop_shm
            self.__read_and_pop_shm.argtypes = [c_int, POINTER(c_ubyte), POINTER(c_size_t)]
            # self.__read_and_pop_shm.restype = POINTER(c_ubyte)

            self.__write_shm = self.__shm_interface.write_shm
            self.__write_shm.argtypes = [c_int, POINTER(c_ubyte), POINTER(c_size_t)]

            self.__is_load = True

    def __checkVaild(self):
        ret = False
        if not self.__is_load:
            print("[-] shm_interface.so unload!")
        elif self.__shmid < 0:
            print("[-] shmid is invaild!")
        else:
            ret = True
        return ret

    def getShmId(self, shm_id_file):
        '''If file existed, read id from file, else create id and store it in file.'''
        if not self.__is_load:
            print("[-] shm_interface.so unload!")
            return

        self.__shm_id_file = shm_id_file
        if self.__shmid > 0:
            return self.__shmid
        elif not os.path.exists(shm_id_file):
            # print("[-] check /path/to/net_shm_id.txt is existed!")
            self.__shmid = self.__create_shm()
            if self.__shmid < 0:
                print("[-] create shmid failed, try again.")
                return
            with open(shm_id_file, mode='w+', encoding="utf-8") as sif:
                sif.write(str(self.__shmid))
        else:
            with open(shm_id_file, mode='r', encoding="utf-8") as sif:
                shm_id_str = sif.readlines()
                self.__shmid = int(shm_id_str[0])
        print("[+] get shm_id=%d" % self.__shmid)
        return self.__shmid

    @staticmethod
    def hexdump(c_ubyte_p, ubyte_len):
        for i in range(ubyte_len):
            if i != 0 and i % 16 == 0:
                print(end='\n')
            print(hex(c_ubyte_p[i])[2:], end=" ")
        print(end='\n')

    def writeShm(self, wri_buf, len_buf):
        # todo: check wri_buf Vaild
        if not self.__checkVaild():
            return

        retlen = pointer(c_size_t(len_buf))
        self.__write_shm(self.__shmid, wri_buf, retlen)
        print("Actual writing len=%d" % retlen.contents.value)
        self.hexdump(wri_buf, retlen.contents.value)
        return retlen.contents.value

    def readShm(self, len_buf):
        if not self.__checkVaild():
            return
        retbuf = (c_ubyte * len_buf)()
        retlen = pointer(c_size_t(len_buf))
        self.__read_and_pop_shm(self.__shmid, cast(retbuf, POINTER(c_ubyte)), retlen)
        print("Actual reading len=%d" % retlen.contents.value)
        self.hexdump(retbuf, retlen.contents.value)
        return retbuf, retlen.contents.value

    def freeShm(self, shmid=None):
        if not self.__is_load:
            print("[-] shm_interface.so unload!")
            return

        if shmid is None:
            os.remove(self.__shm_id_file)
            self.__destory_shm(self.__shmid)
            print("[-] free shm_id=%d" % self.__shmid)
        else:
            self.__destory_shm(shmid)
            print("[-] free shm_id=%d" % shmid)

if __name__ == "__main__":
    # use example:
    # first: import this file:
    # from shm_interface import *

    # first: init object
    nsi = NetShmInterface(r"/path/to/shm_interface.so")
    nsi.getShmId(r"/path/to/shm_id.txt")

    # second: use it
    write_len = 10
    write_buf = (c_ubyte * write_len) ()
    for i in range(write_len):
        write_buf[i] = c_ubyte(100-i)
    write_len = nsi.writeShm(write_buf, write_len) # return actual writing len

    read_buf, read_len = nsi.readShm(5) # return actual reading buf and len

    write_len = 12
    write_buf = (c_ubyte * write_len) ()
    for i in range(write_len):
        write_buf[i] = c_ubyte(512+i)
    write_len = nsi.writeShm(write_buf, write_len) # return actual writing len

    read_buf, read_len = nsi.readShm(15) # return actual reading buf and len
    read_buf, read_len = nsi.readShm(10) # return actual reading buf and len

    s = "helle world. nju cs seg.........."
    write_len = len(s)
    write_buf = (c_ubyte * write_len) ()
    for i in range(write_len):
        write_buf[i] = c_ubyte(ord(s[i]))
    write_len = nsi.writeShm(write_buf, write_len) # return actual writing len
    nsi.freeShm() # will delete the id file
