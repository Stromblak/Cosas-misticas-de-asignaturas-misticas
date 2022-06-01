#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <bits/stdc++.h>

using namespace std;
int main() {
	const char* server_name = "localhost";
	const int server_port = 8877;

	struct sockaddr_in server_address;
	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;

	// creates binary representation of server name
	// and stores it as sin_addr
	// http://beej.us/guide/bgnet/output/html/multipage/inet_ntopman.html
	inet_pton(AF_INET, server_name, &server_address.sin_addr);

	// htons: port in network order format
	server_address.sin_port = htons(server_port);

	// open a stream socket
	int sock;
	sock = socket(PF_INET, SOCK_STREAM, 0);
	if (sock < 0) {
		printf("could not create socket\n");
		return 1;
	}

	// TCP is connection oriented, a reliable connection
	// **must** be established before any data is exchanged
	if (connect(sock, (struct sockaddr*)&server_address,
	            sizeof(server_address)) < 0) {
		printf("could not connect to server\n");
		return 1;
	}

	// send

	
	string nombre_archivo;
    	ifstream archivo;

    	cout << "nombre del archivo?" << endl;
    	cin >> nombre_archivo;

    	archivo.open(nombre_archivo.c_str());

	vector<string> text;
	string line;

	std::ifstream in(nombre_archivo.c_str());
std::string contents((std::istreambuf_iterator<char>(in)), 
    std::istreambuf_iterator<char>());

	
    	// data that will be sent to the server
	send(sock, contents.c_str(), strlen(contents.c_str()), 0);

	// receive

	int n = 0;
	int len = 0, maxlen = 10000;
	char buffer[maxlen];
	char* pbuffer = buffer;

	// will remain open until the server terminates the connection
	while ((n = recv(sock, pbuffer, maxlen, 0)) > 0) {
		pbuffer += n;
		maxlen -= n;
		len += n;

		buffer[len] = '\0';
		cout << "Recibido" << endl;
		cout << buffer << endl;
		//printf("received: '%s'\n", buffer);
	}

	// close the socket
	close(sock);
	return 0;
}
