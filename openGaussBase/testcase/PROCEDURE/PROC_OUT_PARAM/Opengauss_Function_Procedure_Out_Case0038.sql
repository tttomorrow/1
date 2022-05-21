-- @testpoint: 仅带出参，出参类型为bool，并且将出参赋给类型为decimal(8,2)的变量的的存储过程

--step1：创建表并插入数据; expect: 成功
drop table if exists test_001;
create table test_001(
  t1 int,
  t2 integer not null,
  t3 bigint,
  t4 number default 0.2332,
  t5 number(12,2),
  t6 number(12,6),
  t7 binary_double,
  t8 decimal,
  t9 decimal(8,2),
  t10 decimal(8,4),
  t11 real,
  t12 char(4000),
  t13 char(100),
  t14 varchar(4000),
  t15 varchar(100),
  t16 varchar2(4000),
  t17 numeric,
  t19 date,
  t20 timestamp,
  t21 timestamp(6),
  t22 bool
) ;

create unique index  indx_out_param_t1 on test_001(t1);
create index indx_out_param_t2 on test_001(t2,t17,t20);

insert into test_001 values(12,58812,546223079,1234567.89,12345.6789,12.3456789,1234.56,2345.67,12345.6789,12.3456789,12.33,'dbcd','abcde','1999-01-01','ab','adc',123.45,'2005-08-08','2000-01-01 15:12:21.11','2000-08-01 15:12:21.32',true);
insert into test_001 values(13,58813,546223078,1234567.78,12345.5678,12.2345678,1234.67,2345.78,12345.5678,12.2345678,12.44,'dbce','abcdf','abcdeg','ac','ade',123.46,'2012-08-08','2000-02-01 15:22:21.11','2012-02-01 15:12:11.32',false);
insert into test_001 values(14,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','2010-02-28','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into test_001 values(15,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into test_001 values(16,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);

--step2:创建仅带出参的存储过程测试（测试出参类型为bool，并且将出参赋给类型为decimal(8,2)的变量的的存储过程; expect: 成功
create or replace procedure proc_out_param_001(p1 out bool)
as
v1 decimal(8,2);
begin
select t22 into v1 from test_001 where t1=12;
raise info 'v1:%',v1;
exception
when no_data_found then raise info 'no_data_found';
end;
/

--step3: 调用存储过程; expect: 成功
declare
v_p1 decimal(8,2);
begin
proc_out_param_001(v_p1);
end;
/

--step4: 清理环境; expect: 清理环境成功
drop procedure proc_out_param_001;
drop table if exists test_001;