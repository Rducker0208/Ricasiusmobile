# syntax=docker/dockerfile:1

FROM python:3.11.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt update -y && apt install openjdk-17-jdk xorg -y
CMD ["python", "main.py"]
 
