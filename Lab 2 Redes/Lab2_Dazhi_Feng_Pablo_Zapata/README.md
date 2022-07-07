# Instrucciones

## Server
- Para ejecutar el server, hacer:

	- `$ python server.py`

- Luego, debe escribir el nombre de la carpeta con los archivos que se compartirán.

	- Por ejemplo: `Cosas`

- Después debe crear alguna clave, ingresándola en la consola.

- Finalmente, se creará e inicializara el servidor.

## Client
- Para ejecutar el client, hacer:

	- `$ python client.py`

- Luego, debe ingresar la clave del server.

Si la clave ingresada es la correcta, podrá ver algunas opciones y los archivos del server.

- Para descargar un archivo, basta con escribir el nombre del archivo con su extensión.

	- Por ejemplo: `data.txt`

- Después de descargar el archivo, se terminará el programa.

## Cosas a tener en cuenta para que funcione bien el programa:
- Debe haber solo un servidor ejecutado, esperando conexiones.
- Luego se podrá ejecutar un cliente. No se puede ejecutar otro servidor o ejecutar un cliente sin servidor.
- El archivo a enviar, puede ser binario o .txt. Si es .txt debe estar en UTF-8.
