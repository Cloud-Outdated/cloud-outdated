start:
	docker-compose up -d

stop:
	docker-compose stop django
	docker-compose stop postgres

rebuild:
	docker-compose up -d --no-deps --build postgres
	docker-compose up -d --no-deps --build django

destroy:
	docker-compose down --volumes
