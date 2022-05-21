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
Case Type   : tools
Case Name   : 使用gaussdb指定-W的值单位为分钟启动数据库，启动后等待时间是否为指定时间
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_luz/cluster/dn1
    2.使用gaussdb工具指定-W启动数据库
    gaussdb  -D /opt/openGauss_zl/cluster/dn1 -p 19701 -W 1min &
    3.连接数据库，检验等待时间是否为1分钟
    gsql -d postgres -p 19701 -r
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具指定-W启动数据库成功
    3.连接数据库时并未立即间接成功，等待时间为1min，与设置值一致，-W参数设置成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0077 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_systools(self):
        self.logger.info('-------若为主备环境，后续不执行-------')
        excute_cmd = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg0 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg0)
        if 'Standby' in msg0:
            self.logger.info('主备环境，后续不执行!')
        else:
            self.logger.info('--------关闭正在运行的数据库--------')
            excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                          f'{self.DB_INSTANCE_PATH}'
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info('-------使用gaussdb工具后台运行进程--------')
            excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                          f'gaussdb -D {self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -W 1min'
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            self.logger.info('------------连接数据库-----------')
            sql_cmd3 = 'drop user if exists user006 cascade;'
            msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
            self.logger.info(msg3)
            self.assertTrue(msg3.find('DROP ROLE') > -1)
            self.logger.info('----------查看环境是否主备，主备需恢复状态---------')
            check_status_cmd = f'source {self.DB_ENV_PATH};gs_om -t status ' \
                               f'--detail'
            check_status_msg = self.userNode.sh(check_status_cmd).result()
            self.logger.info(check_status_msg)
            if 'Standby' in check_status_msg:
                self.logger.info('------------恢复主备集群状态-----------')
                excute_cmd6 = f'source {self.DB_ENV_PATH};gs_ctl restart ' \
                              f'-D \'{self.DB_INSTANCE_PATH}\'-M primary'
                msg6 = self.userNode.sh(excute_cmd6).result()
                self.logger.info(msg6)
            else:
                self.logger.info('单机环境不需要恢复')
            excute_cmd7 = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
            msg7 = self.userNode.sh(excute_cmd7).result()
            self.logger.info(msg7)
            if 'Standby' in msg7:
                self.logger.info('-----------检查主备状态正常----------')
                self.assertTrue(
                    'P Primary Normal' in msg7 and 'S Standby Normal' in msg7)
            else:
                self.logger.info('-----------检查单机状态正常----------')
                self.assertTrue('P Primary Normal' in msg7)


def tearDown(self):
    self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0077 finish')
