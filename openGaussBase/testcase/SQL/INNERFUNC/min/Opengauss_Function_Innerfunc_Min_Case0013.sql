-- @testpoint: 非网络类型转换为inet后ipv4地址取最小值

--step1:创建表; expect:成功
drop table if exists t_min_case0013;
create table t_min_case0013(c inet);
create table t_min_case0013_text(t text);
create table t_min_case0013_clob(c clob);
create table t_min_case0013_varchar(c varchar);
create table t_min_case0013_bpchar(c bpchar);
create table t_min_case0013_nvarchar2(c nvarchar2);
create table t_min_case0013_cidr(c cidr);

--step2:text类型转换为inet; expect:192.168.0.1/24
insert into t_min_case0013_text values('192.168.0.1/24'),('192.168.0.0/25'),('192.168.1.0'),('192.168.1.0/25');
insert into t_min_case0013  select inet(t) from t_min_case0013_text;
select min(c) from  t_min_case0013;

--step3:clob类型转换为inet; expect:192.168.255.1/14
delete from t_min_case0013;
insert into t_min_case0013_clob values('192.168.255.1/14'),('192.169.0.0/14');
insert into t_min_case0013  select inet(c) from t_min_case0013_clob;
select min(c) from  t_min_case0013;

--step4:varchar类型转换为inet; expect:9.8.0.0/16
delete from t_min_case0013;
insert into t_min_case0013_varchar values('10.0.0.0/8'),('9.8.0.0/16'),('10.1.0.0/16');
insert into t_min_case0013  select inet(c) from t_min_case0013_varchar;
select min(c) from  t_min_case0013;

--step5:bpchar类型转换为inet; expect:192.168.100.128/25
delete from t_min_case0013;
insert into t_min_case0013_bpchar values('192.168.100.128/25'),('192.168.100.128');
insert into t_min_case0013  select inet(c) from t_min_case0013_bpchar;
select min(c) from  t_min_case0013;

--step6:nvarchar2类型转换为inet; expect:10.1.2.3/32
delete from t_min_case0013;
insert into t_min_case0013_nvarchar2 values('10.1.2.3/32'),('10.1.2.12'),('10.1.2.12/30');
insert into t_min_case0013  select inet(c) from t_min_case0013_nvarchar2;
select min(c) from  t_min_case0013;

--step7:cidr类型转换为inet; expect:10.1.2.3/32
delete from t_min_case0013;
insert into t_min_case0013_cidr values('10.1.2.3/32'),('10.1.2.12/31'),('10.1.2.12/30');
insert into t_min_case0013  select inet(c) from t_min_case0013_cidr;
select min(c) from  t_min_case0013;

--tearDown
drop table if exists t_min_case0013;
drop table if exists t_min_case0013_text;
drop table if exists t_min_case0013_clob;
drop table if exists t_min_case0013_varchar;
drop table if exists t_min_case0013_bpchar;
drop table if exists t_min_case0013_nvarchar2;
drop table if exists t_min_case0013_cidr;