FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py
COPY ./src /code/src
COPY ./.env /code/.env

EXPOSE 9999:9999

CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9999"]

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9999"]
ENTRYPOINT ["tail", "-f", "/dev/null"]

