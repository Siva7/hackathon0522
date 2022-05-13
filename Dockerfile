FROM python:3.7
WORKDIR /root/hackathon0522
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pwd
COPY . .
RUN ls -ltr
ENTRYPOINT ["python","Executor.py"]