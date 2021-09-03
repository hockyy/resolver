build:
	sudo docker build -t hockyy/resolver:2.0.0 .
run:
	sudo docker run -d -p 9997:80 --name resolver hockyy/resolver:2.0.0
stop:
	sudo docker stop resolver
	sudo docker rm resolver
