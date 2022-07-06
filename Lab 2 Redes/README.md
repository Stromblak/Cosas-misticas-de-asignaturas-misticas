## Instrucciones

### Server
- Para ejecutar el server, hacer:

	- `$ python server.py`

- Luego, debe escribir el nombre de la carpeta con el archivo.

	- Por ejemplo: `Cosas`

- Despues debe crear alguna clave, ingresandola en la consola.

- Finalmente, se creara e inicializara el servidor.

### Client
- Para ejecutar el client, hacer:

	- `$ python client.py`

- Luego, debe ingresar la clave del server.

Si la clave ingresada es la correcta, podra ver algunas opciones y los archivos del server.

- Para descargar un archivo, basta con escribir el nobmre del archivo con su extension.

	- Por ejemplo: `data.txt`

- Despues de descargar el archivo, se terminara el programa.

### Cosas a tener en cuenta para que funcione bien el programa:
- Debe haber solo un servidor ejecutado, esperando conexiones.
- Luego se podra ejecutar un cliente. No se puede ejecutar otro servidor o ejecutar un cliente sin servidor.
- El archivo a enviar, puede ser binario o .txt. Si es .txt debe estar en UTF-8.
