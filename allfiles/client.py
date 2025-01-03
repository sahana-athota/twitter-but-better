import socket
from ip import ip,port

def returntables():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    while True:
        msg = s.recv(10024)
        text = msg.decode().split('\n')
        if len(text) == 4:
            user_info = text[0]
            post_info = text[0]
            tagmanagement = text[0]
        
            return user_info,post_info,tagmanagement

def sqlquery(data):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    s.send(data.encode())
    
    while True:
        msg = s.recv(10000000)
        output = msg.decode().split(';')
        import time
        time.sleep(0.001)
        break
    s.close()
    return output
    import time
    time.sleep(0.01)
        
    
   

        
