
#.SILENT:
SHELL = /bin/bash

.PHONY: clean clean_build clean_pack clean_test clean_docker_test clean_venv test docker_test

all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"DataCAD_simple_math_core_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
Addition section:\n\
 venv\n\
"

GENERATE_VERSION = $(shell cat setup.py | grep __version__ | head -n 1 | sed -re 's/[^"]+//' | sed -re 's/"//g' )
GENERATE_BRANCH = $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')
SET_VERSION = $(eval VERSION=$(GENERATE_VERSION))
SET_BRANCH = $(eval BRANCH=$(GENERATE_BRANCH))

define clean_docker_containers
	@echo "Stopping and removing docker containers"
	docker-compose -f docker-compose-test.yml stop
	if [[ $$(docker ps -aq -f name=DataCAD_simple_math_core) ]]; then docker rm $$(docker ps -aq -f name=DataCAD_simple_math_core);  fi;
endef

pack: make_build
	$(SET_VERSION)
	$(SET_BRANCH)
	rm -f DataCAD_simple_math_core-*.tar.gz
	echo Create archive \"DataCAD_simple_math_core-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../DataCAD_simple_math_core-$(VERSION)-$(BRANCH).tar.gz DataCAD_simple_math_core

clean_pack:
	rm -f DataCAD_simple_math_core-*.tar.gz


DataCAD_simple_math_core.tar.gz: build
	cd make_build; tar czf ../DataCAD_simple_math_core.tar.gz DataCAD_simple_math_core && rm -rf ../make_build

build: make_build

make_build: venv venv.tar.gz
	# required section
	echo make_build
	mkdir make_build

	cp -R ./DataCAD_simple_math_core make_build
	rm make_build/DataCAD_simple_math_core/DataCAD_simple_math_core.conf
	mv make_build/DataCAD_simple_math_core/DataCAD_simple_math_core.conf.example make_build/DataCAD_simple_math_core/DataCAD_simple_math_core.conf
	cp *.md make_build/DataCAD_simple_math_core/
	cp *.py make_build/DataCAD_simple_math_core/
	if [ -s requirements.txt ]; then \
		mkdir make_build/DataCAD_simple_math_core/venv;\
		tar -xzf ./venv.tar.gz -C make_build/DataCAD_simple_math_core/venv; \
	fi

clean_build:
	rm -rf make_build

venv:
	if [ -s requirements.txt ]; then \
		echo Create venv; \
		conda create --copy -p ./venv -y; \
		conda install -p ./venv python==3.9.7 -y; \
		./venv/bin/pip install --no-input  -r requirements.txt; \
	fi

venv.tar.gz: venv
	if [ -s requirements.txt ]; then \
		conda pack -p ./venv -o ./venv.tar.gz; \
	fi

clean_venv:
	rm -rf venv
	rm -f ./venv.tar.gz


clean: clean_build clean_venv clean_pack clean_test

test: docker_test

logs:
	mkdir -p ./logs

docker_test: logs
	$(call clean_docker_containers)
	@echo "Testing..."
	CURRENT_UID=$$(id -u):$$(id -g) docker-compose -f docker-compose-test.yml run --rm  complex_rest python ./complex_rest/manage.py test ./tests --settings=core.settings.test --no-input
	$(call clean_docker_containers)

clean_docker_test:
	$(call clean_docker_containers)

clean_test: clean_docker_test







