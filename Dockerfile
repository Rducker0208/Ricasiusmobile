# syntax=docker/dockerfile:1

FROM python:3.11.8
WORKDIR /app
COPY --chmod=0755 . .
RUN pip install --upgrade buildozer Cython==0.29.33 virtualenv
RUN apt update -y && apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
RUN snap install gh
CMD ["bash", "./Scripts/apk_builder.sh"]
