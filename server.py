#!/usr/bin/env python
#encoding:utf-8
import socket,time,struct,os

BUFSIZE=65535

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('',9999))
server.listen(5)
def function(connection,address):
			
	try:
		fileinfo_size=struct.calcsize('136si')
		buf=connection.recv(fileinfo_size)
		if buf:
			filename,filesize=struct.unpack('136si',buf)
			filename=filename.decode('utf-8')	
			filename_f=filename.strip('\00')
			c=connection.recv(1)
			if c == '1':
				path=connection.recv(1024)
			if c == '2':
				path='/home/yu/'	
			filenewname=os.path.join(path,'new_'+filename_f)
			print filenewname
			print "file new name is %s, filesize is %s" %(filenewname,filesize)
			recvd_size=0
			wf = open(filenewname,'wb')
			print "write"
			while not recvd_size==filesize:
				if filesize - recvd_size > 1024:
					rdata = connection.recv(1024)
					recvd_size += len(rdata)
				else:
					rdata = connection.recv(filesize- recvd_size)
					recvd_size = filesize
				wf.write(rdata)
			wf.close()
			print "over"			
	except socket.timeout:
		connection.close()	
while True:
	connection,address=server.accept()
	while True:
		data=connection.recv(1)
		if not data:
			break
		if data == '1':
			msg=connection.recv(BUFSIZE)		
			if not msg:
				break
			if msg == "exit":
				break
			print msg
		if data == '2':
			function(connection,address)
		remsg=raw_input("请选择回复信息类型：1.字符/字符串 2.文件: \n")
		if not remsg:
			break
		connection.send(remsg)
		if remsg == '1':
			data1=raw_input("请输入要回复的字符/字符串：")
			if not data1:
				break			
			connection.send(data1)
		if remsg == '2':
			filepath1=raw_input("请输入要回复的文件路径：\r\n")			
			if os.path.isfile(filepath1):
				fileinfo_size1=struct.calcsize('136si')				
				fhead1=struct.pack('136si',os.path.basename(filepath1),os.stat(filepath1).st_size)
				
				connection.send(fhead1)
				c=raw_input("选择是否指定路径：1.指定 2.不指定：\n")
				if not c:
					break
				connection.send(c)
				if c == '1':
					path1=raw_input("请输入要回复的文件到达路径：\r\n")
					connection.send(path1)
				
				fo1=open(filepath1,'rb')
				print 'read'
				while True:
					filedata=fo1.read(1024)
					if not filedata:
						break
					connection.send(filedata)
				fo1.close()
				print 'over'
		
	connection.close()
server.close()
