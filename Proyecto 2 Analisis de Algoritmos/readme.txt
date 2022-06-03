El codigo se compila usando g++, no requiere ninguna opcion especial.
$ g++ *.cpp -o nombre_del_ejecutable
La clase hashPerfecto recibe un string como parametro en su constructor, 
el string debe contener solo los siguientes caracteres: A, C, T, G
En caso contrario tirara una exepcion.


Al ejecutar el ejecutable apareceran dos opciones:
1: Ingreso de archivo
2: Ingreso manual de string

Ingresar 1 en la consola conllevara a tres opciones mas:
	1: GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna
	2: t.txt
	Ingresar numero o nombre del archivo:

	Ingresar 1 abre el archivo del genoma.
	Ingresar 2 abre el archivo un t.txt (usado para testeo).
	Ingresar un nombre de archivo (ej: archivo.txt), abrira dicho archivo.

	Esta etapa elimina de los arhivos las lineas que contengan datos no 
	pertenecientes al genoma en si:
		Ej: >NZ_CCYG01000001.1 Clostridiaceae bacterium MS3, whole genome shotgun sequence

Ingresar 2 en la consola permitira ingresar un string
	Ej: AGTGTGTGACACAC

Luego se creara el HashPerfecto.
	Crear el hash para el genoma de Polynesia massiliensis demora unos 20 segundos en nuestro caso

Finalmente aparecera esto:
Ingresar 15-mer a buscar, 0 para salir

Esta etapa es un while(true) donde se pueden ingresar k-mers para buscar
si estan presentes en el genoma.
	Ej: GGGGGGGGGGGGGGG
	Ingresar un 0 termina el bucle while, lo que conlleva a la finalizacion del ejecutable.

