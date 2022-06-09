import socket
import encriptacion as enc


def server(host, port, modo):
    print("Servidor inicializado")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind socket, con la direccion y el puerto, luego un listen
            s.bind((host, port
            s.listen()
        except socket.error:
            print("Error en la creacion del servidor")
            print("Cerrando servidor")
            return
        print("Esperando conexiones")
        
        while True:
            # no creo que sea necesario un try aca
            clientsocket, address = s.accept()
            
            with clientsocket as c:
                print(f"Conexion entrante: {address}")
                
                # aca tampoco estoy seguro, pero prefiero dejarlo por si acaso dsadas
                try:
                    if modo == 0:
                        data = c.recv(512).decode().split("|", 3)
                    if modo == 1:
                        key = input("Ingrese la clave para descifrar: ")
                        try:
                            data = enc.decrypt_sim(c.recv(512), key).split("|", 3)
                        except:
                            print(f"Clave incorrecta, finalizando el programa.")
                            sys.exit(1)
                    if modo == 2:
                        data = enc.decrypt_asim(c.recv(512)).split("|", 3)
                except socket.error:
                    print("Error al recibir el archivo")
                    print("Cerrando servidor")
                    return

                filename = data.pop(0)
                filesize = float(data.pop(0))
                total = int(data.pop(0))
                filepath = "server\\" + filename
                recibido = len(data[0])

                print(f"Recibiendo el archivo {filename} de tamaño {filesize} MB.")
                print(f"Progreso: {round(100*recibido/total,2)}%")
                while True:
                    try:
                        buffer = c.recv(512)
                    except socket.error:
                        print(f"Error al recibir el archivo")
                        print("Cerrando servidor")
                        return
                    
                    if not buffer:
                        break
                        
                    if modo == 0:
                        bufferDec = buffer.decode()
                    if modo == 1:
                        bufferDec = enc.decrypt_sim(buffer, key)
                    if modo == 2:
                        bufferDec = enc.decrypt_asim(buffer)
                    data.append(bufferDec)
                    recibido += len(bufferDec)

                    print(f"Progreso: {round(100*recibido/total,2)}%")

                with open(filepath, "w") as r:
                    r.write(''.join(data))

                print(f"Conexion finalizada\n")
