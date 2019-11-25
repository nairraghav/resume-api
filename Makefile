IMAGE_NAME=resume
TAG=latest

clean:
	rm -rf .pytest_cache/ .coverage

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-tag: docker-build
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(TAG)

docker-run:
	docker run -d -p 5000:5000 -e SECURE_KEY $(IMAGE_NAME):$(TAG)

docker-run-it:
	docker run -p 5000:5000 -it $(IMAGE_NAME):$(TAG) bash

test:
	python -m pytest tests/ --cov=src/

lint:
	flake8 src/ tests/

format:
	black src --line-length 79
