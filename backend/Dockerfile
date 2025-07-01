FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# Install UV for fast Python deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy and install dependencies
COPY requirements.txt .
RUN uv pip install -r requirements.txt --system

# Copy the Django project
COPY . .

EXPOSE 8000

# CMD ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#
# FROM python:3.13.5-slim-bookworm
#
# ENV PYTHONDONTWRITEBYTECODE=1 \
# PYTHONUNBUFFERED=1
#
# WORKDIR /app
#
# RUN apt-get update && apt-get install -y curl
#
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
#
# COPY backend/requirements.txt .
# RUN uv pip install -r requirements.txt --system
#
# COPY backend/ .
#
# EXPOSE 8000
#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#
