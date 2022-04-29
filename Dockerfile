FROM python:3.9.5-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
EXPOSE 80
CMD [ "python3", "-m" , "app", "run", "--host=0.0.0.0"]