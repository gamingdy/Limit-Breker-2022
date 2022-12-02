FROM python:3.10-slim
WORKDIR /app
COPY ./src/ /app
RUN apt update
RUN apt upgrade -y
RUN pip install -r requirements.txt
CMD ["python", "main.py"]