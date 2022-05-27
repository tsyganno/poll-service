FROM python:3.9.5-slim

EXPOSE 8000

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl git libpq-dev gcc

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint-migrate.sh .

COPY . .

ENTRYPOINT ["/opt/entrypoint-migrate.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]