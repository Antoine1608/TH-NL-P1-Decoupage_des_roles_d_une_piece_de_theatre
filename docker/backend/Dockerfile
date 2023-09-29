FROM python:3.9-slim

RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /code

#EXPOSE 8000

#CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=80"]
#CMD ["python", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]