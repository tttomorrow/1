-- @testpoint: 创建列存表,验证字符串类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为字符类型，指定主键约束
--step1:测试点一,创建列存普通表,字段类型为字符类型,指定主键约束   expect:成功
drop table if exists t_columns_unique_index_0085_01;
create table t_columns_unique_index_0085_01(
name1 varchar(10), name2 char(10), name3 char, name4 text, name5 nvarchar2,
primary key(name1,name2,name3,name4,name5)) with(orientation=column);

--step2:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0085_01 values('good','very good','a','primary','unique');

--step3:测试点一,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0085_01 values('good','very good','a','primary','unique');

--step4:测试点一,清理环境    expect:成功
drop table t_columns_unique_index_0085_01;


--测试点二:创建列存普通表，字段类型为字符类型，指定唯一约束
--step1:测试点二,创建列存普通表,字段类型为字符类型,指定唯一约束   expect:成功
drop table if exists t_columns_unique_index_0085_02;
create table t_columns_unique_index_0085_02(
name1 varchar(10), name2 char(10), name3 char, name4 text, name5 nvarchar2,
constraint const_85 unique(name1,name2,name3,name4,name5)) with(orientation=column);

--step2:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0085_02 values('good','very good','a','primary','unique');

--step3:测试点二,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0085_02 values('good','very good','a','primary','unique');

--step4:测试点二,清理环境    expect:成功
drop table t_columns_unique_index_0085_02;


--测试点三:创建列存普通表，字段类型为字符类型，创建唯一索引
--step1:测试点三,创建列存普通表,字段类型为字符类型   expect:成功
drop table if exists t_columns_unique_index_0085_03;
create table t_columns_unique_index_0085_03(
name1 varchar(10), name2 char(10), name3 char, name4 text, name5 nvarchar2,
primary key(name1,name2,name3,name4,name5)) with(orientation=column);

--step2:创建唯一索引   expect:成功
create unique index i_columns_unique_index_0085 on t_columns_unique_index_0085_03 using btree(name1,name2,name3,name4,name5);

--step2:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0085_03 values('good','very good','a','primary','unique');

--step3:测试点三,再次插入重复数据   expect:失败
insert into t_columns_unique_index_0085_03 values('good','very good','a','primary','unique');

--step4:测试点三,清理环境    expect:成功
drop table t_columns_unique_index_0085_03;



