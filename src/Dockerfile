FROM mcr.microsoft.com/playwright/python:v1.54.0-noble AS configure-deps

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip poetry
RUN export PATH="$HOME/.local/bin:$PATH"
RUN poetry install --only=main --no-interaction

FROM configure-deps AS configure-playwright

RUN poetry run playwright install

FROM configure-playwright AS app

COPY . .

CMD ["poetry", "run", "python", "main.py"]