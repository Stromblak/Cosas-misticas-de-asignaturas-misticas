Para ejecutar el programa, hacer:

	$ python main.py

Luego apareceran 2 opciones:

	1: Servidor
	2: Cliente

Debe elegir una de las 2 opciones escribiendo en el teclado.

Luego para cliente y servidor, apareceran 3 opciones:
	
	0: Sin encriptacion
	1: Encriptacion simetrica
	2: Encriptacion asimetrica

Donde cada mensaje representa lo que dice (Sin encriptacion no cifrara,
Encriptacion simetricacifrara con cifrado asimetrico, etc.). Debe elegir
una de las opciones escribiendo en el teclado.

Despues, se ejecutara el programa si escogio servidor. 
Si eligio cliente, debe ingresar el nombre del archivo a enviar,
con su extension, por ejemplo: data.txt

Cosas a tener en cuenta para que funcione bien el programa:

- Debe haber solo un servidor ejecutado, esperando conexiones.
- Luego se podra ejecutar un cliente. No se puede ejecutar otro servidor
  o ejecutar un cliente sin servidor.
- Las opciones que elija para el cifrado, deben ser las mismas 
  para el cliente y el servidor.
- El archivo a enviar, puede ser binario o .txt.
  Si es .txt debe estar en UTF-8.
