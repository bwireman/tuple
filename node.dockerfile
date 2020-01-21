FROM python:3.6

WORKDIR /app
COPY node .
RUN make env
RUN make .uwsgi-reqs
CMD [ "make", "uwsgi" ]