## Estructura de la API

Este código provee las siguientes clases:

- `RUDPServer(port)`: crea un servidor UDP fiable en el puerto `port`.
    - `receive()`: Espera a recibir un mensaje de algún cliente, retornando su contenido y su dirección de origen.
    - `reply(address, payload)`: Envía `payload` al cliente en `address`.
- `RUDPClient(address, port)`: crea un cliente UDP fiable que se conecta al servidor en `address`:`port`.
    - `send_recv(payload)`: Envía `payload` al servidor y reintenta un determinado número de veces hasta obtener una respuesta

Les recomiendo mirar los ejemplos en `server.py` y `client.py` para entender cómo utilizar estas clases.
