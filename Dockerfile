FROM python:3.13-slim-buster 

LABEL name="insignia-app" version="1.0"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.pesentation.api.main:app", "--reload"]