# -*- coding: utf-8 -*-
"""XML parser for spring generator and mybatis generator.
 XML is an inherently hierarchical data format.
 This module will parse the xml which is given,
 it is able to parse each children node.
 The parser will put node attributes to a Python dict `params`,
 the key is tag of node and the value is text of node which is effective.
 Also, some special dict item will be handled.
"""
import os
from xml.etree import cElementTree

from constant import DEFAULT_CONFIG_PATH
_author_ = 'luwt'
_date_ = '2020/5/15 17:33'


params = dict()
tree = cElementTree.parse(os.path.join(os.path.abspath('.'), DEFAULT_CONFIG_PATH))
root = tree.getroot()


def setter(i):
    params[i.tag] = i.text


# put item to params, key is tag of node and value is text of node which is effective
[[setter(child) for child in node if child.text and child.text.strip()] for node in root.iter()]


# handle special item
params['table_names'] = set(params.get('table_names').split(','))
params['lombok'] = True if params.get('lombok').lower() == 'true' else False
