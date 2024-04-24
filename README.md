## Set Up

1. Clone the forked repository and proceed with the steps mentioned below:
```
git clone https://github.com/NayashaPrakash/fyle-interview-intern-backend.git
```
Move to your project directory to proceed with the following steps.

2. Run the docker container.
```
docker-compose build
docker-compose up
```
3. List the running containers by the following command.
```
docker ps
```
You can check the container name under NAMES column here.

4. Start the bash shell.
```
docker exec -it <container_name> bash
```
5. Set up database.

```
make db
```
6. Start the server.

```
make server
```
7. Run the following command to run tests and get test coverage report. 

```
make test
```
