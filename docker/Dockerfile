FROM python:3.12-slim
WORKDIR /workspace
COPY requirements-dev.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
EXPOSE 5000
CMD ["sh", "docker/entrypoints/development.sh"]
