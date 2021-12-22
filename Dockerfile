FROM python:3.8-alpine

RUN mkdir /flask-app
COPY PhoneBookModel.py /flask-app
COPY requirements.txt /flask-app
COPY Service.py /flask-app
WORKDIR /flask-app
RUN pip install -r requirements.txt
EXPOSE 32000
ENTRYPOINT [ "python" ]
CMD [ "Service.py" ]