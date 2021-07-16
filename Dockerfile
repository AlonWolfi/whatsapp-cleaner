FROM python:3
# LABEL maintainer "Alon Wolf <alonwolfy@gmail.com>"
COPY ./src ./src
COPY ./drivers ./drivers
COPY requirements.txt /
RUN pip install -r /requirements.txt
EXPOSE 8050
CMD ["python", "./app.py"]