FROM python:3.12-slim

WORKDIR /lambda_benchmark

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py" ]
CMD ["--help"]
