#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : seccenter.fcgi
'''Purpose : Intro sth                                 '''
# Creation Date : 1428389717
# Last Modified :
# Release By : Doom.zhou


from flup.server.fcgi import WSGIServer
from seccenter import app


if __name__ == '__main__':
    WSGIServer(app, bindAddress=('127.0.0.1', 8080)).run()
