--  @testpoint:openGauss关键字replace(非保留)，作为列名带引号并且更新时使用该列，建表成功，replace的值更新为100

drop table if exists replace_test;
create table replace_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"replace" varchar(100) default 'replace'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into replace_test(c_id,"replace") values(1,'hello');
update replace_test set "replace"=100;
select * from replace_test order by "replace";

drop table replace_test;