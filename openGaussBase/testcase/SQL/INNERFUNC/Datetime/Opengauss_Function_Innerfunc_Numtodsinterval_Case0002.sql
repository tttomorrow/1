--  @testpoint: numtodsinterval interval_unit为 ’DAY‘兼容格式输出

drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2001-02-16');
SET intervalstyle = a;
SELECT numtodsinterval(100, 'DAY');
select to_date(clo1) + numtodsinterval(100, 'DAY') from test_date01;
drop table if exists test_date01;