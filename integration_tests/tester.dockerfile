FROM python:3

WORKDIR /app
COPY test_integration.py .

RUN pip install pytest requests
CMD [ "pytest" , "-v"]