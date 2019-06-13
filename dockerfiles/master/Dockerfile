FROM kennethreitz/pipenv

COPY . /app

EXPOSE 8089

ARG HOST
ENV HOST=$HOST

CMD locust --host=$HOST --master