#coding:utf-8
import xml.etree.ElementTree as etree
import time

class ReadXML():
    def __init__(self,path=None):
        self.path=path
        if self.path!=None:
            #获取xml文件中的树结构对象，root节点
            self.dom=etree.parse(self.path)
            self.root=self.getroot()

    def getroot(self):
        # self.root=self.dom.documentElement
        self.root=self.dom.getroot()
        return self.root

#将字符串转换为xml
    def stringtoXML(self,text_str):
        return etree.fromstring(text_str)

# 将从xml文件获取的根节点转换为 xml字符串 (供传参时内容是xml字符串时使用)
    def tostring(self):
        self.root=self.getroot()
        self.root_str=etree.tostring(self.root)
        return self.root_str

#获取节点的标签名
    def get_eleTag(self,ele):
        return ele.tag

#获取节点的属性
    def get_eleAttrib(self,ele):
        return ele.attrib

#获取节点的文本内容
    def get_eleText(self,ele):
        return ele.text

#获取子节点的文本内容
    def get_childeleText(self,fele,cele):
        return fele.find(cele).text

#修改节点的内容(用于审方入参数据的修改)
    def set_eleText(self,fele,cele):
        for ele in fele:
            if ele.tag==cele:
                ele.text=str(time.time())
                print(ele,ele.text)
            self.set_eleText(ele,cele)

#将xml中节点文本内容中的换行与空格去掉
    def del_space(self,root):
        for ele in root:
            # print(ele.text,list(ele))
            if list(ele)!=[] or ele.text==None:   #如果节点下面还有子节点或者节点文本内容为空,不进行删除操作
                ele.text=ele.text
            else:
                ele.text=ele.text.replace("\n",'').strip()
            self.del_space(ele)
        self.dom.write(self.path,encoding='utf-8')

#获取审方入参的recipe_id
    def get_recipeid(self):
        return self.root.find('opt_prescriptions').find('opt_prescription').find('opt_prescription_info').find('recipe_id').text
        # for ele in root:
        #     if ele.tag==eletag:
        #         return ele.text
        #     break
        #     self.get_idtext(ele,eletag)


#根据属性名称获取属性的内容
    def get_eleAttribByName(self,ele,name):
        return ele.get(name)

#获取所有的节点以及节点的内容
    def get_allEle(self,fele):
            for child in fele:
                self.child_text=child.text.replace(" ","") if child.text!=None else child.text     #把xml中节点内容中有空格的去掉
                self.rlt_dict[child.tag]=self.child_text.replace("\n",'None') if self.child_text=='\n' else self.child_text   #把xml中节点内容是换行符的替换成None
                self.get_allEle(child)   #调用函数自己本身
            return self.rlt_dict

#定义一个局部变量,调用获取节点的接口,获取所有的节点
    def get_allEle_change(self,fele):
        self.rlt_dict={}
        return self.get_allEle(fele)


