-- @testpoint: Hash分区表结合列约束（default）默认值和数据类型不匹配 合理报错

--step1：创建hash分区表 expect：合理报错
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                        number(7)  default 'aaa',
 use_filename               varchar2(20) ,
 filename                   varchar2(255),
 text                       varchar2(2000)
 )
partition by hash(id)
(partition p1,
 partition p2);