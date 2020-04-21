from common.readXML import ReadXML
import xml.etree.ElementTree as etre
import config.cfg as cf
import json

class CompareResult():

#获取统一接口返回的xml
    def get_apiResultXML(self,api,inputxml):
        self.api=api
        self.rlt=self.api(inputxml)
        print(self.rlt)
        self.xml=etre.fromstring(self.rlt)
        # self.api_rlt=self.get_allele_api(self.xml)
        self.api_rlt=ReadXML().get_allEle_change(self.xml)
        return self.api_rlt


#获取标准输出的xml
    def get_standardResult(self,outputxml):
        self.rxml=ReadXML(outputxml)
        self.rlt_stan=self.rxml.get_allEle_change(self.rxml.root)
        return self.rlt_stan

#比较xml_正常接口
    def compareXML(self,api,inxml,outxml):
        self.api=eval(api)  #注意 在python环境下运行时需去掉eval,在RF中调用时需加上eval()函数：将传过来的字符串转换成实例对象
        # self.api=api
        self.api_result = self.get_apiResultXML(self.api, inxml)
        self.standard_result = self.get_standardResult(outxml)
        # print(self.api_result, '\n', self.standard_result)
        self.print_result(self.api_result,self.standard_result)

# 比较xml_审方审核结果比较
    def compareXML_sf(self,inxml, outxml):
        self.api_result = self.get_standardResult(inxml)
        self.standard_result = self.get_standardResult(outxml)
        # print(self.api_result, '\n', self.standard_result)
        self.print_result(self.api_result,self.standard_result)

# 循环json数据得到对应的键值
    def get_jsonele(self, rlt):
            for i in rlt:
                # print(i,rlt[i])
                self.rlt_hjjson[i] = rlt[i]
                if type(rlt[i]) is dict:  # 通过键循环字段
                    self.get_jsonele(rlt[i])
                if type(rlt[i]) is list:  # 是字典的话先通过索引得到字段，再循环字段
                    for n in range(len(rlt[i])):
                        self.get_jsonele(rlt[i][n])
            return self.rlt_hjjson

# 定义一个局部变量，获取json所有的节点
    def get_jsonele_change(self, rlt):
            self.rlt_hjjson={}
            return self.get_jsonele(rlt)

#获取统一接口返回的json
    def get_apiResultJson(self,api,inputxml):
        self.api = api
        self.rlt = self.api(inputxml)
        print(self.rlt)
        self.rlt_json = json.loads(self.rlt)
        # print(type(self.rlt_json),self.rlt_json)
        return self.get_jsonele_change(self.rlt_json)

# 比较json
    def compareJson(self,api,inputxml,outjson):
        self.api = eval(api)
        # self.api=api
        self.inputxml = inputxml
        self.outjson = outjson
        self.api_result = self.get_apiResultJson(self.api, self.inputxml)
        self.standard_result = self.get_jsonele_change(outjson)
        # self.print_resultjson(self.api_result, self.standard_result)
        # print(self.api_result,'\n',self.standard_result)
        self.print_result(self.api_result, self.standard_result)


#打印比对结果
    def print_result(self,rlt,s_rlt):

        # print('rlt:%s,"\n"s_rlt:%s'%(rlt,s_rlt))
        print("比标准出参多出来的节点如下>>>>>>>>>>>>>>>>>")
        self.rlt1 = set(rlt) - set(s_rlt)
        if self.rlt1 == set():
            print('没有多余的节点')
        else:
            for i in self.rlt1:
                print(i)

        print("比标准出参少的节点如下>>>>>>>>>>>>>>>>>")
        self.rlt2 = set(s_rlt) - set(rlt)
        if self.rlt2 == set():
            print('没有缺少的节点')
        else:
            for i in self.rlt2:
                print(i)

        print("与标准出参类型不一致的节点如下>>>>>>>>>>>>>>>>>")
        try:
            for i in s_rlt:
                if i in rlt and s_rlt[i] != 'None':
                    if type(s_rlt[i])not in (dict,list):          #此判断排除json中根节点的比较
                        # print(self.standard_result[i],self.api_result[i])
                        if eval(s_rlt[i]) != type(rlt[i]):
                            print('节点名称:%s,标准出参类型:%s,实际出参类型:%s' % (i.ljust(20), s_rlt[i].ljust(20), type(rlt[i])))
        except Exception as e:
            print(e)





if __name__=="__main__":
      # cr=CompareResult()
      # cr.compareJson(hj.hj_v4,cf.hjopt_inputpath,cf.hjopt_out_new)
      # cr.compareJson(hj.hj_v4, cf.hjipt_inputpath, cf.hjipt_out_new)
    cropt = CompareResult()
    cropt.compareXML(sf.sf_audit_center, cf.sfopt_center_inputpath, cf.sfopt_center_outputpath)

# cropt.compareXML(hj.hj_v4, cf.hjipt_inputpath, cf.hjipt_out_xml)
    # cropt.compareXML_sf(inputxml3,outputxml3)
    # cropt.compareXML(gy.gy_v4,cf.gyopt_inputpath,cf.gyopt_outputpath)
    # cropt.compareXML(sf.sf_audit_center_json, cf.sfopt_center_inputpath, cf.sfopt_center_outputpath)
    # cropt.compareXML(gy.gy_v4, inputxml2, outputxml2)
#     cropt.compareXML_sf(inputxml3,outputxml3)

