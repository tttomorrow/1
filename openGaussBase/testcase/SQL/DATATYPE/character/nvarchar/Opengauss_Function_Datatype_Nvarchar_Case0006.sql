-- @testpoint: 行存普通表-NVARCHAR(n)的约束\索引\表操作测试 部分测试点合理报错

--step1:建表; expect:成功
drop schema if exists s_schema_0006 cascade;
create schema s_schema_0006;
create table s_schema_0006.t_nvarchar_0006_01(c_nvarchar nvarchar PRIMARY KEY);
create table s_schema_0006.t_nvarchar_0006_02(c_nvarchar nvarchar);

--step2:约束测试; expect:成功
--增加/删除唯一约束:成功
alter table s_schema_0006.t_nvarchar_0006_02 add constraint t_nvarchar_0006_02_c_nvarchar_key unique(c_nvarchar);
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values('test'),('test');
alter table s_schema_0006.t_nvarchar_0006_02 drop constraint t_nvarchar_0006_02_c_nvarchar_key;
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values('test'),('test');
truncate s_schema_0006.t_nvarchar_0006_02;
--增加/删除NOT NULL约束:成功
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar not null;
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values(null);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar NULL;
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values(null);
truncate s_schema_0006.t_nvarchar_0006_02;
--增加/删除默认约束:成功
alter table s_schema_0006.t_nvarchar_0006_02 alter c_nvarchar set default 'test0006';
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values(default);
select c_nvarchar from s_schema_0006.t_nvarchar_0006_02;
truncate s_schema_0006.t_nvarchar_0006_02;
alter table s_schema_0006.t_nvarchar_0006_02 alter c_nvarchar drop default;
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values(default);
select c_nvarchar from s_schema_0006.t_nvarchar_0006_02;
truncate s_schema_0006.t_nvarchar_0006_02;
--增加/删除检查约束:成功
alter table s_schema_0006.t_nvarchar_0006_02 add constraint t_nvarchar_0006_02_c_nvarchar_key check (c_nvarchar='test');
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values('test0006');
alter table s_schema_0006.t_nvarchar_0006_02 drop constraint t_nvarchar_0006_02_c_nvarchar_key;
insert into s_schema_0006.t_nvarchar_0006_02(c_nvarchar) values('test0006');
select c_nvarchar from s_schema_0006.t_nvarchar_0006_02;
--增加/删除主外键约束:成功
alter table s_schema_0006.t_nvarchar_0006_02 add constraint t_nvarchar_0006_02_c_nvarchar_key  primary key (c_nvarchar);
alter table s_schema_0006.t_nvarchar_0006_02 add column c_nvarchar1 nvarchar;
alter table s_schema_0006.t_nvarchar_0006_02 add constraint t_nvarchar_0006_02_c_nvarchar_fkey  foreign key (c_nvarchar1) references s_schema_0006.t_nvarchar_0006_01(c_nvarchar);
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0006_02') order by conname;
alter table s_schema_0006.t_nvarchar_0006_02 drop constraint t_nvarchar_0006_02_c_nvarchar_key cascade;
alter table s_schema_0006.t_nvarchar_0006_02 drop constraint t_nvarchar_0006_02_c_nvarchar_fkey cascade;
alter table s_schema_0006.t_nvarchar_0006_01 drop constraint "t_nvarchar_0006_01_pkey" cascade;
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0006_02') order by conname;

--step3:索引; expect:成功
create index index_0006_01 on s_schema_0006.t_nvarchar_0006_02(c_nvarchar,c_nvarchar1);
create index index_0006_02 on s_schema_0006.t_nvarchar_0006_02 using gin(to_tsvector('english', c_nvarchar));

--step4:表操作; expect:成功
--增删字段:成功
alter table s_schema_0006.t_nvarchar_0006_02 drop column c_nvarchar1;
alter table s_schema_0006.t_nvarchar_0006_02 add column c_nvarchar1 nvarchar;
--修改字段长度:成功
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(200);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(1048576);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(1048575);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(1048577);
--修改字段类型:成功
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar2(100);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(150);
alter table s_schema_0006.t_nvarchar_0006_02 add constraint t_nvarchar_0006_02_c_nvarchar_key unique(c_nvarchar);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar2(100);
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 text;
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 clob;
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 char;
alter table s_schema_0006.t_nvarchar_0006_02 modify c_nvarchar1 nvarchar(150);

--step5:sql操作; expect:成功
insert into s_schema_0006.t_nvarchar_0006_02 values (1::nvarchar),(2::nvarchar),(3::nvarchar),(4::nvarchar),(5::nvarchar);
select * from s_schema_0006.t_nvarchar_0006_02;
update s_schema_0006.t_nvarchar_0006_02 set c_nvarchar = 'test' where c_nvarchar='1';
select * from s_schema_0006.t_nvarchar_0006_02;
delete from s_schema_0006.t_nvarchar_0006_02 where c_nvarchar = '2';
select * from s_schema_0006.t_nvarchar_0006_02;
--upsert:成功
truncate s_schema_0006.t_nvarchar_0006_02;
insert into s_schema_0006.t_nvarchar_0006_02 values ('a','test0006');
select * from s_schema_0006.t_nvarchar_0006_02 where c_nvarchar = 'a';
insert into s_schema_0006.t_nvarchar_0006_02 values ('a','test0006_01') on duplicate key update c_nvarchar1='test0006_01';
select * from s_schema_0006.t_nvarchar_0006_02 where c_nvarchar = 'a';

--step6:清理环境; expect:成功
drop table if exists s_schema_0006.t_nvarchar_0006_01 cascade;
drop table if exists s_schema_0006.t_nvarchar_0006_02 cascade;
drop schema if exists s_schema_0006;
