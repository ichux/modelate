FORMAT="\nID\t{{.ID}}\nIMAGE\t{{.Image}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.RunningFor}}\nSTATUS\t{{.Status}}\nPORTS\t{{.Ports}}\nNAMES\t{{.Names}}\n"

help:
	make cls
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  clean           to make the work directories clean of unwanted files"
	@echo "  bash            to make bash for the docker environment"
	@echo "  logs            to make logs for the docker environment show up"
	@echo "  bde             to make build and then detach from the docker environment"
	@echo "  cls             to clear the screen"
	@echo "  down            to make the docker environment go down and clean itself up"
	@echo "  rmi             to remove the image with a specified id or id(s)"
	@echo "  tail            to tail the modelate_app container"
	@echo "  dpa             to run docker ps -a"
	@echo "  routes          displays the application's routes"
	@echo "  shell           displays the application's shell"

	@echo "  dbi             to make a development migration init"
	@echo "  dbm             to make a development migration migrate"
	@echo "  dbr             to make a development migration revision"
	@echo "  dbu_sql         to make a development migration upgrade, showing the sql"
	@echo "  dbu_no_sql      to make a development migration upgrade, not showing the sql"
	@echo "  dd              to make a development migration downgrade"
	@echo "  test            to make the unittest run"


clean:
	find . -iname '*.pyc' -delete; find . -iname '.DS_Store' -delete
	find . -name '__pycache__' -type d -print0 | xargs -0 /bin/rm -rf '{}'

bash:
	docker-compose run --rm flaskapp bash

logs:
	docker-compose logs  --timestamps --follow

bde: clean
	make cls
	docker-compose up --build -d; docker-compose logs; docker-compose ps

cls:
	printf "\033c"  # clear the screen

down:
	docker-compose down
	docker images

rmi:
    # make rmi id=4152a9608752; make rmi id="1ea5b921a459 07ee12a5eb2a"
	docker rmi $(id)
	make cls
	docker images

tail: cls
	docker logs modelate_app --timestamps --follow

dpa: cls
	docker ps -a --format $(FORMAT)

routes: cls
	docker-compose run --rm flaskapp flask routes

shell: cls
	docker-compose run --rm flaskapp flask shell

dbi: cls
	docker-compose run --rm flaskapp flask dbi

dbm: cls
	docker-compose run --rm flaskapp flask dbm

dbr: cls
	docker-compose run --rm flaskapp flask dbr

dbu_sql:
	make cls
	docker-compose run --rm flaskapp flask dbu-sql

dbu_no_sql: cls
	docker-compose run --rm flaskapp flask dbu-no-sql

dd: cls
	docker-compose run --rm flaskapp flask downgrade

tests:
	docker-compose run --rm flaskapp python -m unittest discover -s tests/