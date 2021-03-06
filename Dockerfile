FROM python:3.8-alpine
WORKDIR /usr/src/app
COPY . .
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]