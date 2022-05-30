FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000