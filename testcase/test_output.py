# -*- coding: utf-8 -*-
# @Time : 2020/3/5 23:04
# @Author : wangmengmeng
import pytest
import xmltodict
import time
from config.cfg import url_normal, url_cancel


class TestIpt:
    @pytest.mark.parametrize("xmlname,expected,despensing_num",
                             [('ipt_return_drug', '-1', '-1.0'), ('ipt_stop', '4', '1.0'),('ipt_new', '0', '1.0')])
    def test_ipt_0(self, get_conn, send, xmlname, expected, despensing_num):
        """药嘱新开、退药和停止"""
        send.post_xml(url_normal, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['orders']['medical_order_item']['order_status'] == expected
        assert xmltodict.parse(content)['root']['orders']['medical_order_item']['despensing_num'] == despensing_num
        if expected == '-1':
            assert not xmltodict.parse(content)['root']['orders']['medical_order_item']['drug_return_flag']
        elif expected == '4':
            assert not xmltodict.parse(content)['root']['orders']['medical_order_item']['stop_flag']
        else:
            assert not xmltodict.parse(content)['root']['orders']['medical_order_item']['drug_return_flag']
            assert not xmltodict.parse(content)['root']['orders']['medical_order_item']['stop_flag']


    @pytest.mark.parametrize("xmlname,expected", [('ipt_cancel', '2')])
    def test_ipt_2(self, get_conn, send, xmlname, expected):
        """药嘱删除"""
        send.post_xml(url_cancel, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['orders']['medical_order_item']['order_status'] == expected
        assert xmltodict.parse(content)['root']['orders']['medical_order_item']['order_id'] == 'o1_' + filename
        assert xmltodict.parse(content)['root']['orders']['medical_order_item']['group_no'] == filename


class TestHerb:
    @pytest.mark.parametrize("xmlname,expected,despensing_num",
                             [('herb_return_drug', '-1', '-7.0'), ('herb_stop', '4', '7.0'),('herb_new', '0', '7.0')])
    def test_herb_0(self, get_conn, send, xmlname,expected,despensing_num):
        """草药新开、退药和停止"""
        send.post_xml(url_normal, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                   'order_status'] == expected
        assert xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_item'][
                   'despensing_num'] == despensing_num
        if expected == '-1':
            assert not xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                       'drug_return_flag']
        elif expected == '4':
            assert not xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                'stop_flag']
        else:
            assert not xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                'drug_return_flag']
            assert not xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                'stop_flag']



    @pytest.mark.parametrize("xmlname,expected", [('herb_cancel', '2')])
    def test_herb_1(self, get_conn, send, xmlname, expected):
        """草药撤销"""
        send.post_xml(url_cancel, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                   'order_status'] == expected
        assert xmltodict.parse(content)['root']['orders']['herb_medical_order']['herb_medical_order_info'][
                   'order_id'] == 'co4_' + filename


class TestOpt:
    @pytest.mark.parametrize("xmlname,expected", [('opt_new', '0')])
    def test_opt_0(self, get_conn, send, xmlname, expected):
        """原始正常状态，改成新版新开处方状态"""
        send.post_xml(url_normal, xmlname)
        time.sleep(3)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_info'][
                   'recipe_status'] == expected

    @pytest.mark.parametrize("xmlname,expected", [('opt_zuofei', '2'), ('opt_delete', '2')])
    def test_opt_1(self, get_conn, send, xmlname, expected):
        """原作废处方、删除处方都按新版删除处方处理，注意以下是新版本入参，旧版本4.1的接口文档缺少recipe_doc_id、recipe_doc_name
            原始处方退药状态,全退（无明细），此时会被接口拦截 ('opt_return_drug_1', '2')
        <root>
          <base>
            <hospital_code><![CDATA[H0003]]></hospital_code>
            <patient_id><![CDATA[{{mzhzh}}]]></patient_id>
            <event_no><![CDATA[{{mzhzh}}]]></event_no>
            <source><![CDATA[急诊]]></source>
          </base>
          <opt_prescriptions>
            <opt_prescription>
              <opt_prescription_info>
                <recipe_id><![CDATA[rd1_{{ts}}]]></recipe_id>
                <recipe_no><![CDATA[r1_{{ts}}]]></recipe_no>
                <recipe_doc_id><![CDATA[09]]></recipe_doc_id>
                <recipe_doc_name><![CDATA[医生王]]></recipe_doc_name>
                <recipe_status><![CDATA[2]]></recipe_status>
              </opt_prescription_info>
         </opt_prescription>
        </opt_prescriptions>
        </root>
        """
        if xmlname == 'opt_delete':  # 对旧的3.5版本作废走的是正常接口、删除走的删除接口，现两个作废和删除都要走删除接口
            send.post_xml(url_cancel, xmlname)
        else:
            send.post_xml(url_normal, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_info'][
                   'recipe_id'] == 'r1_' + filename
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_info'][
                   'recipe_no'] == 'r1_' + filename
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_info'][
                   'recipe_status'] == expected

    @pytest.mark.parametrize("xmlname,expected", [('opt_return_drug_2', '-1')])
    def test_opt_2(self, get_conn, send, xmlname, expected):
        """原全部退药状态，全退(有明细)，按新版退药处理"""
        send.post_xml(url_normal, xmlname)
        time.sleep(1)
        filename = send.change_data['{{ts}}']
        stdout = get_conn.exec_command('cat /tmp/hisresult/2020-03-09/H0003/receive_path/{}*.txt'.format(filename))[1]
        content = stdout.read()
        print(content)
        print(content.decode('utf-8'))
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_info'][
                   'recipe_status'] == expected
        assert xmltodict.parse(content)['root']['opt_prescriptions']['opt_prescription']['opt_prescription_item'][
                   'despensing_num'] == '-3.0'
