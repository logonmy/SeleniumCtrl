#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2012, TP-LINK Technologies Co., Ltd.
#
# filename:     xpath_parser.py
# version:      1.0.0
# description:  Module for parse the xpath.
# author:       libo
# history:
#       2012-09-24 | First created. 
###############################################################################

"""Module for parse the xpath.

This module exports one class:
    class Xpath: the XPath information
"""

from config_constant import ConfigConstant

CALL_METHOD = {ConfigConstant.WIDGET_TYPE_CHECK_BOX:'check',
               ConfigConstant.WIDGET_TYPE_BUTTON:'click',
               ConfigConstant.WIDGET_TYPE_LINK:'click',
               ConfigConstant.WIDGET_TYPE_TEXT_BOX:'type',
               ConfigConstant.WIDGET_TYPE_MANU:'select',
               ConfigConstant.WIDGET_TYPE_RADIO:'check'}

class Widget(object):
    def __init__(self, name, xpath, type, belongs=None, frame=None, level=None, visiable=True, url=None,
                 default_value=None, current_value=None, save_button=False):
        ''' 
            Arguments:
                name(str) : name of the widget
                xpath(str) : xpath of the widget
                type(str) : type of the widget, such as WIDGET_TYPE_CHECK_BOX, WIDGET_TYPE_BUTTON
                belongs(dict) : which widgets this widget belongs to, {widget1_name:value, widget2_name:value}
                frame(str) : the frame which this widget belongs to
                visiable(bool) : the widget is visiable or not
                url(str): the url which this widget belongs to
                default_value(str) : default value of this widget
                current_value(str): current value of this widget
                save_button(bool) : if the widget is a save button or not
        '''
        self.name    = name
        self.xpath   = xpath
        self.type    = type
        self.belongs = belongs
        self.calls   = CALL_METHOD[type]
        self.level   = level
        self.visiable = visiable
        self.url     = url
        self.default_value = default_value
        self.current_value = current_value
        self.save_button = save_button
        
        if frame is not None:
            self.frame = frame
        elif level is not None:
            if level <= 1:
                self.frame = 'bottomLeftFrame'
            else:
                self.frame = 'mainFrame'
        else:
            if self.belongs is None:
                self.frame = 'bottomLeftFrame'
            else:
                self.frame = 'mainFrame'
                
        self.gets    = self._query_get_methods()
        self.sets    = self._query_set_methods()
        self.globals = {('confirm', True):'choose_ok_on_next_confirmation',
                        ('confirm', False):'choose_cancel_on_next_confirmation',
                        ('prompt', None):'answer_on_next_prompt'}
        
    def _query_get_methods(self):
        get_methods = {}
        get_methods.update({'value':('get_value', 'xpath'), 
                            'text':('get_text', 'xpath'), 
                            'location':('get_location', None),
                            'body_text':('get_body_text', None),
                            'html_source':('get_html_source', None),
                            'alert':('get_alert', None),
                            'alert_present':('is_alert_present', None),
                            'confirm':('get_confirmation', None),
                            'confirm_present':('is_confirmation_present', None),
                            'prompt':('get_prompt', None),
                            'prompt_present':('is_prompt_present', None),
                            })
        if self.type == ConfigConstant.WIDGET_TYPE_CHECK_BOX:
            get_methods.update({'status':('is_checked', 'xpath')})
        elif self.type == ConfigConstant.WIDGET_TYPE_BUTTON or self.type == ConfigConstant.WIDGET_TYPE_LINK:
            pass
        elif self.type == ConfigConstant.WIDGET_TYPE_MANU:
            pass
        else:
            pass
        
        return get_methods
            
    def _query_set_methods(self):
        set_methods = {}
        set_methods.update({})
        if self.type in [ConfigConstant.WIDGET_TYPE_CHECK_BOX, ConfigConstant.WIDGET_TYPE_RADIO]:
            set_methods.update({True:('check', 'xpath'),
                                False:('uncheck', 'xpath')})
        elif self.type == ConfigConstant.WIDGET_TYPE_BUTTON or self.type == ConfigConstant.WIDGET_TYPE_LINK:
            set_methods.update({None:('click', 'xpath')})
        elif self.type == ConfigConstant.WIDGET_TYPE_MANU:
            pass
        else:
            pass
        
        return set_methods
                

# class SeleniumRequest(object):
    # def __init__(self):
        # self.WIDGET_DICT = {}
        # self.widget      = TmpClassForAddAttr()
        # param_list = dir(self)
        # for param in param_list:
            # tmp_param = getattr(self, param)
            # if isinstance(tmp_param, Widget):
                # self.WIDGET_DICT.update({tmp_param.name:tmp_param})
                # self.widget.add_widget(tmp_param.name, tmp_param)           
