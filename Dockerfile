FROM python:alpine

USER root

RUN pip install uv

WORKDIR /python-app
COPY ./app ./app
COPY uv.lock .
COPY pyproject.toml .

RUN addgroup -S nonpriv && adduser -S nonpriv -G nonpriv
RUN mkdir -p /home/nonpriv
RUN chown nonpriv:nonpriv /home/nonpriv

RUN chown -R nonpriv:nonpriv /python-app && chmod -R 775 /python-app

USER nonpriv

RUN uv venv
RUN uv sync

WORKDIR /python-app/app

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
