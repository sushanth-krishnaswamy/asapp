
Client/server multi user chatroom backend.


* This app is a simple multi client chat/chatroom app built using Python. 

* The app uses a sever-client RSA key based authentication. 

* There is no need to generate separate key files. At startup, the keypair generation happens dynamically (4096 bytes long), and are exchanged when connected. 

Libraries required : pycrypto 

Steps for installation and running:

	1. git clone https://github.com/sushanth-krishnaswamy/asapp.git

	2. pip install -r REQUIREMENTS.txt

	3. cd chat_system

	4. For server starting, the synatax used is: 

		sudo python server.py <listening_ip> <listening_port>  

		example : sudo python server.py 127.0.0.1 128

	5. For Client 1, or user 1, the syntax is:

		sudo python cient.py <username> <server's ip> <server's port>

		example: sudo python client.py Sushanth 127.0.0.1 128

	6. Repeat the process 5 for the second user. 

	7. Communicate between the two clients after they are connected.

	8. As of now, the database part to store message history is not yet been implemented. will do so in the future. 

	9. The messages between the two clients (users) are digitally signed. ( can be verified by using wireshark to intercept the messages).

	10. Ctrl/Cmd + C to disconnect the chat. 

