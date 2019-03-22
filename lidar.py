import sys,getopt,time
import serial 
import queue
#from queue import Queue
import socket
import signal
import json
import threading
import binascii
#BaudRate 230400
ldread = True
lddata = queue.Queue()
#sockfs=None
#serip='127.0.0.1'
#serport = 80

def tcpcli(serip,serport):
    print(serip,serport)
    try:
        sockfs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfs.connect((serip,int(serport)))
    except socket.error as msg:
        print(msg)
        sockfs.close() 
    return sockfs

def senddata(serip,serport,lddata):
    print('senddata')
    sockfd=tcpcli(serip,serport)
    while(True):
        try:
            datatmp = lddata.get(timeout=5.0)
            print(sockfd.send((json.dumps(datatmp)).encode('utf-8')))
        except queue.Empty:
            continue
        except socket.error as msg:
            print(msg)
            sockfs.close()
            sockfd=tcpcli(serip,serport)
            continue
    sockfs.close()


def openser(device,lddata):
    print('openser')
    datalist=[]
    datadict={}
    ldser=serial.Serial(device, 230400, timeout=1)
    ldser.write(b'b')
    i=0
    #for i in range(0,60):
    while(True):
        if ldread:
            sync=ldser.read(1)
            #print(binascii.b2a_hex(sync))
            if sync and sync[0]==0xfa: #找到数据头
                distlist=[]
                ldtmp=ldser.read(41)
                degree=(ldtmp[0]-0xa0)*6
                for i in range(0,6):
                    distdict={}
                    print("degree:%d,dist:%d"%(degree+i,ldtmp[6+6*i]*0xff+ldtmp[5+6*i]))
                    distdict["degree"]=degree+i
                    distdict["dist"]=ldtmp[6+6*i]*0xff+ldtmp[5+6*i]
                    distlist.append(distdict)
                datadict['data']=distlist
                #print(datadict)
                lddata.put(datadict)
                #sockfd.send((json.dumps(datadict)).encode('utf-8'))

                
            else:
                i=i+1
                if i>60:
                    print("can't find sync,drop data",sync,type(sync))
                    #lddata.put(i)
                    i=0
        else:
            ldser.write(b'e')
    ldser.close()
    #lddata.put("1")

def usage():
    print("lider 1.0.0 - (C) 2019 Question\n\n-d device\n-h hostnma\n-p tcp port\n")

def main():
    serip='127.0.0.1'
    serport=80
    device=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-d:-h:-p:",["help","version"])
        for op, value in opts:
            if op == "-d":
                device = value
            elif op == "-h":
                #hostname = value
                serip=value
            elif op == "-p":
                serport = value
    except getopt.GetoptError:
        usage()
        sys.exit()
    threads = []
    t1 = threading.Thread(target=openser,args=(device,lddata))
    threads.append(t1)
    #t2 = threading.Thread(target=senddata,args=(serip,serport,lddata))
    #threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    #time.sleep(10)
    #sockfd=tcpcli(serip,serport)
    #openser(sockfd,device)   
    print("serial:%s,hostname:%s,tcp port:%s"%(device,serip,serport))
    #lddata.get()

if __name__ == '__main__':
  main()
