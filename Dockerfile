FROM python:3.8.6-alpine3.12

ENV PYTHONUNBUFFERED=0

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apk add --no-cache net-snmp-dev python3-dev
# ==============================================================================
RUN mkdir -p /src/restful_snmp_api
ADD restful_snmp_api /src

# ==============================================================================
# 파일 복사

ADD . /src
WORKDIR /src

# ==============================================================================
# 설치
RUN python setup.py install

# ==============================================================================
# 설치파일 정리
WORKDIR /root
RUN rm -rf /src
RUN apk del .build-deps

# =============================================================================
# 로그파일 위치 생성
RUN mkdir -p /var/log/app

EXPOSE 5000

ENTRYPOINT ["restful-snmp-api"]
