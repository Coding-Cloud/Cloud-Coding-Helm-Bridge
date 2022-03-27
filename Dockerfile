FROM alpine/helm:latest

RUN apk add --no-cache python3 py3-pip git

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV INFRA_PATH=/home/infra
ENV REPOSITORIES_PATH=/data
ENV API_URL=localhost:3000

VOLUME /home/infra
VOLUME /root/.kube
VOLUME /root/.helm
VOLUME /root/.config/helm
VOLUME /root/.cache/helm

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
