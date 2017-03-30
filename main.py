#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, shutil, argparse
import requests
from io import BytesIO

class fonts(requests.Session):
    def __init__(self, url, dir='dist'):
        super(fonts, self).__init__()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.dir = dir
        self.css = "%s/style.css"%dir
        self.style = self.loadCSS(self.css)
        self.style+= self.getCSS(url)

        if not os.path.isdir(dir):
            os.mkdir(dir)

    def getFilename(self, url):
        return url.rsplit('/', 1)[1]

    def getUrlsFromStyle(self, style):
        return re.findall('url\((https[^\)]*)', style)

    def getCSS(self, url):
        resp = self.get(url, headers=self.headers)
        return resp.content

    def loadCSS(self, path):
        print "Load %s"%path
        try:
            with open(path, 'r') as f:
                return ''.join(f.readlines())
        except IOError:
            return ''

    def saveCSS(self, path, style):
        print "Save %s"%path
        urls = self.getUrlsFromStyle(style)
        for url in urls:
            filename = self.getFilename(url)
            style = style.replace(url, filename)
        with open(path, 'w') as f:
            f.write(style)

    def downloadFile(self, url, dst):
        resp = self.get(url);
        with open(dst, 'wb') as f:
            f.write(BytesIO(resp.content).getvalue())

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('-d', '--directory', default='dist')
    parser.add_argument('family', nargs='?')
    args = parser.parse_args()

    if args.action in ['css', 'icon']:
        print args.action
        url = "https://fonts.googleapis.com/%s?family=%s"%(args.action, args.family)
        gf = fonts(url, args.directory)
        for url in gf.getUrlsFromStyle(gf.style):
            dst = "%s/%s"%(gf.dir, gf.getFilename(url))
            gf.downloadFile(url, dst)
            print 'Download %s'%dst
        gf.saveCSS(gf.css, gf.style)

    elif args.action == 'clean':
        print 'clean: %s'%args.directory
        if os.path.isdir(args.directory):
            shutil.rmtree(args.directory)
    else:
        parser.print_help()
