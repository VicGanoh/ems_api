FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="vicgan.io"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=web
ENV APP_PORT=9000

USER root

RUN touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME [ "/vol/web/static" ]

USER nginx

CMD [ "/run.sh" ]