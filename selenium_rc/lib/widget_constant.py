#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2013, TP-LINK Technologies Co., Ltd.
#
# Firename   : widget_constant.py
# Version    : 1.0.0
# Description: Module for TP-LINK access control.
# Author     : libo
# History:
#   1. 2013-6-7, libo, first created. 
###############################################################################


        
class QuickSetupPages(object):

    ## Quick Setup Start Page
    QS_SETTING_START_PAGE = 'Quick Setup Start Page'

    ## Quick Setup WAN Page
    QS_SETTING_WAN_TYPE_PAGE      = 'Quick Setup Wan Type Page'
    QS_SETTING_WAN_STATIC_PAGE    = 'Quick Setup Wan Static IP Page'
    QS_SETTING_WAN_PPPOE_PAGE     = 'Quick Setup Wan PPPoE Page'
    QS_SETTING_WAN_MAC_CLONE_PAGE = 'Quick Setup Wan Mac Clone Page'
               
    ## Quick Setup Wlan Page
    QS_SETTING_WLAN_PAGE          = 'Quick Setup Wlan Page'
                         
    
    ## Quick Setup End
    QS_SETTING_END_PAGE = 'Quick Setup End Page'                     

class WidgetConstant(QuickSetupPages):
    pass
    