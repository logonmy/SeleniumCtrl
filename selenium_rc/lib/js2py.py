#!/usr/bin/env python
# -*- coding: UTF-8 -*

# ------------------------------------------------------------------------------
# Copyright (C), 2010-2011, TP-LINK Technologies Co., Ltd.
#
# filename: js2py.py
# version:      1.2.0
# description:  parse the javascript code
# first create: libo
# history:
#       2011-08-31 | 1.0.0
#       2011-10-14 | 1.1.0
#                    libo, First created
#       2011-12-12 | 1.2.0
#                    libo, modify
#       2012-04-20 | 1.2.1
#                    libo, modify
# ------------------------------------------------------------------------------

"""javascript to python
"""

__version__ = '1.2.1'
__author__  = 'libo'

import re
import logging

logging.basicConfig(level=logging.DEBUG)

def extract_js(html_source):
    """ Extract JavaScript from html source
    """

    js_code     = re.findall('<SCRIPT language="javascript" '
                             'type="text/javascript">([\s\S]*?)</SCRIPT>',
                             html_source, re.I)
    js_code.extend(re.findall('<SCRIPT language="{0,1}javascript"{0,1}>([\s\S]*?)</SCRIPT>',
                              html_source, re.I))
    js_code.extend(re.findall('<SCRIPT type="text/javascript">([\s\S]*?)</SCRIPT>',
                              html_source, re.I))

    myjs        = JS2PY()
    for string in js_code:
        myjs.get_eval(string)
    return myjs

def extract_str(string):
    """ Extract the string
    """
    old = ['\\\\', '\\n', '\\t', '\\"', '\\r', '\\<', '\\>', '\\/']
    new = ['\\', '\n', '\t', '\"', '\r', '<', '>', '/']
    for i in range(len(old)):
        string = string.replace(old[i], new[i])
    return string

class JSVar(object):
    def __init__(self):
        self.keys = []
    def __getitem__(self, num):
        return self.__dict__[self.keys[num]]
    def __len__(self):
        return len(self.keys)

class JS2PY(object):

    def __init__(self, string = ''):
        """ Initialization.
            __init__(self, string = '')
        """
        self.attr       = JSVar()
        self.str_list      = ['']
        self.__str_mark = 'js2py_str'
        self.get_eval(string)
        self.logger     = logging.getLogger(self.__class__.__name__)
        

    def get_eval(self, string):
        """ Transform JavaScript to Python
        """
        # if not isinstance(string, str):
            # self.logger.debug("Error!The input is not a string.")
            # raise ValueError

        # replace "" by js2py_str0
        tmpstr = re.findall('[^\\\\]""', string)
        for i in tmpstr:
            string = string.replace(i, '%s%s0'%(i[0], self.__str_mark))

        # replace "..." by js2py_stri, i is a integer
        str_match = re.findall('"([\s\S]*?[^\\\\](\\\\\\\\)*?)"', string)
        for i in range(len(str_match)):
            string = string.replace('"%s"'%(str_match[i][0]),
                                    '%s%s'%(self.__str_mark, len(self.str_list)))
            self.str_list.append(str_match[i][0])
            
        # remove the remarked sentence

        string = re.sub('//.*?\n', '', string)
        string = re.sub('//.*?\r\n', '', string)
        string = re.sub('/\*[\s\S]*?\*/\n', '', string)
        string = re.sub('/\*[\s\S]*?\*/\r\n', '', string)
        
        # replace the \r\n
        string = string.replace('\r\n', '')
        string = string.replace('\n', '')
        
        # extract code
        string = re.findall('(var .*?=.*?);', string)
        for i in range(len(string)):
            if re.findall('new\s+Array\(.*?\)', string[i]):
                self.__array_trans(string[i])
            elif re.findall('var .*?=\s*{', string[i]):
                self.__dict_trans(string[i])
            else:
                self.__var_trans(string[i])

    def __str_to_var(self, string):
        """ transform string to variable
        """
        string = string.replace(' ', '')
        try:
            if self.__str_mark in string:
                return extract_str(self.str_list[
                    int(string.replace(self.__str_mark, ''))])
            elif '.' in string:
                return float(string)
            elif string == 'true' or string == 'false':
                return string
            else:
                return int(string)
        except Exception, ex:
            return string

    def __var_trans(self, string):
        """ Parse the sentence like this:
            var a = 1;
        """
        string = re.search("var\s+(.*)\s*=\s*(.*)", string)
        key    = string.group(1).replace(' ', '')
        value  = string.group(2)
        self.attr.__dict__[key] = self.__str_to_var(value)
        if not key in self.attr.keys:
            self.attr.keys.append(key)

    def __array_trans(self, string):
        """ Parse the sentence like this:
            var a = new Array(1,2,3);
        """
        string = re.search("var\s+(.*)\s*=\s*new Array\((.*)\)", string)
        key    = string.group(1).replace(' ', '')
        value  = string.group(2).split(',')
        value  = [self.__str_to_var(x) for x in value]
        self.attr.__dict__[key] = value
        if not key in self.attr.keys:
            self.attr.keys.append(key)
            
    def __dict_trans(self, string):
        ''' Parse the sentence like this:
            var a = {ssid:"TP-LINK_xxx", channel:6};
        '''
        string = re.search("var\s+(.*)\s*=\s*(.*)", string)
        key    = string.group(1).replace(' ', '')
        value  = string.group(2).replace(' ', '').replace('\t', '')
        tmp_dict = {}
        new_value = ""
        list_mark = 0
        
        for i in range(len(self.str_list)):
            exec("%s%s = self.str_list[i]"%(self.__str_mark, i))
            exec("global %s%s"%(self.__str_mark, i))
        
        for i in value:
            if i == '[':
                list_mark = 1
            elif i == ']':
                list_mark = 0
            
            if list_mark:
                new_value += i
            elif i == '{' or i == ',':
                new_value += i+'"'
            elif i == ':':
                new_value += '":'
            else:
                new_value += i
        
        value = eval(new_value)
        self.attr.__dict__[key] = value
        if not key in self.attr.keys:
            self.attr.keys.append(key)
