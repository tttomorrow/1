-- @testpoint: 创建列存表,修改字段约束,验证字符类型对主键/唯一约束/唯一索引的支持,部分step合理报错

--测试点一:创建列存普通表，字段类型为数值型，新增字段唯一约束
--step1:测试点一,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0086_01;
create table t_columns_unique_index_0086_01(
name1 varchar(10), name2 char(10), name3 char, 
name4 text, name5 nvarchar2) with(orientation=column);

--step2:测试点一,修改新增字段的约束为唯一约束   expect:成功
alter table t_columns_unique_index_0086_01 add constraint const_86_1 unique(name1);
alter table t_columns_unique_index_0086_01 add constraint const_86_2 unique(name2);
alter table t_columns_unique_index_0086_01 add constraint const_86_3 unique(name3);
alter table t_columns_unique_index_0086_01 add constraint const_86_4 unique(name4);
alter table t_columns_unique_index_0086_01 add constraint const_86_5 unique(name5);
alter table t_columns_unique_index_0086_01 add constraint const_86_6 unique(name1,name2,name3,name4,name5);

--step3:测试点一,插入数据   expect:成功
insert into t_columns_unique_index_0086_01 values('good','very good','a','primary','unique');

--step4:测试点一,再次插入数据   expect:失败
insert into t_columns_unique_index_0086_01 values('good','very good','a','primary','unique');

--step5:清理环境   expect:成功
drop table t_columns_unique_index_0086_01;



--测试点二:创建列存普通表，字段类型为数值型，新增字段主键约束
--step1:测试点二,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0086_02;
create table t_columns_unique_index_0086_02(
name1 varchar(10), name2 char(10), name3 char,
name4 text, name5 nvarchar2) with(orientation=column);

--step2:测试点二,修改新增字段的约束为主键约束   expect:成功
alter table t_columns_unique_index_0086_02 add primary key(name1,name2,name3,name4,name5);

--step3:测试点二,插入数据   expect:成功
insert into t_columns_unique_index_0086_02 values('good','very good','a','primary','unique');

--step4:测试点二,再次插入数据   expect:失败
insert into t_columns_unique_index_0086_02 values('good','very good','a','primary','unique');

--step5:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0086_02;



--测试点三:创建列存普通表，字段类型为数值型，为字段新增唯一索引
--step1:测试点三,创建列存表，字段类型为支持的数值类型   expect:成功
drop table if exists t_columns_unique_index_0086_03;
create table t_columns_unique_index_0086_03(
name1 varchar(10), name2 char(10), name3 char,
name4 text, name5 nvarchar2) with(orientation=column);

--step2:测试点三,新增唯一索引   expect:成功
create unique index i_columns_unique_index_0086_01 on t_columns_unique_index_0086_03 using btree(name1);
create unique index i_columns_unique_index_0086_02 on t_columns_unique_index_0086_03 using btree(name2);
create unique index i_columns_unique_index_0086_03 on t_columns_unique_index_0086_03 using btree(name3);
create unique index i_columns_unique_index_0086_04 on t_columns_unique_index_0086_03 using btree(name4);
create unique index i_columns_unique_index_0086_05 on t_columns_unique_index_0086_03 using btree(name5);
create unique index i_columns_unique_index_0086_06 on t_columns_unique_index_0086_03 using btree(name1,name2,name3,name4,name5);

--step3:测试点三,插入数据   expect:成功
insert into t_columns_unique_index_0086_03 values('good','very good','a','primary','unique');

--step4:测试点三,再次插入数据   expect:失败
insert into t_columns_unique_index_0086_03 values('good','very good','a','primary','unique');

--step5:测试点三,清理环境   expect:成功
drop table t_columns_unique_index_0086_03;
