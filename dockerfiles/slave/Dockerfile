FROM kennethreitz/pipenv

COPY . /app

EXPOSE 8089

CMD locust --slave --master-host=$MASTER_HOST