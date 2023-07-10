
#.SILENT:
SHELL = /bin/bash

.PHONY: clean clean_build clean_pack clean_test clean_docker_test clean_venv test docker_test

all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"dtcd_simple_math_core_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
Addition section:\n\
 venv\n\
"

GENERATE_VERSION = $(shell cat setup.py | grep __version__ | head -n 1 | sed -re 's/[^"]+//' | sed -re 's/"//g' )
GENERATE_BRANCH = $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')
SET_VERSION = $(eval VERSION=$(GENERATE_VERSION))
SET_BRANCH = $(eval BRANCH=$(GENERATE_BRANCH))

CONDA = conda/miniconda/bin/conda

define clean_docker_containers
	@echo "Stopping and removing docker containers"
	docker-compose -f docker-compose-test.yml stop
	if [[ $$(docker ps -aq -f name=dtcd_simple_math_core) ]]; then docker rm $$(docker ps -aq -f name=dtcd_simple_math_core);  fi;
endef

pack: make_build
	$(SET_VERSION)
	$(SET_BRANCH)
	rm -f dtcd_simple_math_core-*.tar.gz
	echo Create archive \"dtcd_simple_math_core-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../dtcd_simple_math_core-$(VERSION)-$(BRANCH).tar.gz dtcd_simple_math_core

clean_pack:
	rm -f dtcd_simple_math_core-*.tar.gz


dtcd_simple_math_core.tar.gz: build
	cd make_build; tar czf ../dtcd_simple_math_core.tar.gz dtcd_simple_math_core && rm -rf ../make_build

build: make_build

make_build: venv venv.tar.gz
	# required section
	echo make_build
	mkdir make_build

	cp -R ./dtcd_simple_math_core make_build
	rm make_build/dtcd_simple_math_core/dtcd_simple_math_core.conf
	mv make_build/dtcd_simple_math_core/dtcd_simple_math_core.conf.example make_build/dtcd_simple_math_core/dtcd_simple_math_core.conf
	cp *.md make_build/dtcd_simple_math_core/
	cp *.py make_build/dtcd_simple_math_core/
	if [ -s requirements.txt ]; then \
		mkdir make_build/dtcd_simple_math_core/venv;\
		tar -xzf ./venv.tar.gz -C make_build/dtcd_simple_math_core/venv; \
	fi

conda/miniconda.sh:
	echo Download Miniconda
	mkdir -p conda
	wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O conda/miniconda.sh; \

conda/miniconda: conda/miniconda.sh
	bash conda/miniconda.sh -b -p conda/miniconda; \

clean_build:
	rm -rf make_build

venv: clean_venv conda/miniconda
	if [ -s requirements.txt ]; then \
		echo Create venv; \
		$(CONDA) create --copy -p ./venv -y; \
		$(CONDA) install -p ./venv python==3.9.7 -y; \
		./venv/bin/pip install --no-input  -r requirements.txt; \
	fi

venv.tar.gz: venv
	if [ -s requirements.txt ]; then \
		$(CONDA) pack -p ./venv -o ./venv.tar.gz; \
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







