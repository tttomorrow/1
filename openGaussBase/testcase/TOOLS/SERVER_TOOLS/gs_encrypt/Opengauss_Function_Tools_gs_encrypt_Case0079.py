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
Case Type   : 服务端工具
Case Name   : gs_encrypt工具组合使用参数--vector，--file-prefix,--vector-base64
              加密明文字符串
Description :
    1.生成16位字符串以base64方式编码的密文；
      base64.b64encode([用户输入的16位字符串].encode(encoding='utf-8'))
    2.执行命令，生成加密文件cipher，rand到$GAUSSHOME/bin目录下；
      gs_guc generate -S [用户输入的口令] -D [$GAUSSHOME/bin目录]
      -o [用户指定的加密文件前缀名]
    3.执行命令，组合使用参数--vector，--file-prefix,--vector-base64加密字符串
      gs_encrypt --vector=[用户输入的盐值] --file-prefix=
      [用户指定的加密文件前缀名] --vector-base64=[用户输入字符串编码的密文]
      [待加密明文字符串]
    4.清理环境
Expect      :
    1.成功生成密文；
    2.成功生成文件；
    3.执行失败，报错提示密钥必须和盐值一起指定
    4.清理环境成功
History     :
"""

import os
import base64
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class GsEncrypt60(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.common = Common()
        self.Constant = Constant()
        self.prefix = 'test'
        self.file_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                      'app', 'bin')
        self.cipher_path = os.path.join(self.file_path, f'{self.prefix}.key.'
                                        f'cipher')
        self.rand_path = os.path.join(self.file_path, f'{self.prefix}.key.'
                                      f'rand')

    def test_gs_encrypt(self):
        self.logger.info('-----进行加密操作-----')
        step = "step1:生成16位字符串以base64方式编码的密文 except:成功生成密文"
        self.logger.info(step)
        encrypt = 'ff$$R44'
        rand = '12gg##GGgggggggg'
        enc = rand.encode(encoding='utf-8')
        vec = base64.b64encode(enc)
        self.assertEqual(type(vec), bytes, step)

        step = "step2:执行命令，在$GAUSSHOME/bin目录下生成加密文件cipher，" \
               "rand except:成功生成文件"
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_guc generate -S {encrypt} -D {self.file_path} -o \
            {self.prefix};
            ls {self.file_path}'''
        self.logger.info(check_cmd1)
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        self.assertTrue(f'{self.prefix}.key.cipher' in msg1
                        and f'{self.prefix}.key.rand' in msg1,
                        "生成失败" + step)

        step = "step3:.执行命令，组合使用参数--vector，--file-prefix," \
               "--vector-base64加密明文字符串 " \
               "except:step3执行失败，报错提示报错提示密钥必须和盐值一起指定"
        self.logger.info(step)
        self.vec_spl = str(vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --vector={rand} --file-prefix={self.prefix}\
            --vector-base64={self.vec_spl} {self.prefix}'''
        self.logger.info(check_cmd1)
        self.logger.info("-----加密结果-----")
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        self.assertIn(self.Constant.secure_false, msg1, "执行失败" + step)

    def tearDown(self):
        step = 'step4:清理环境 except:清理环境成功'
        self.logger.info(step)
        del_file = f'''rm -rf {self.cipher_path};
            rm -rf {self.rand_path}'''
        self.logger.info(del_file)
        self.common.get_sh_result(self.dbuserNode, del_file)
        for s in [self.cipher_path, self.rand_path]:
            cmd = f'if [ -f {s} ]; then echo "does exists"; ' \
                f'else echo "not exists"; fi'
            file_judgments = self.common.get_sh_result(self.dbuserNode, cmd)
            self.assertIn('not exists', file_judgments, "清理失败" + step)
        self.logger.info('--------------清理完成--------------')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')
