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

from ...lib.config_constant import ConfigConstant

from ...lib.xpath_parser import Widget
from widget_base import WidgetBase

class LoginPageWidget(WidgetBase):
    
    def __init__(self):
    
        ## Login Page Set Password
        self.LOGIN_PAGE_SET_PASSWORD     = Widget(name='LOGIN_PAGE_SET_PASSWORD',
                                             xpath="//input[@name='newpassword']",
                                             type=ConfigConstant.WIDGET_TYPE_TEXT_BOX,
                                             url='')
        self.LOGIN_PAGE_CONFIRM_PASSWORD = Widget(name='LOGIN_PAGE_CONFIRM_PASSWORD',
                                             xpath="//input[@name='newpassword2']",
                                             type=ConfigConstant.WIDGET_TYPE_TEXT_BOX,
                                             url='')
        self.LOGIN_PAGE_SET_PASSWORD_SUBMIT = Widget(name='LOGIN_PAGE_SET_SUBMIT',
                                             xpath="//label[@id='loginBtn']",
                                             type=ConfigConstant.WIDGET_TYPE_BUTTON,
                                             url='',
                                             save_button=True)
                                             
        ## Login Page Login
        self.LOGIN_PAGE_LOGIN_PASSWORD   = Widget(name='LOGIN_PAGE_LOGIN_PASSWORD',
                                             xpath="//input[@name='pcPassword']",
                                             type=ConfigConstant.WIDGET_TYPE_TEXT_BOX,
                                             url='')
        self.LOGIN_PAGE_LOGIN_SUBMIT     = Widget(name='LOGIN_PAGE_LOGIN_SUBMIT',
                                             xpath="//label[@id='loginBtn']",
                                             type=ConfigConstant.WIDGET_TYPE_BUTTON,
                                             url='',
                                             save_button=True)