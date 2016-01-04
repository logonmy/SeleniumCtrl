#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2013, TP-LINK Technologies Co., Ltd.
#
# filename:     quick_setup_tlwr740n_v5_like.py
# version:      1.0.0
# description:  Module for TP-LINK base products' control.
# first create: libo
# history:
#       2013-06-14 | First created. 
###############################################################################

"""Module for TP-LINK base products' control.

This module exports a class to control routers:
    class QuickSetup: control TP-LINK base products' quick setup
"""

from ..lib.config_constant import ConfigConstant 
from quick_setup import QuickSetupBase

class QuickSetup(QuickSetupBase):

    def __init__(self,*args,**kargs):
        QuickSetupBase.__init__(self,*args,**kargs)
        
    def set_quick_setup_mode_param(self, mode=None):
        ''' set mode
            Argument
                mode: 'Wan', '3G', 'Wlan'
        '''
        pass
        
    def set_quick_setup_wan_type_param(self, wan_type=None):
        if wan_type is not None:
            self.widgets.QS_SETTING_WAN_TYPE_DYNAMIC.current_value = False
            if wan_type == ConfigConstant.WAN_DYNAMIC_IP:
                self.widgets.QS_SETTING_WAN_TYPE_DYNAMIC.current_value = True
            elif wan_type == ConfigConstant.WAN_STATIC_IP:
                self.widgets.QS_SETTING_WAN_TYPE_STATIC.current_value = True
            elif wan_type == ConfigConstant.WAN_PPPoE:
                self.widgets.QS_SETTING_WAN_TYPE_PPPOE.current_value = True
            elif wan_type == ConfigConstant.WAN_PPTP:
                self.widgets.QS_SETTING_WAN_TYPE_PPTP.current_value = True
            elif wan_type == ConfigConstant.WAN_L2TP:
                self.widgets.QS_SETTING_WAN_TYPE_L2TP.current_value = True
            else:
                raise ValueError('Wan type %s is not supported'%wan_type)
    
    def set_quick_setup_wan_static_param(self, ip=None, mask=None, 
                                   gateway=None, dns1=None, dns2=None):
        if ip is not None:
            self.widgets.QS_SETTING_WAN_STATIC_IP.current_value = ip
        if mask is not None:
            self.widgets.QS_SETTING_WAN_STATIC_MASK.current_value = mask
        if gateway is not None:
            self.widgets.QS_SETTING_WAN_STATIC_GATEWAY.current_value = gateway
        if dns1 is not None:
            self.widgets.QS_SETTING_WAN_STATIC_DNS1.current_value = dns1
        if dns2 is not None:
            self.widgets.QS_SETTING_WAN_STATIC_DNS2.current_value = dns2
        
    def set_quick_setup_wan_pppoe_param(self, username=None, password=None, ip_type=None, sta_ip=None, sta_mask=None):
        if username is not None:
            self.widgets.QS_SETTING_WAN_PPPOE_USERNAME.current_value = username
        if password is not None:
            self.widgets.QS_SETTING_WAN_PPPOE_PASSWORD.current_value         = password
            self.widgets.QS_SETTING_WAN_PPPOE_PASSWORD_CONFIRM.current_value = password
        
    def set_quick_setup_wan_l2tp_param(self, username=None, password=None, ip_type=None, server_name=None,
                                       sta_ip=None, sta_mask=None, sta_gateway=None, sta_dns=None):
        pass
    
    def set_quick_setup_wan_pptp_param(self, username=None, password=None, ip_type=None, server_name=None,
                                       sta_ip=None, sta_mask=None, sta_gateway=None, sta_dns=None):
        pass
        
    def set_quick_setup_mac_clone_param(self, is_clone=None):
        pass
        
    def set_quick_setup_wlan_param(self, ssid=None, wlan_enable=None, region=None, 
                                   mode=None, channel=None, bandwidth=None, 
                                   sec_type=None, rate=None, key=None,
                                   wep_auth_type=None, wep_key_format=None, wep_key_index=None):
        if ssid is not None:
            self.widgets.QS_SETTING_WLAN_SSID.current_value = ssid
        
        if sec_type is not None:
            self.widgets.QS_SETTING_WLAN_SECURITY_NONE.current_value = False
            if sec_type == ConfigConstant.WLAN_NO_ENCRYPTION:
                self.widgets.QS_SETTING_WLAN_SECURITY_NONE.current_value = True
            elif sec_type == ConfigConstant.WLAN_ENCRYPTION_AES:
                self.widgets.QS_SETTING_WLAN_SECURITY_AES.current_value = True
                if key is not None:
                    self.widgets.QS_SETTING_WLAN_SECURITY_AES_KEY.current_value = key
            else:
                pass
        
        if wlan_enable is not None:
            self.widgets.QS_SETTING_WLAN_STATUS.current_value = bool(wlan_enable)
