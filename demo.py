# -*- coding: utf-8 -*-
# @Time : 2020/3/10 17:12
# @Author : wangmengmeng
import xml.etree.ElementTree as ET

from common.readXML import ReadXML


def get_allEle(fele):
    rlt_dict = {}
    for child in fele:
        child_text = child.text.replace(" ", "") if child.text != None else child.text  # 把xml中节点内容中有空格的去掉
        rlt_dict[child.tag] = child_text.replace("\n",'None') if child_text == '\n' else child_text  # 把xml中节点内容是换行符的替换成None
        get_allEle(child)  # 调用函数自己本身
    return rlt_dict
    # return fele


def get_standardResult(outputxml):
    rxml = ReadXML(outputxml)
    rlt_stan = rxml.get_allEle_change(rxml.root)
    return rlt_stan


# print(get_standardResult('ipt_new'))





tree = ET.parse('ipt_new')
root = tree.getroot()
for child in root:
    print(child.tag)
print(get_allEle(root))


# xmlstr = ET.tostring(xml_data, encoding='unicode', method='xml')
# print(xmlstr)
# print(get_allEle(xml_data))

# print(xmlstr)
# data_dict = dict(xmltodict.parse(xmlstr))
# print(data_dict)

# with open('new_data_2.json', 'w+') as json_file:
#     json.dump(data_dict, json_file, indent=4, sort_keys=True)
