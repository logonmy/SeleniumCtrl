#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2013, TP-LINK Technologies Co., Ltd.
#
# filename:     quick_setup.py
# version:      1.0.0
# description:  Module for TP-LINK base products' control.
# first create: libo
# history:
#       2013-06-14 | First created. 
###############################################################################

"""Module for TP-LINK base products' control.

This module exports a class to control routers:
    class QuickSetupSave: control TP-LINK base products' quick setup save
"""

import logging
import time

from ..lib.config_constant import ConfigConstant 
from ..lib.selenium_operator import SeleniumOperator
from ..lib.js2py import extract_js

class QuickSetupBase(SeleniumOperator):
    
    def __init__(self,*args,**kargs):
        SeleniumOperator.__init__(self,*args,**kargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def quick_setup_save(self, timeout=None):
        self.set(self.widgets.QS_SETTING_LINK)

        STEPS = []
        
        # do from the first page
        if hasattr(self.widgets, 'QS_SETTING_START_NEXT'):
            curr_location = self.widgets.QS_SETTING_START_NEXT.url
        else:
            raise RuntimeError('Can not find Quick Setup Widgets')
            
        while curr_location != self.widgets.QS_SETTING_END_FINISH.url:
            self.logger.debug('current url is %s'%curr_location)
            STEPS.append(self.widgets.QS_SETTING_URL_PAGE_DICT[curr_location])
            
            # get all widget in curr_location
            if self.widgets.URL_PARAMS_DICT.has_key(curr_location) and \
                        self.widgets.URL_SAVE_DICT.has_key(curr_location):
                widget_list = self.widgets.URL_PARAMS_DICT[curr_location]
                save_button = self.widgets.URL_SAVE_DICT[curr_location]
            else:
                raise ValueError('Can not find widgets in the page %s'%curr_location)

            # set widget default value
            for widget_name in widget_list:
                widget = self.widgets.WIDGET_DICT[widget_name]
                if widget.current_value is not None:
                    self.set(widget=widget, value=widget.current_value)
                    widget.current_value = None
                elif widget.default_value is not None:
                    self.set(widget=widget, value=widget.default_value)
                else:
                    pass
            
            # save
            self.set(self.widgets.WIDGET_DICT[save_button])
            
            # update location
            curr_location = '/'.join(self.sel.get_location().split('/')[3:])
            
        # finish
        response = self.sel.get_html_source()
        js_obj   = extract_js(response)
        curr_location = '/'.join(self.sel.get_location().split('/')[3:])
        self.logger.debug('current url is %s'%curr_location)
        STEPS.append(self.widgets.QS_SETTING_URL_PAGE_DICT[curr_location])
        
        if js_obj.attr.wzdFinishInf[5] == 1 or js_obj.attr.wzdFinishInf[6] == 1:
            self.set(method='confirm', value=True)
            self.set(widget=self.widgets.QS_SETTING_END_REBOOT)
        else:
            self.set(self.widgets.QS_SETTING_END_FINISH)
        
        if timeout is not None:
            time.sleep(timeout)
        else:
            self.wait_for_restart()

        return STEPS
        