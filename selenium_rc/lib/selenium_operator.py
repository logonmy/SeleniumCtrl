#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2013, TP-LINK Technologies Co., Ltd.
#
# filename:     selenium_operator.py
# version:      1.0.0
# description:  Module for sending HTTP Request.
# first create: libo
# history:
#       2013-06-08 | First created. 
###############################################################################

"""Module for operate seleniumRC.

This module exports one class:
    class SeleniumOperator: operate selenium
"""

import os
import re
import time
import urllib
import urllib2
import httplib
import urlparse
import base64

import my_ping
import Auth_handler

import logging
from selenium import selenium

from config_constant import ConfigConstant
from xpath_parser import Widget


class SeleniumOperator(object):
    
    AUTHORITY_BASIC   = 'basic'
    AUTHORITY_COOKIE  = 'cookie'
    AUTHORITY_SESSION = 'session'
    AUTHORITY_UNKNOWN = 'unknown'
    
    sel = None
    
    def __init__(self, ip='192.168.1.1', username='admin', password='admin', port=80,
                 default_ip=None, default_username=None, default_password=None, default_port=None,
                 sel_host='localhost', sel_port=4444, sel_browser=ConfigConstant.BROWSER_FIREFOX,
                 login_mode='basic'):
                 
        self.ip = ip
        self.username = username
        self.password = password
        self.port     = port
        self.sel_host = sel_host
        self.sel_port = sel_port
        self.sel_browser = sel_browser
        if default_ip is None:
            self.default_ip = ip
        else:
            self.default_ip = default_ip
        if default_username is None:
            self.default_username = username
        else:
            self.default_username = default_username
        if default_password is None:
            self.default_password = password
        else:
            self.default_password = default_password
            
        if default_port is None:
            self.default_port = port
        else:
            self.default_port = default_port
            
        self.login_mode   = login_mode
        self.authority    = login_mode
        self.login_status = False 
        
        if self.__class__.sel is None:
            self.__class__.sel = selenium(self.sel_host, self.sel_port, self.sel_browser, 'http://%s/'%self.ip)
            self.__class__.sel.start()
        
    # @property    
    # def sel(self):
        
        # if hasattr(self, '_sel'):
            # return self._sel
            
        # if self.login_mode == 'basic':
            # self._sel = selenium(self.sel_host, self.sel_port, self.sel_browser, 
                                 # 'http://%s:%s@%s:%s/'%(self.username, self.password, self.ip, self.port))
        # else:
            # self._sel = selenium(self.sel_host, self.sel_port, self.sel_browser, 'http://%s/'%self.ip)
        # self._sel.start()
        
        # return self._sel
        
    def login(self):
        ''' login the dut
        '''
        if self.login_status:
            return
        self.login_status = True
        
        if self.login_mode == 'cookie':
            url = 'http://%s/'%(self.ip)
            self.sel.open(url)
            if self.is_widget_present(self.widgets.LOGIN_PAGE_SET_PASSWORD):
                self.set(widget=self.widgets.LOGIN_PAGE_SET_PASSWORD, value=self.default_password)
                self.set(widget=self.widgets.LOGIN_PAGE_CONFIRM_PASSWORD, value=self.default_password)
                self.set(widget=LOGIN_PAGE_SET_PASSWORD_SUBMIT)
            if self.is_widget_present(self.widgets.LOGIN_PAGE_LOGIN_PASSWORD):
                self.set(widget=self.widgets.LOGIN_PAGE_LOGIN_PASSWORD, value=self.default_password)
                self.set(widget=self.widgets.LOGIN_PAGE_LOGIN_SUBMIT)
        elif self.login_mode == 'session':
            pass
        else:
            url = 'http://%s:%s@%s:%s/'%(self.username, self.password, self.ip, self.port)
            self.sel.open(url)  
        
            
    def is_widget_present(self, widget):
        return self.sel.is_element_present(widget.xpath)
            
    def go_to_widget(self, end=None, start=None):
        self.login()
        if end is None or not isinstance(end, Widget):
            raise Exception('there is no end widget')
        
        # find how to reach the widget
        widget_list = []
        tmp_end     = end
        if start is not None:
            start = start.name
        
        while tmp_end.belongs is not None and tmp_end.belongs.keys()[0] != start:
            widget_list.append(tmp_end.belongs)
            tmp_end = self.widgets.WIDGET_DICT[tmp_end.belongs.keys()[0]]
        if start is not None:
            widget_list.append({start:None})

        # go to the widget
        # from the first father widget,
        # find all widgets belongs to this url
        # input the default value, click the save button
        widget_list.reverse()
        try:
            self.sel.select_frame('relative=up')
        except:
            pass
        for widget in widget_list:
            
            if self.is_widget_present(end):
                break
                
            # find all widget for current url
            
            # set default value for all widget except save_button
            save_button = None
            
            for curr_widget in widget.keys():
                widget_ctrl = self.widgets.WIDGET_DICT[curr_widget]
                if widget_ctrl.save_button:
                    save_button = widget_ctrl
                    continue
                self.set(widget=widget_ctrl, value=widget[curr_widget])
                    
            # save button
            if save_button is not None:
                self.set(widget=save_button)
            
        self.curr_widget = end
        
    def set(self, widget=None, method=None, value=None, timeout=None):
        ''' set the widget
            
            Arguments:
                widget(obj)  : the widget which need to be set
                method(str)  : the method which we set the widget with
                value(str)   : the value which we set the widget by
                timeout(int) : the timeout to sleep after setting the widget
        '''
        
        self.login()
        
        if widget is None:
            widget = self.curr_widget
        else:
            self.curr_widget = widget
            
        try:
            self.sel.select_frame('relative=up')
            self.sel.select_frame(widget.frame)
        except:
            pass
            
        # do the required mathod
        if method is not None:
            if (method, value) in widget.globals.keys():
                exec("self.sel.%s()"%widget.globals[(method, value)])
                return
            else:
                pass        

        # do the default method
        elif value is None:
            exec("self.sel.%s(widget.xpath)"%widget.calls)
            
        # do method according to value    
        else:
            if widget.sets.has_key(value):
                exec("self.sel.%s(widget.xpath)"%widget.sets[value][0])
            else:
                exec("self.sel.%s(widget.xpath, value)"%widget.calls)
        
        if widget.type in (ConfigConstant.WIDGET_TYPE_BUTTON, ConfigConstant.WIDGET_TYPE_LINK):
            if timeout is not None:
                time.sleep(timeout)
            else:
                if not self.sel.is_alert_present():
                    self.wait_for_page_to_load()
                else:
                    raise Exception('An alert is detected')
        
    def get(self, widget=None, value=None):
        ''' get some message of the widget
            
            Arguments:
                widget(obj) : the widget
                value(str)  : which message you want to get
        '''
        if widget is None:
            widget = self.curr_widget
        if value is None:
            value = 'value'

        # get some message without widget
        if value in ['location', 'body_text']:
            self.sel.select_frame(widget.frame)
            result = eval("self.sel.%s()"%widget.gets[value][0])
            self.sel.select_frame('relative=up')
            return result
            
        # get some message with widget
        if not value in widget.gets.keys():
            raise Exception('can not find the method for "%s"'%value)
        
        comm = widget.gets[value]
        if comm[1] is not None:
            return eval("self.sel.%s(widget.xpath)"%comm[0])
        else:
            return eval("self.sel.%s()"%comm[0])
    
    def update_rqst_args(self, ip=None, port=None, username=None, password=None):
        ''' update the request arguments
        
            Arguments:
                ip(str)       : the ip address of the dut
                port(int)     : the port of web server
                username(str) : the username of the dut
                password(str) : the password of the dut
            Returns:
                None
        '''
        
        if ip is not None:
            self.ip       = ip 
        if port is not None:
            self.port     = port 
        if username is not None:
            self.username = username 
        if password is not None:
            self.password = password 
            
    def restart(self):
        self.sel.close()
        self.sel.stop()
        self.login_status = False
        
    def request_with_get(self, url, param_dict=None, referer=None):
        ''' Send HTTP request with GET method.'''
        
        if self.port == 80 or self.port == '80':
            pass
        else:
            url = url.replace(self.ip, '%s:%s' % (self.ip, self.port))
        
        tmp_url = url
        if param_dict is not None:
            params = urllib.urlencode(param_dict)
            url = '%s?%s' % (url, params)
        else:
            param_dict = {}
            
        if self.authority == self.AUTHORITY_COOKIE:
            auth_handler = Auth_handler.HTTPMifiAuthHandler(ip=self.ip, password=self.password,
                                                                    user=self.username, port =self.port, referer=referer)
            opener = urllib2.build_opener(auth_handler)
            req = urllib2.Request(url=url)
        elif self.authority == self.AUTHORITY_SESSION:
            auth_handler = Auth_handler.HTTPMifiAuthHandler(ip=self.ip, password=self.password,
                                                                    user=self.username, port =self.port, referer=referer)
            opener = urllib2.build_opener(auth_handler)
            req = urllib2.Request(url='http://%s:%s/'%(self.ip, self.port))
            f = opener.open(req, timeout=60)
            response = f.read()
            js2py_obj = js2py.extract_js(response)
            if hasattr(js2py_obj.attr, 'fileParaFS'):
                file_paras = js2py_obj.attr.fileParaFS
                cmp        = file_paras[0]
                session    = file_paras[1]
            param_dict.update({'cmp':cmp, 'session':session})
            params = urllib.urlencode(param_dict)
            if '?' in tmp_url:
                url ='%s&%s'%(tmp_url, params)
            else:
                url = '%s?%s' % (tmp_url, params)
            req = urllib2.Request(url=url)
            
        else:
            psw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            psw_mgr.add_password(None, 'http://%s:%s' % (self.ip, self.port), self.username, self.password)
            auth_handler = urllib2.HTTPBasicAuthHandler(psw_mgr)
            opener = urllib2.build_opener(auth_handler)
            req = urllib2.Request(url=url)
            req.add_header('Accept-Encoding', 'gzip,deflate')
            if referer is None:
                req.add_header('Referer', 'http://%s/'%self.ip)
            elif referer == False:
                pass
            else:
                req.add_header('Referer', referer)
            req.add_header('User-Agent', 
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
            if not url.endswith((self.ip, '%s/' % self.ip, '%s:%s' % (self.ip, self.port), '%s:%s/' % (self.ip, self.port))):
                req.add_header('Authorization', 'Basic %s' % base64.b64encode('%s:%s' % (self.username, self.password)))
                
        f = opener.open(req, timeout=60)
        
        # add by wanpanpan
        # to fix the bug of blocking when TL-WR740N(CN) 5.0 rebooting
        if param_dict is not None and 'Reboot' in param_dict:
            return None
            
        response = f.read()
        m_res = '(var\s+errCode\s*=\s*"\d+")'
        m = re.search(m_res, response, re.I)
        if m is not None:
            err_code = m.group(1)
            raise RuntimeError(self.ERR_URL, 'Error Code is %s' % err_code)
        else:
            return response            
        
    def wait_for_restart(self):
        ''' Wait for finishing restarting.'''
        
        ## The full timeout is 24*1*5 = 120s
        ## ping ok, then wait 3s, ping ok, then wait 3s, ping ok
        RETRY_TIMES = 30
        retry_times = RETRY_TIMES
        time.sleep(5)
        
        while retry_times:
            time.sleep(3)
            if my_ping.check_ping(self.ip, timeout=1, count=5):
                time.sleep(3)
                if my_ping.check_ping(self.ip, timeout=1, count=5):
                    return self.wait_for_webserver_start()
                    # if retry_times == RETRY_TIMES:
                        # raise self.NotEffectError(
                                # 'restart didn\'t take effect.')
                    # else:
                        # return self.wait_for_webserver_start()
                else:
                    retry_times -= 1
            else:
                retry_times -= 1
                
        raise RuntimeError(1, 'Ping through device fail after restart it.')

    def wait_for_webserver_start(self):
        ''' wait for web server start after ping DUT ok'''
        RETRY_TIMES = 20
        retry_times = RETRY_TIMES
        while retry_times:
            time.sleep(3)
            try:
                self.request_with_get(url="http://%s" % (self.ip) )
                return
            except Exception, ex:
                self.logger.warn("DUT web server didn't start yet, "
                                 "retry %d times: %s" % (retry_times, ex) )
                retry_times -= 1
                
        raise RuntimeError(2, 'DUT web server didn\'t start within %d \
                                seconds after dut ping OK' % (RETRY_TIMES * 3)) 
                                
    def wait_for_page_to_load(self, timeout=None):
        if timeout is None:
            timeout = 150000
        self.sel.wait_for_page_to_load(timeout)      
            
    def __del__(self):
        self.sel.open('about:blank')
    
            