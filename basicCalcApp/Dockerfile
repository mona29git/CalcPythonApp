FROM python:3.8-slim-buster
ADD . /code
WORKDIR /code
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
