FROM python:3.7-alpine
COPY src/ /app
COPY requirements.txt /
WORKDIR /app
RUN pip install -r /requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "server:app"]