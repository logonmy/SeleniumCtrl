#!/usr/bin/env python
# -*- coding: UTF-8 -*

########################################################################################################################
# Copyright (C), 2012, TP-LINK Technologies Co., Ltd.
#
# Filename:     SeleniumRC.py
# Version:      1.0.0
# Description:  Module for (Wireless) Router control.
# Author:       libo
# History:
#   1. 2012-9-25,  libo, first created.
########################################################################################################################

'''Module for (wireless) router control.

This module exports several class to control routers:
    class SohoSeleniumRC: control all the routers of TP-LINK
'''

import os
import re
from xml.dom import minidom
import logging
import urllib2
from selenium import selenium

from selenium_rc.lib.config_constant import ConfigConstant
from selenium_rc.lib.xpath_parser import Widget

logging.basicConfig(level=logging.DEBUG)
    
__version__ = '1.1.1'

FILE_DIR = os.path.join(os.getcwd(), os.path.dirname(__file__))
 
class RouterMap(object):
    ''' Class for searching right control module from a xml file.'''

    selenium_rc_package = 'selenium_rc'
    map_xml_path        = os.path.join(FILE_DIR, 'selenium_rc/etc/map.xml')
    
    def __init__(self, ip='192.168.1.1', username='admin', password='admin', port=80,
                 default_ip=None, default_username=None, default_password=None, default_port=None,
                 class_name=None, login_mode=None,
                 sel_host='localhost', sel_port=4444, sel_browser=ConfigConstant.BROWSER_FIREFOX):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ip               = ip
        self.username         = username
        self.password         = password
        self.port             = port
        self.default_ip       = default_ip
        self.default_username = default_username
        self.default_password = default_password
        self.default_port     = default_port
        self.sel_host         = sel_host
        self.sel_port         = sel_port
        self.sel_browser      = sel_browser
        self.login_mode       = login_mode
        self.class_name       = class_name
        self.realm            = self._get_realm()
        self.logger.debug('Realm is: %s' % self.realm)
        self.map_doc  = minidom.parse(self.map_xml_path)        
        
    def get_class_obj(self):
        ''' return instance of the matching class'''
        
        if self.class_name is not None:
            return self._instance_class(self.class_name)
            
        real_realm = unicode(self.realm, 'gb2312')
        router_nodes = self.map_doc.getElementsByTagName('router')
        for router_node in router_nodes:
            try:
                realm = router_node.getAttribute('realm')
                if realm == real_realm:
                    class_name = router_node.getAttribute('class')
                    if router_node.getAttribute('login_mode'):
                        self.login_mode = router_node.getAttribute('login_mode')
                    return self._instance_class(class_name)  
            except Exception, ex:
                self.logger.debug('%s' % ex)
        
        return None
        
    def _parse_router_node_with_normal_class_name(self, router_node):
        ''' for tplink, linksysy, etc '''
        
        ## instance class
        class_name = router_node.getAttribute('class')
        class_obj = self._instance_class(class_name)  
        
        map_nodes = router_node.getElementsByTagName('map')        
        if map_nodes:
            ## Get real software
            self.logger.debug('Get real software...')
            real_software_version = class_obj.get_software_version()
            self.logger.debug('Real software is: %s' % real_software_version)
            
            ## Get build date in software version
            m = re.search('(\d{6})', real_software_version)
            date = m.group() 
            
            ## find the matching class name
            current_class_name = None
            for map_node in map_nodes:
                software_version = map_node.getAttribute('sw')
                class_name = map_node.getAttribute('class')
                if re.match('\d{6}~\d{6}', software_version):
                    [first_date, last_date] = re.split('~', software_version)
                    if first_date < date and date <= last_date:
                        current_class_name = class_name
                else:
                    if software_version == real_software_version:
                        current_class_name = class_name
                        break
                        
            if current_class_name:
                class_obj = self._instance_class(current_class_name)
                
            return class_obj
        else:
            return class_obj
        
    def _parse_router_node_with_blank_class_name(self, router_node):
        ''' for dlink '''
        
        map_nodes = router_node.getElementsByTagName('map')
        for map_node in map_nodes:
            ## get software in map.xml
            software_version = map_node.getAttribute('sw')
            class_name = map_node.getAttribute('class')
            
            ## get real software
            try:
                class_obj = self._instance_class(class_name)
                real_software_version = class_obj.get_software_version()
                self.logger.debug('Real software is: %s' % real_software_version)
            except Exception, ex:
                self.logger.debug('Not a right class: %s' % ex)
                continue
            
            ## if match, return
            if real_software_version == software_version:
                return class_obj
                
        return None
        
    def _instance_class(self, class_name):          
        self.logger.debug('importing %s' % class_name)
        exec('from %s import %s' % (self.selenium_rc_package, class_name))
        c = eval('%s.%s' % (class_name, class_name))
        self.logger.debug('New %s' % class_name)
        class_obj = c(ip=self.ip, username=self.username, password=self.password, port=self.port,
                      default_ip=self.default_ip, default_username=self.default_username, 
                      default_password=self.default_password, default_port=self.default_port,
                      login_mode=self.login_mode,
                      sel_host=self.sel_host,
                      sel_port=self.sel_port,
                      sel_browser=self.sel_browser)
        
        return class_obj         
        
    def _get_realm(self):
        ''' get realm '''
        
        url = 'http://%s:%s' % (self.ip, self.port)
        try:
            request_obj = urllib2.Request(url)
            request_obj.add_header('Accept-Encoding', 'gzip,deflate')
            request_obj.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
            handle = urllib2.urlopen(request_obj, timeout=5)
            realm  = self._get_realm_from_header(handle)
            if not realm:
                realm = self._get_realm_from_response(handle)
            return realm
        except IOError, ex:
            if hasattr(ex, 'code'):
                if ex.code != 401:
                    self.logger.error('We got another error: %s' % ex.code)
                    raise ex
                else:
                    return self._get_realm_from_header(ex)
            else:
                raise ex
        
    def _get_realm_from_header(self, url_handle):
        '''Get realm from HTTP header.'''
        
        # for d-link products
        if 'www-authenticate' not in url_handle.headers:
            return ''
        
        auth_message = url_handle.headers['www-authenticate']
        m_realm = 'Realm="(.*)"'
        m = re.search(m_realm, auth_message, re.I)
        if m is not None:
            realm = m.group(1)
        else:
            realm = ''
            
        return realm
        
    def _get_realm_from_response(self, url_handle):
        ''' Get realm from response'''
        
        response = url_handle.read()
        search   = re.search('<title>(.*?)</title>', response, re.I)
        if search:
            return search.group(1)
        else:
            return ''
        
    def get_realm(self):
        return self.realm
    

class SohoSeleniumRC(object):
    def __new__(self, ip='192.168.1.1', username='admin', password='admin', port=80,
                 default_ip=None, default_username=None, default_password=None, default_port=None,
                 class_name=None, login_mode=None,
                 sel_host='localhost', sel_port=4444, sel_browser=ConfigConstant.BROWSER_FIREFOX):
        
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.logger.debug('Create Selenium RouterCtrl object, ip=%s, username=%s, password=%s'   \
                                % (ip, username, password))
        router_map = RouterMap(ip=ip, username=username, password=password, port=port,
                                default_ip=default_ip, 
                                default_username=default_username, 
                                default_password=default_password,
                                default_port=default_port,
                                class_name=class_name,
                                login_mode=login_mode,
                                sel_host=sel_host,
                                sel_port=sel_port,
                                sel_browser=sel_browser)
        class_obj = router_map.get_class_obj()
        if class_obj is None:
            err_msg = 'Fail to control your DUT. ' \
                      'Please Make sure that you have added an entry in /router_ctrl/etc/map.xml.'
            self.logger.warn(err_msg)
            raise RuntimeError(err_msg)
        return class_obj
            