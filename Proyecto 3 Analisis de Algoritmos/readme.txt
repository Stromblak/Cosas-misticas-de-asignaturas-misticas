AproxVertexCover.cpp consiste en el algortitmo 2-aproximado de vertex-cover
Usa una lista de adyacencia y al elegir una arista, se eliminan las listas de adyacencias
de los dos vertices.

Usar g++ para compilar AproxVertexCover.cpp

El input consiste en una linea conteniendo la cantidad de vertices 
seguido de la cantidad de aristas Ej: 3 2
Eso serian 3 vertices y 2 aristas

Luego vienen las cantidad de aristas ingresadas. En el ejemplo anterior
serian 2.
Ej:
1 2
2 3
Hay una arista en entre el vertice 1 y 2
Hay una arista en entre el vertice 2 y 3

Se retornan los vertices elegidos por el algoritmo 2-aproximado 
de vertex cover.