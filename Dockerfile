FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV LISTEN_PORT 5003

EXPOSE 5003

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN python -m nltk.downloader punkt

COPY . /app