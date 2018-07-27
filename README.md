# Penetration Testing

### Unix Password Cracker - [click here](python3/uPwdCrack/)  
 -  python3 uPwdCrack.py -p \<passwordFile\> -d \<dictionaryFile\>
 - **Format in text file:** id: encrypted_password
 - **example:** python3 uPwdCrack.py -p pwd.txt -d dict.txt

### Zip File Password Cracker -[click here](python3/zFileCrack/) 
 - for zipCrypto based encryption
 - **example:** python3 zFileCrack.py -z file.zip -d dict.txt

### TCP (client + server) -[click here](python3/tcp/)
 - test for services , send data, etc. command shells or proxy
 - **example:** 
 			> python3 tcp_server.py  
 			> python3 tcp_client.py --host \<host\> -p \<port\> 

### UDP client -[click here](python3/udp/)
 - similar to TCP
 - **example:** python3 udp_client.py --host \<host\> -p \<port\> 

### TCP Port Scanner + banner grabbing - [click here](python3/TCP_portScanner/portScanner.py)  
 - identify hosts using TCP full connect scan
 - **example:** python3 portScanner.py --host iith.ac.in -p 21 22

### TCP proxy
 - to help understand unknown protocols, create test cases for fuzzers and modify traffic being sent to an application
 - **example:** python3 -lh \<local host\> -lp \<local port\> -rh \<remote host\> -rp \<remote port\> -r

### NMAP Scan

### Net tool

### SSH

#### Readme Yet to be updated...