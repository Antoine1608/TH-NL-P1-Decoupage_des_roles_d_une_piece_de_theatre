# backend/Dockerfile

FROM python:3.9-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY  . /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "api.py"]
#CMD ["python", "streamlit", "run", "api.py"]