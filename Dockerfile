FROM python:3.10.2

WORKDIR /src

ENV PYTHONPATH "${PYTHONPATH}:/src"

COPY requirements.txt .
COPY requirements-dev.txt .
COPY requirements-all.txt .
COPY setup.cfg .

RUN pip install -r requirements-all.txt

COPY src/ src/
COPY tests/ tests/
