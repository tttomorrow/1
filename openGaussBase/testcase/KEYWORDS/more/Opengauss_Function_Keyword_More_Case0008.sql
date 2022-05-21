--  @testpoint:openGauss关键字more(非保留)，作为列名带引号并且删除时使用该列,建表成功，more列值是'hello'的删除成功

drop table if exists explain_test;
create table explain_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"more" varchar(100) default 'more'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into explain_test(c_id,"more") values(1,'hello');
insert into explain_test(c_id) values(2);
delete from explain_test where "more"='hello';
select * from explain_test order by "more";
drop table explain_test;


