#---	Variables	---#
IMAGE_NAME		= energy-api
CONTAINER_NAME	= energy-app
PORT			= 5000

#---	Build the Docker image	---#
build:
	docker-compose build

#---	Run the Docker container	---#
run: build
	docker-compose up --build

#---	Stop the container	---#
stop:
	docker-compose down

#---	Clean up (remove image and stopped containers)	---#
clean: stop
	docker-compose down --rmi all --volumes --remove-orphans

#---	Rebuild and restart the container	---#
restart: clean run

.PHONY: build run stop clean restart