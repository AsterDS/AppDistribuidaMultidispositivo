Instalacion y Requerimientos

- Docker Desktop
- Terminal

Se descarga el zip del proyecto y se extrae, abrir docker desktop
usar las terminales / usar windows powershell
indicar la ruta del proyecto usando cd "RUTA DEL PROYECTO"
ejecutar las instrucciones de abajo.

 --------------------------------------------------------------------

Construcción y ejecución

--Usando Docker Compose--

Construir todas las imágenes:
 docker-compose build
 
Iniciar el servidor:
 docker-compose up -d server

Ejecutar el cliente en otra terminal:
 docker-compose run client

Disfrutar del juego!

Al terminar, detener los contenedores:
 docker-compose down

 --------------------------------------------------------------------

--Usando comandos directos--

Construir las imágenes de forma manual:
 cd server
 docker build -t python-server

cd ../client
 docker build -t python-client

Ejecutar el servidor:
 docker run -d --rm --name python-server -p 5000:5000 python-server

Ejecutar el cliente:
 docker run -it --rm python-client
