help:
	@echo "Available commands:"
	@echo "	make test -> Run tests"
	@echo "	make ci-test -> Run tests and generate coverage file"

test:
	cd src && pipenv run scrapy check
	pipenv run pytest -v

ci-test:
	cd src && pipenv run scrapy check -v
	pipenv run coverage run --source='.' -m pytest -v
	pipenv run coverage xml -o cobertura.xml

run-spider:
	cd src && pipenv run scrapy crawl $(SPIDER)