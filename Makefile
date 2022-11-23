.PHONY: deploy docker elasticsearch

env.activate:
	conda activate tensorflow

elasticsearch:
	screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
	sysctl -w vm.max_map_count=262144
deploy: deploy.clean deploy.mkdir deploy.access docker.download_docker_file docker.compose.up
deploy.clean:
	sudo rm -R /opt/clearml/
deploy.mkdir:
	sudo mkdir -p /opt/clearml/data/elastic_7
	sudo mkdir -p /opt/clearml/data/mongo_4/db
	sudo mkdir -p /opt/clearml/data/mongo_4/configdb
	sudo mkdir -p /opt/clearml/data/redis
	sudo mkdir -p /opt/clearml/logs
	sudo mkdir -p /opt/clearml/config
	sudo mkdir -p /opt/clearml/data/fileserver
deploy.access:
	sudo chown -R $(shell whoami):staff /opt/clearml

docker.restart: docker.compose.down docker.compose.up
docker.download_docker_file:
	sudo curl https://raw.githubusercontent.com/allegroai/clearml-server/master/docker/docker-compose.yml -o /opt/clearml/docker-compose.yml
docker.compose.up:
	docker-compose -f /opt/clearml/docker-compose.yml up -d
docker.compose.down:
	docker-compose -f /opt/clearml/docker-compose.yml down
