FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV LISTEN_PORT 5004

EXPOSE 5004

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]
COPY . /app