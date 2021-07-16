FROM bitnami/python:3
# LABEL maintainer "Alon Wolf <alonwolfy@gmail.com>"
COPY ./src ./src
COPY ./drivers ./drivers
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt install -y firefox
# RUN Y
EXPOSE 8050
CMD ["python", "src/app.py"]
