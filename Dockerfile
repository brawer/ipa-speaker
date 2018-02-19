FROM debian:buster
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-install-suggests \
  espeak-ng \
  python3 python3-pip python3-setuptools
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

STOPSIGNAL SIGTERM
EXPOSE 80
CMD ["python3", "./ipa_speaker.py", "--port=80"]

