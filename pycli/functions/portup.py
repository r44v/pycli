import socket

def portup(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
        return True
    except socket.gaierror:
        print("Could not get address")
        return False
    except socket.timeout:
        return False
    except Exception as e:
        print(type(e).__name__)