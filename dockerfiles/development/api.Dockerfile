FROM python:3.7.5

WORKDIR /usr/ETrader/

EXPOSE 5000

COPY ./requirements.txt .
COPY ./app.py .
COPY ./src ./src

RUN pip install -r ./requirements.txt

# to keep container running forever as 
# long as this process is not
# terminated
CMD /bin/bash
