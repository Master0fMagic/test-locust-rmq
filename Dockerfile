FROM python:3.7-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8089
COPY . .
CMD ["locust"]