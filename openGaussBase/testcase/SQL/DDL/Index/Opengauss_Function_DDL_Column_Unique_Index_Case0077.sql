-- @testpoint: 列存普通表，修改时指定字段约束deferrable,合理报错

--测试点一:创建列存普通表，增加主键约束且指定字段约束可推迟，重复插入相同数据
--step1:测试点一,创建列存普通表   expect:成功
drop table if exists t_columns_unique_index_0077_01;
create table t_columns_unique_index_0077_01(id1 int,id2 integer) with(orientation=column);

--step2:测试点一,给表中字段增加主键约束，指定字段约束可推迟   expect:失败
alter table t_columns_unique_index_0077_01 add primary key(id1) deferrable initially deferred;

--step3:测试点一,清理环境   expect:成功
drop table t_columns_unique_index_0077_01 cascade;


--测试点二:创建列存普通表，增加唯一约束且指定字段约束不可推迟，重复插入相同数据
--step1:测试点二,创建列存普通表,指定字段约束不可推迟   expect:成功
drop table if exists t_columns_unique_index_0077_02;
create table t_columns_unique_index_0077_02(id1 smallint, id2 integer) with(orientation=column);

--step2:测试点二,给表中字段增加唯一约束，指定字段约束不可推迟   expect:失败
alter table t_columns_unique_index_0077_02 add constraint const_77 unique(id1) deferrable initially deferred;

--step3:测试点二,清理环境   expect:成功
drop table t_columns_unique_index_0077_02 cascade;

