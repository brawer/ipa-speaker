#!/usr/bin/env python
# Server that calls eSpeak to synthesize IPA strings for /speak?q=ipa&lang=en
# SPDX-License-Identifier: MIT


from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import subprocess
import unicodedata
import urllib


class IPASpeaker(BaseHTTPRequestHandler):
    def speak(self, request, query):
        q = query.get('q')
        lang = query.get('lang')
        if not q or not lang or len(q) != 1 or len(lang) != 1:
            self.reply_bad_request()
            return
        q = q[0].strip()
        lang = lang[0].strip().replace('_', '-')
        if not re.match(r'^[a-zA-Z0-9\-]+$', lang):
            lang = 'de'
        global ipa_mapper, espeak_binary
        kirshenbaum = ipa_mapper.espeak(q)
        audio = subprocess.check_output(
            [espeak_binary, '-v' + lang, '[[%s]]' % kirshenbaum, '--stdout'])
        self.reply(audio, content_type='audio/x-wav', status=200)

    def do_GET(self):
        req = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(req.query)
        if req.path == '/speak':
            self.speak(req, query)
        else:
            self.reply(b'404 Not Found\n', status=404,
                       content_type='text/plain')

    def do_HEAD(self):
        self.do_GET()

    def reply_bad_request(self):
        self.reply(b'400 Bad Request\n', status=400,
                   content_type='text/plain')

    def reply(self, content, status=200, content_type='text/html', headers={}):
        self.send_response(status)
        self.send_header('Server', 'SpeakIPA/0.1')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Content-Type', content_type)
        for key, value in sorted(headers.items()):
            self.send_header(key, value)
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)


class IPAMapper(object):
    def __init__(self, config_path):
        self.mapping = self._read_ipa_to_espeak_mapping(config_path)
        syms = '|'.join(sorted(self.mapping.keys(), key=len, reverse=True))
        self.regexp = re.compile(syms + '|.')

    def espeak(self, ipa):
        return self.regexp.sub(lambda x: self.mapping.get(x.group(0), '?'),
                               ipa)

    def _read_ipa_to_espeak_mapping(self, config_path):
        result = {'.': ' '}
        for line in open('ipa_to_espeak.txt', encoding='utf-8'):
            line = line.split('#')[0].strip()
            line = unicodedata.normalize('NFC', line)
            if line:
                ipa, espeak = [s.strip() for s in line.split('\t')]
                assert ipa == ipa.strip(), ipa
                assert ipa not in result, ipa
                result[ipa] = espeak
        return result

    
def run():
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='TCP port for serving HTTP requests')
    parser.add_argument('--espeak', default='/usr/bin/espeak-ng',
                        help='espeak binary to be called in a subprocess')
    args = parser.parse_args()
    global ipa_mapper, espeak_binary
    espeak_binary = args.espeak
    ipa_mapper = IPAMapper('ipa_to_espeak.txt')
    httpd = HTTPServer(('', args.port), IPASpeaker)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
