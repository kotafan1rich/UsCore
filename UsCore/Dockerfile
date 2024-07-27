FROM python:3.9

RUN mkdir "app"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
RUN chmod -R 755 static


ENTRYPOINT ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--reload"]