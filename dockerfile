FROM python:3.7.2-alpine3.8
LABEL maintainer="kirBMSTU"
ENV DOCUMENT_ROOT="/var/www/html"
ENV CONFIG="/etc/httpd.conf"
RUN apk update && apk upgrade && apk add bash
COPY . ./app
EXPOSE 8080
WORKDIR ./app
CMD ["python3", "./serv.py"]