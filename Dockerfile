FROM python:3.13-slim

RUN pip install uv

RUN useradd --create-home --shell /bin/bash bot

WORKDIR /app
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --no-install-project
RUN chown bot:bot /app

USER bot
COPY . .

CMD ["uv", "run", "main.py"]