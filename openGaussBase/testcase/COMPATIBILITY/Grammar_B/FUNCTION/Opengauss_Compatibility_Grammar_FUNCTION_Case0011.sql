-- @testpoint: 时间函数timestamp(单参数)功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入timestamp入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31'')', TIMESTAMP('2003-12-31'));
insert into func_test(functionName, result) values('TIMESTAMP(''20031231'')', TIMESTAMP('20031231'));
insert into func_test(functionName, result) values('TIMESTAMP(20031231)', TIMESTAMP(20031231));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 12:00:00.123456'')', TIMESTAMP('2003-12-31 12:00:00.123456'));
insert into func_test(functionName, result) values('TIMESTAMP(''20000229120000.1234567'')', TIMESTAMP('20000229120000.1234567'));
insert into func_test(functionName, result) values('TIMESTAMP(20000229120000.1234567)', TIMESTAMP(20000229120000.1234567));
insert into func_test(functionName, result) values('TIMESTAMP(20000229120000)', TIMESTAMP(20000229120000));
insert into func_test(functionName, result) values('TIMESTAMP(''9999-12-31'')', TIMESTAMP('9999-12-31'));
insert into func_test(functionName, result) values('TIMESTAMP(''9999-12-31 23:59:59.999999'')', TIMESTAMP('9999-12-31 23:59:59.999999'));
insert into func_test(functionName, result) values('TIMESTAMP(''0000-01-01'')', TIMESTAMP('0000-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''0000-01-01 00:00:00.000001'')', TIMESTAMP('0000-01-01 00:00:00.000001'));

--step3:插入timestamp涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMP(''10000-01-01'')', TIMESTAMP('10000-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''10000-01-01 00:00:00'')', TIMESTAMP('10000-01-01 00:00:00'));
--step4:插入入参为特殊类型的timestamp用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMP(date''2003-01-01'')', TIMESTAMP(date'2003-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(cast(''2007-12-10 23:59:59'' as datetime))', TIMESTAMP(cast('2007-12-10 23:59:59' as datetime)));
insert into func_test(functionName, result) values('TIMESTAMP(null)', TIMESTAMP(null));

--step5:插入非法入参时timestamp执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMP(''2003-13-01'')', TIMESTAMP('2003-13-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-2-29'')', TIMESTAMP('2003-2-29'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 25:00:00'')', TIMESTAMP('2003-12-31 25:00:00'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 23:60:00'')', TIMESTAMP('2003-12-31 23:60:00'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 23:59:60'')', TIMESTAMP('2003-12-31 23:59:60'));
insert into func_test(functionName, result) values('TIMESTAMP(''asdasd'')', TIMESTAMP('asdasd'));
insert into func_test(functionName, result) values('TIMESTAMP(true)', TIMESTAMP(true));
insert into func_test(functionName, result) values('TIMESTAMP(B''1'')', TIMESTAMP(B'1'));

--step6:查看timestamp函数执行结果是否正确;expect:成功
select * from func_test;

--step7:清理环境;expect:成功
drop table if exists func_test;