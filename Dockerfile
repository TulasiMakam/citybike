FROM python:3.11
COPY client.py /
COPY requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "-u", "client.py" ]