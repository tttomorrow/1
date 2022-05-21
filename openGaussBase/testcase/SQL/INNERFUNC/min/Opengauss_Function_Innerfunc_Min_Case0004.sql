-- @testpoint: inet类型网络地址/子网掩码/主机地址组合测试取最小值--ipv4

--step1:创建表; expect:成功
drop table if exists t_min_case0004;
create table t_min_case0004(id int, i inet);

--step2:网络地址/子网掩码相同，主机地址不同; expect:122.5.5.3/26
insert into t_min_case0004 values(1,'122.5.5.3/26'),(2,'122.5.5.9/26');
select min(i) from  t_min_case0004;

--step3:网络地址/子网掩码相同，主机地址相同; expect:1,'128.255.254.3/26'
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.254.3/26'),(2,'128.255.254.3/26');
select min(i) from  t_min_case0004;

--step4:子网掩码不同:网络地址（子网掩码同长度部分相同，不同部分不相同），; expect:128.255.255.3/19
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.255.3/19'),(2,'128.255.224.0/26');
select min(i) from  t_min_case0004;

--step5:子网掩码不同:网络地址（子网掩码同长度部分不相同），; expect:128.255.255.3/19
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.255.3/19'),(2,'129.255.224.0/26');
select min(i) from  t_min_case0004;

--step6:网络地址不同，子网掩码相同，; expect:128.255.255.3/19
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.255.3/19'),(2,'129.255.224.0/19');
select min(i) from  t_min_case0004;

--step7:网络地址不同，子网掩码不同，主机地址相同; expect:128.255.224.3/19
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.224.3/19'),(2,'129.255.224.3/26');
select min(i) from  t_min_case0004;

--step8:网络地址不同，子网掩码不同，主机地址不相; expect:126.255.224.255/26
delete from t_min_case0004;
insert into t_min_case0004 values(1,'128.255.224.0/19'),(2,'126.255.224.255/26');
select min(i) from  t_min_case0004;

--step9:全1地址与全0地址; expect:0.0.0.0
delete from t_min_case0004;
insert into t_min_case0004 values(1,'255.255.255.255'),(2,'0.0.0.0');
select min(i) from  t_min_case0004;

--tearDown
drop table if exists t_min_case0004;