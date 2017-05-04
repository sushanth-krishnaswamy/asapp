import os
import select
import socket
import sys
import signal
from time import sleep


from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA

from communication import send,recieve

class Server_Chat(object):
	
	def __init__(self,address='127.0.0.1', port= 3490):
		self.client = 0

		self.clientmap = {}

		self.outputs = []

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((address, int(port)))

        print "Generating the RSA keys now..."
        self.server_private_key = RSA.generate(4096, os.random)
        self.server.bind((address,int(port)))

        print "Now, listening to port on port : ",port,"..."
        self.server.listen(5)

        #this is to trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)


    def sighandler(self,signum,frame):
    	#close the server --- very important to not cause data leakage

    	print "shutting down the server now ..."

    	for i in self.outputs:
    		i.close()

    	self.sever.close()


    def getname(self,client):

    	#returns the name of the user(client) 

    	info = self.clientmap[client]
    	host,name = info[0][0], info[1]

    	return '@'.join((name,host))

    def get_just_name(self,client):
    	return self.clientmap[client][1]

    def send_encrypted(self,to_who,message,name):
    	try:
    		encryptor = self.clientmap[to_who][2]
    		msg = encryptor.encrypt(message,0)
    		send(to_who,msg)

    	except IOError:
    		send(to_who,'PLAIN: cannot find public key for: %s' , %name)

    def verify_signature(self,client,message,signature):
    	try:
    		key = self.clientmap[client][2]
    		msg_hash = SHA.new()
    		msg_hash.update(message)

    		verifier = PKCS1_PSS.new(key)
    		return verifier.verofy(msg_hash,signature)

    	except IOError:
    		return False

    def serve(self):
    	inputs = [self.server, sys.stdin]
    	self.outputs = []

    	running = 1

    	while running:
    		try:
    			inputready, outputready, exceptready = select.select(inputs, self.ooutputs, [])


    		except select.error:
    			break
    		except socket.error:
    			break

    		for s in inputready:
    			if s == self.server:
    				# handle this server socket properly

    				client, address = self.server.accept()
    				print "The chat server got connection: connection %d is from %s", %(client.fileno(),address)

    				#now, getting the client's public key and send the server's public key

    				pubkey = RSA.importKey(recieve(client))
    				send(client,self.server_pubkey.exportKey())

    				#get and read the login name
    				cname = receieve(client).split('NAME: ')[1]


    				#sending the client name back to display
    				self.clients += 1
    				send(client, 'CLIENT: '+ str(address,cname,pubkey))


    				#sending this client's joining info to other people(clients)

    				msg = '\n(Connected : New client (%d) from %s)' % (self.clients, self.getname(client))

    				for i in self.outputs:
    					try:
    						self.send_encrypted(i,msg,self.get_just_name(i))

    					except socket.error:
    						self.outputs.remove(i)
    						inputs.remove(i)

    				self.outputs.append(client)

    			elif s == sys.stdin:

    				#handle standard input

    				sys.stdin.readline()
    				running = 0
    			else:

    				#handling all the other sockets
    				try:
    					data = receive(s)

    					if data:
    						dataparts = data.split('#^[[')
    						signature = dataparts[1]

    						data = dataparts[0]

    						verified = self.verify_signature(s, data, signature)
                            data = self.server_privkey.decrypt(data)

                            if data != '\x00':
                                if verified:
                                    data = '%s [OK]' % data

                                else:
                                	data = '%s [Not verified]' %data

                               	# Send as new client's message...
                                msg = '\n# [' + self.getname(s) + ']>> ' + data

                                # Send data to all except ourselves

                                for i in self.outputs:
                                    if i != s:
                                        self.send_encrypted(o, msg, self.get_just_name(s))

                        else:

                        	print 'Chatserver: Client %d hung up' % s.fileno()
                            self.clients -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from %s)' % self.getname(s)

                            for i in self.outputs:
                                self.send_encrypted(i, msg, self.get_just_name(i))


                    except socket.error:
                        # Remove
                        inputs.remove(s)
                        self.outputs.remove(s)

            
            sleep(0.5)

        self.server.close()

if __name__ == "__main__" :
	if len(sys.argv) < 3:
		sys.exit('Usage: %s listening_ip listening_port' %sys.argv[0])

	Server_Chat(sys.argv[1],sys.argv[2].serve())

	        	
