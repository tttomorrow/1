-- @testpoint: 创建序列同义词，创建成功，使用时合理报错
--创建序列
drop SEQUENCE if exists s_SYN_061 cascade;
CREATE SEQUENCE s_SYN_061;
SELECT nextval('s_SYN_061');
--创建同义词
drop synonym if exists SYN_061;
CREATE synonym SYN_061 for s_SYN_061;
--调用nextval函数，报错
SELECT nextval('SYN_061');
--清理环境
drop SEQUENCE if exists s_SYN_061 cascade;
drop synonym if exists SYN_061;
