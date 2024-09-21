# syntax=docker/dockerfile:1

FROM python:3.11.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
 
