FROM python:3.7.2-alpine3.8
LABEL maintainer="kirBMSTU"
ENV CONFIG="/etc/httpd.conf"
RUN apk update && apk upgrade && apk add bash
COPY . ./app
EXPOSE 80
WORKDIR ./app
CMD ["python3", "./serv.py"]