# Basic ML REST APIs

Framework to create basic REST APIs for ML predictions. REST APIs are created using `FastAP` python package

FastAPI is way faster than flask & django

## Setup

```
pip install -r requirements.txt
```

Download  `en_core_web_sm` model from `spacy` to get the feature sentiment

```bash
python3 -m spacy download en_core_web_sm
```

## Run Server

```
python main.py
```

## Swagger APIs

http://localhost:8000/docs
