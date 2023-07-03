FROM python:3.10-slim-bullseye

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV DEBUG=False
ENV FLASK_APP=run.py
ENV PORT=5000

CMD if [ "$DEBUG" = "True" ] ; then export FLASK_ENV=development && flask run --host=0.0.0.0 --port=$PORT --reload ; else gunicorn -b :$PORT run:app ; fi
