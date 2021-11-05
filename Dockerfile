FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD main.py /app/
ADD requirements.txt /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["ddtrace-run", "python", "/app/main.py"]
