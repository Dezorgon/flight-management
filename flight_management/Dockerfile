FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod 755 ./entrypoint.sh

WORKDIR /app

RUN useradd -ms /bin/bash user
USER user

COPY --chown=user:user . .

ENTRYPOINT ["/entrypoint.sh"]
