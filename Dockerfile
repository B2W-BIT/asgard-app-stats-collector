FROM python:3.6.5-alpine

#Tag: sieve/infra/asgard-app-stats-collector
#Version: 0.2.1-rc1

WORKDIR /opt/app

RUN pip install -U pip \
    && pip install pipenv==2018.05.18

COPY . /opt/app

RUN apk -U add --virtual .deps gcc g++ make python-dev \
&& pipenv install --system --deploy --ignore-pipfile \
&& apk del --purge .deps

CMD ["python", "-m", "status_collector"]
