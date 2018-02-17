# IPA Speaker

Small experimental HTTP server for synthesizing strings in the
[International Phonetic Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet). Currently, it calls [eSpeak-NG](https://github.com/espeak-ng/espeak-ng) for speech synthesis.


## Build and run

```bash
$ git clone https://github.com/brawer/ipa-speaker.git ; cd ipa-speaker
$ docker build -t ipa-speaker .
$ docker run -p 8080:80 -it ipa-speaker
```

This will serve queries like [/speak?q=ʃtrɛkə&lang=de-CH](http://localhost:8080/speak?q=%CA%83tr%C9%9Bk%C9%99&lang=de-CH) from localhost on port 8080.
