#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2012, TP-LINK Technologies Co., Ltd.
#
# Filename   : MIFI_AUTH_Handler.py
# Version    : 1.0.0
# Description: Module for mifi authorization handler for TL-TR761 2000L.
# Author     : panxingyu
# History:
#   1. 2013-04-16, panxingyu, first created. 
###############################################################################


import urllib
import urllib2
import cookielib
import re
import base64

class HTTPMifiAuthHandler( urllib2.BaseHandler):

    def __init__(self, ip, password, user='admin', port=80, referer=None):
        self._ip = ip
        self._password = password
        self._user = user
        self._port = port
        self._referer = referer
        
    def http_request(self, req):
    
        raw = "%s:%s" % (self._user, self._password)
        auth = 'Basic %s' % base64.b64encode(raw).strip()
        
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Encoding', 'gzip,deflate')
        if self._referer is None:
            req.add_header('Referer', 'http://%s/'%self._ip)
        elif self._referer == False:
            pass
        else:
            req.add_header('Referer', self._referer)
        req.add_header('Cache-Control','max-age=0')
        req.add_header('User-Agent', 
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
        
        url = req.get_full_url()
        
        req.add_header('Cookie','Authorization=%s; subType=%s; TPLoginTimes=1'
                        % (urllib.quote(auth),urllib.quote('pcSub'))
                        )
        return req

def test():
    url = 'http://192.168.1.1/cgi-bin/index.cgi'
    # psw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # psw_mgr.add_password(None, 'http://192.168.1.1/cgi-bin/index.cgi', 'admin', 'admin')
    # auth_handler = HTTPMifiAuthHandler(psw_mgr)
    opener = urllib2.build_opener(  HTTPMifiAuthHandler(ip='192.168.1.1', password='admin', user='admin', port=80),
                                    urllib2.HTTPCookieProcessor())
    req = urllib2.Request(url=url)
    # req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    # req.add_header('Accept-Encoding', 'gzip,deflate')
    # req.add_header('Referer', 'http://192.168.1.1/')
    # req.add_header('Connection','keep-alive')
    # req.add_header('Cache-Control','max-age=0')
    # req.add_header('Cookie','Authorization=Basic%20YWRtaW46YWRtaW4%3D; subType=pcSub; TPLoginTimes=1')
    
    f = opener.open(req, timeout=60)
    
    response = f.read()
    print '=' * 80
    print response
if __name__ == '__main__':
    test()
