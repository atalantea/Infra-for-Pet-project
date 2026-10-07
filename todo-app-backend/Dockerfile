FROM python:3.15.0rc2 AS builder

COPY requirements.txt /tmp/requirements.txt

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

FROM python:3.15.0rc2

RUN useradd --create-home appuser
WORKDIR /home/appuser/app

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.pet-project:app", "--host", "0.0.0.0", "--port", "8000"]