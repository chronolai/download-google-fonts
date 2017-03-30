#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil, argparse
import requests
from io import BytesIO

class fonts(requests.Session):
    def __init__(self, dirname='fonts'):
        super(fonts, self).__init__()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.css = '';
        self.dirname = dirname
        if os.path.isdir(self.dirname):
            shutil.rmtree(self.dirname)
        os.mkdir(self.dirname)

    def loadCSS(self, url):
        print "[Load] %s"%url
        resp = self.get(url, headers=self.headers)
        self.css = resp.content
        return resp

    def downloadFont(self, url):
        resp = self.get(url);
        with open('%s/%s'%(self.dirname, self.getFilename(url)), 'wb') as f:
            f.write(BytesIO(resp.content).getvalue())

    def getFilename(self, url):
        return url.rsplit('/', 1)[1]

    def getUrls(self):
        return re.findall('url\(([^\)]*)', self.css)

    def saveCssFile(self):
        urls = self.getUrls()
        for url in urls:
            filename = self.getFilename(url)
            self.css = self.css.replace(url, filename)
        with open('%s/styles.css'%self.dirname, 'w') as f:
            f.write(self.css)

if __name__=='__main__':
    css = fonts()
    css.loadCSS('https://fonts.googleapis.com/css?family=Roboto')
    for url in css.getUrls():
        print "> %s"%url
        css.downloadFont(url)
    css.saveCssFile()

    print
    icon = fonts('icon')
    icon.loadCSS('https://fonts.googleapis.com/icon?family=Material+Icons')
    for url in icon.getUrls():
        print "> %s"%url
        icon.downloadFont(url)
    icon.saveCssFile()
