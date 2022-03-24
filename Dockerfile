FROM alpine/helm:latest

RUN apk add --no-cache python3 py3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV INFRA_PATH=/home/infra

VOLUME /home/infra
VOLUME /root/.kube
VOLUME /root/.helm
VOLUME /root/.config/helm
VOLUME /root/.cache/helm

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
