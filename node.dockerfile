FROM python:3.6

WORKDIR /app
COPY node .
RUN pip install -r requirements.txt
CMD [ "make", "serve" ]