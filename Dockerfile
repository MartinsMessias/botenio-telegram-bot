FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

ENV FROM_EMAIL ${FROM_EMAIL}
ENV FROM_PWD ${FROM_PWD}
ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV TWITTER_TOKEN ${TWITTER_TOKEN}
ENV SHODAN_API_KEY ${SHODAN_API_KEY}
ENV ADMIN_CHAT_ID ${ADMIN_CHAT_ID}

RUN mkdir /service
WORKDIR /service
COPY . /service

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]