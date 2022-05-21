"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : gs_expansion
Case Name   : 互信检查-root用户
Description :
    1、准备扩容所用的XML文件
    2、执行整个扩容流程
Expect      :
    1、准备xml成功
    2、扩容失败，提示root互信不正常
History     :
"""
import os
import re
import unittest

from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Pri_U_SH = CommonSH('PrimaryDbUser')
Node_Num = Pri_U_SH.get_node_num()


@unittest.skipIf(3 > Node_Num, '不满足一主两备环境跳过')
class GsExpansion50(unittest.TestCase):
    def setUp(self):
        self.sh = {'pri_root': CommonSH('PrimaryRoot'),
                   'sta1_user': CommonSH('Standby1DbUser'),
                   'sta2_user': CommonSH('Standby2DbUser')}
        self.log = Logger()
        self.cons = Constant()
        self.com = Common()
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：集群状态正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = '----前置操作：数据库主机解压安装包，以免找不到扩容、建互信脚本 expect: 成功----'
        self.log.info(text)
        cmd = f'cd {os.path.dirname(macro.DB_SCRIPT_PATH)} && ' \
            f'tar -xf openGauss-Package-bak*.tar.gz && ' \
            f'ls {macro.DB_SCRIPT_PATH}|grep gs_sshexkey'
        self.log.info(cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, cmd)
        self.assertEqual(res, 'gs_sshexkey', f'执行失败: {text}')

        text = '----前置操作：破坏主节点root互信 expect: 成功----'
        self.log.info(text)
        self.hosts = (self.sh.get("pri_root").node.ssh_host,
                      self.sh.get("sta1_user").node.ssh_host,
                      self.sh.get("sta2_user").node.ssh_host)
        self.params = {'-f': 'expansion_28_hosts'}
        cmd = f'rm -rf {os.path.join("~", ".ssh", "*")}'
        self.log.info(cmd)
        res = self.com.get_sh_result(self.sh['pri_root'].node, cmd)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 准备扩容所用XML文件(延用安装时xml) expect: 成功----'
        self.log.info(text)
        self.xml_path = macro.DB_XML_PATH

        text = '----step1.1: 一主两备减容一备 expect: 成功----'
        self.log.info(text)
        expect_msg = 'Success to drop the target nodes'
        shell_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout 300
            spawn gs_dropnode -U {Pri_U_SH.node.ssh_user} \
            -G {Pri_U_SH.node.ssh_user} \
            -h {self.sh.get("sta1_user").node.ssh_host}
            expect "*(yes/no)?"
            send "yes\\n"
            expect eof''' + "\nEOF\n"
        self.log.info(shell_cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, shell_cmd)
        self.assertIn(expect_msg, res, f'执行失败: {text}')

        text = '----step2: 执行扩容流程 expect: 扩容失败，提示root互信不正常----'
        self.log.info(text)
        self.expansion_cmd = f'cd {macro.DB_SCRIPT_PATH};' \
            f'source {macro.DB_ENV_PATH}\n' \
            f'./gs_expansion -U {Pri_U_SH.node.ssh_user} ' \
            f'-G {Pri_U_SH.node.ssh_user} -X {macro.DB_XML_PATH} ' \
            f'-h {self.sh.get("sta1_user").node.ssh_host} -L'
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)
        expect = 'Failed to verify SSH trust on these nodes:.* by root'
        regex_res = re.search(expect, res, re.S)
        self.assertIsNotNone(regex_res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text = '----后置操作: 建立root互信 expect: 成功----'
        self.log.info(text)
        ssh_res = self.sh['pri_root'].exec_gs_sshexkey(
            macro.DB_SCRIPT_PATH, *self.hosts, **self.params)

        text = '----后置操作: 执行扩容流程 expect: 成功----'
        self.log.info(text)
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)

        expect = 'Expansion results:.*:.*Success.*Expansion Finish.'
        regex_res1 = re.search(expect, res, re.S)

        text = f'----检查集群状态是否正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res2 = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res2)
        self.assertEqual(len(regex_res2), Node_Num, f'执行失败: {text}')

        self.assertIsNotNone(regex_res1, f'执行失败: {text}')
        self.assertIn('Successfully created SSH trust', ssh_res,
                      f'执行失败: {text}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)
