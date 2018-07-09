FROM python:3.6.5-alpine

#Tag: sieve/infra/asgard-status-collector
#Version: 0.1.0-rc1

WORKDIR /opt/app

RUN pip install -U pip \
    && pip install pipenv==2018.05.18

COPY . /opt/app

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "-m", "status_collector"]