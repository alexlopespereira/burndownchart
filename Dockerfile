FROM tiangolo/uwsgi-nginx-flask:flask

COPY ./app /app
COPY ./users.py /app/
# copy over our requirements.txt file
COPY ./app/requirements.txt /tmp/
# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

EXPOSE 8888
CMD ["python3", "/var/www/app/burndownchart.py"]