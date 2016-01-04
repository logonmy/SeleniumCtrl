#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2013, TP-LINK Technologies Co., Ltd.
#
# Firename   : quick_setup_tlwr740n_v5_like.py
# Version    : 1.0.0
# Description: Module for TP-LINK access control.
# Author     : libo
# History:
#   1. 2013-6-7, libo, first created. 
###############################################################################


from ...lib.xpath_parser import Widget

class WidgetBase(object):
    URL_PARAMS_DICT = {}
    WIDGET_DICT     = {}
    URL_SAVE_DICT   = {}
    
    def __setattr__(self, attr, value):
        
        if isinstance(value, Widget):
            # if invisable pass
            if not value.visiable:
                return
                
            # set attr
            object.__setattr__(self, attr, value)

            # add item to url
            if hasattr(value, 'url') and value.url is not None:
                
                # add url dict for the first time
                if not self.__class__.URL_PARAMS_DICT.has_key(value.url):
                    self.__class__.URL_PARAMS_DICT.update({value.url:[]})
                    
                # add map for item and url
                if value.save_button:
                    self.__class__.URL_SAVE_DICT.update({value.url:value.name})
                elif not value.name in self.__class__.URL_PARAMS_DICT[value.url]:
                    self.__class__.URL_PARAMS_DICT[value.url].append(value.name)
                else:
                    pass
            
            
            # add map for item and name
            self.__class__.WIDGET_DICT.update({value.name:value})
            
        else:
            object.__setattr__(self, attr, value)