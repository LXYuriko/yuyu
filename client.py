#!/Python27/
#encoding:utf-8
import socket,os,struct
BUFSIZE=65535
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.93.135',9999))
def main():
	#循环执行
	while True:
		msg=input("请选择发送信息类型：1.字符/字符串 2.文件：\n")
		if not msg or msg == "exit":
			break
		client.send(msg.encode("utf-8"))
		if msg == '1':
			data=input("请输入要发送的字符/字符串：")
			if not data:
				break
			client.send(data.encode("utf-8"))
		if msg == '2':
			filepath=input("请输入要发送的文件路径：\r\n")
			if os.path.isfile(filepath):
				#封包的编码方式
				fileinfo_size=struct.calcsize('136si')
				#将传递方式，文件名和文件大小封包在fhead中
				fhead=struct.pack('136si',os.path.basename(filepath).encode("utf-8"),os.stat(filepath).st_size)
				client.send(fhead)
				c=input("选择是否指定路径：1.指定 2.不指定：\n")
				if not c :
					break
				client.send(c.encode("utf-8"))
				if c == '1':
					path=input("请输入要发送的文件到达路径：\r\n")
					client.send(path.encode("utf-8"))
				fo=open(filepath,'rb')
				print ("read")
				while True:
					filedata=fo.read(1024)
					if not filedata:
						break
					client.send(filedata)
				fo.close()
				print ("over")
		#收到来自server端的回复信息类型
		data1=client.recv(1).decode("utf-8")
		if not data1:
			break
		#回复信息为字符串
		if data1 == '1':
			msg=client.recv(BUFSIZE)
			if not msg:
				break
			print (msg.decode("utf-8"))
		#回复信息为文件
		if data1 == '2':
				fileinfo_size=struct.calcsize('136si')
				buf=client.recv(fileinfo_size)
				if buf:
					#解包
					filename,filesize=struct.unpack('136si',buf)
					#将文件名从字节型转为str型
					filename=filename.decode("utf-8")
					filename_f=filename.strip('\00')
					#收到来自server端是否指定文件下载路径的判断数
					c=client.recv(1).decode("utf-8")
					#指定路径，接收路径
					if c == '1':
						path1=client.recv(1024)
					#不指定路径
					if c == '2':
						path1='D:\\cn\ks\\'
					#重新设置文件下载路径，在文件名前new_
					filenewname=os.path.join(path1,'new_'+filename_f)
					print(filenewname)
					recvd_size=0
					#将收到的文件内容循环写入新的文件中，知道写入文件的大小等于文件本身大小
					wf = open(filenewname,'wb')
					print("write")
					while not recvd_size==filesize:
						if filesize - recvd_size>1024:
							rdata=client.recv(1024)
							recvd_size+=len(rdata)
						else:
							rdata = client.recv(filesize-recvd_size)
							recvd_size = filesize
						wf.write(rdata)
					wf.close()
					print("over")
	#断开连接
	client.close()
main()
