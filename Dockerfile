FROM alpine/helm:latest

RUN apk add --no-cache python3 py3-pip git

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV REPOSITORIES_PATH=/data
ENV API_URL=localhost:3000
ENV VALUES_PATH=/home/infra/values
ENV CODE_RUNNER_PATH=/home/infra/code-runner

VOLUME /data
VOLUME /home/infra
VOLUME /root/.kube
VOLUME /root/.helm
VOLUME /root/.config/helm
VOLUME /root/.cache/helm

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
