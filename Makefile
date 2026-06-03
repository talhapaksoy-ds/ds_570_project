IMAGE_NAME=ds570-house-price-dashboard
PORT=8501

.PHONY: install preprocess train run docker-build docker-run clean

install:
	pip install -r requirements.txt

preprocess:
	python src/data/preprocess.py

train:
	python src/models/train.py

run:
	streamlit run app/streamlit_app.py

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --rm -p $(PORT):8501 $(IMAGE_NAME)

clean:
	rm -f models/*.joblib reports/*.json reports/*.csv
