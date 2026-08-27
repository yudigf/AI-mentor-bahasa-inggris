FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependencies definitions
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copy project source code
COPY . .
RUN uv sync --frozen

CMD ["uv", "run", "main.py"]
