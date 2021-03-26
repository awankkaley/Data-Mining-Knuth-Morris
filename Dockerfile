FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV LISTEN_PORT 3000

EXPOSE 3000

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /app