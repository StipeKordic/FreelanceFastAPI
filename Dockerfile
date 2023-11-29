FROM python:3.9.13

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN alembic upgrade head

COPY . .

CMD  ["uvicorn", "app.main:app", "--reload", "--port", "8000"]