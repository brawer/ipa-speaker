FROM debian:buster
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-install-suggests \
  espeak-ng \
  python3
COPY . .

STOPSIGNAL SIGTERM
EXPOSE 80
CMD ["python3", "./ipa_speaker.py", "--port=80"]

