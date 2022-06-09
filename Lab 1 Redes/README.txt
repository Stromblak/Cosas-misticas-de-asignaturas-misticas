Para ejecutar el programa hacer:

	$ python main.py

Luego apareceran 2 opciones:

	1: Servidor
	2: Cliente

Debe elegir una de las 2 opciones escribiendo en el teclado.
Si elige cliente, debera escribir el nombre del archivo con su extension,
por ejemplo: data.txt

Luego para cliente y servidor, apareceran 3 opciones
	
	0: Sin cifrado
	1: Cifrado Simetrico
	2: Cifrado Asimetrico

Donde, cada mensaje representa lo que dice (sin cifrado no cifrara,
cifrado asimetrico cifrara con cifrado asimetrico, etc.). Debe elegir
una de las opciones escribiendo en el teclado.

Despues, se ejecutara el programa (cliente o servidor).

Cosas a tener en cuenta para que funcione bien el programa:

- Debe haber solo un servidor ejecutado, esperando conexiones.
- Luego se podra ejecutar un cliente. No se puede ejecutar otro servidor
  o ejecutar un cliente sin servidor.
- Las opciones que elija para el cifrado, deben ser las mismas 
  para el cliente y el servidor.
- El archivo a enviar, puede ser binario o .txt.
  Si es .txt debe estar en UTF-8.