FROM python:3.11.2-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","run.py"]

