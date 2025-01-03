import socket
import sys
from allfiles.ip import ip,port


while True:

    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((ip,port))
        s.listen()

        import mysql.connector

        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="deens123"
        )
        mycursor = mydb.cursor()
        mycursor.execute('use project')
        print('ok')

        while True:
            clientsocket,address=s.accept()
            print(f"connection from {address} has been established!")
            #clientsocket.send('hi from server'.encode())
            while True:
                clientmsg = clientsocket.recv(10002400)
                print(clientmsg)
                import time
                mycursor.execute(clientmsg.decode())
                if 'select' not in clientmsg.decode():
                    mydb.commit()
                    clientsocket.close()
                    break
                elif clientmsg.decode() == '':
                    clientsocket.close()
                else:
                    out = mycursor.fetchall()
                    string = ''

                    if out != []:
                        for i in out:
                            string += str(i) + ";"
                            print(string)
                        clientsocket.send(string.encode())

                    else:
                        i = ('',)
                        string = str(i)+';'
                        print(string)
                        clientsocket.send(string.encode())

                    if not clientmsg:
                        print(f'Client disconnected: {address}')
                        clientsocket.close()
                        break

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="deens123"
            )

            mycursor = mydb.cursor()
            mycursor.execute('use project')

    except Exception as e:
        print('\n\nERROR :',e,'\n\n')




        
