FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN opentelemetry-bootstrap -a install

EXPOSE 8000

# CMD [ "export", "OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true", "opentelemetry-instrument", "--logs_exporter" ]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
