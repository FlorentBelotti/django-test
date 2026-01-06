run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Migrate Django models
	python manage.py migrate

user: ## Create a super-user to access Django-admin
	python manage.py createsuperuser

populate: ## Populate data
	python manage.py create_places -n 10
	python manage.py create_buses -n 5
	python manage.py create_drivers -n 5
	python manage.py create_bus_shifts -n 10
	python manage.py create_bus_stops -n 20

clear: ## Clear database
	python manage.py flush --noinput
