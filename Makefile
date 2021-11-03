start:
	docker-compose up -d

stop:
	docker-compose stop django
	docker-compose stop cockroach

rebuild:
	docker-compose up -d --no-deps --build cockroach
	docker-compose up -d --no-deps --build django

destroy:
	docker-compose down --volumes
