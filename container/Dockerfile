# Generated fallback container starter. Adjust as needed.
FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app
COPY . /app
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

ENV APP_PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "app.py"]
