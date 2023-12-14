.PHONY: test

CLI=docker-compose run --rm pkg

help:	# list available targets with descriptions if they exist
	@sed -n 's/\(^[^_#[:space:].\%*][[:alnum:]]*:\)\([^#]*\)\(#.*$$\)\{0,1\}/\1 \3/ip' Makefile | column -t -s '#' | sort

update:
	touch requirements-test.txt
	docker-compose build
	docker-compose stop
	$(CLI) /bin/bash -c 'pip-compile --resolver backtracking requirements-test.in'
	docker-compose rm -f
	docker-compose build

bash:	# start a bash shell in the container
	$(CLI) /bin/bash

test:	# run tests in the container
	$(CLI) bash -c "tox"

test-watch:	# continuously run tests in the container
	$(CLI) /bin/bash -c '$(PYTEST); while inotifywait -qqre modify .; do $(PYTEST); done'

format:	# format python project code
	$(CLI) black .
	$(CLI) isort .

reset:	# destroy current local CLI containers
	docker-compose stop
	docker-compose down -v
