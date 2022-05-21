--  @testpoint:openGauss关键字contains(非保留)，作为列名带引号并且更新时使用该列，建表成功，contains的值更新为100

drop table if exists contains_test;
create table contains_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"contains" varchar(100) default 'contains'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into contains_test(c_id,"contains") values(1,'hello');
update contains_test set "contains"=100;
select * from contains_test order by "contains";

drop table contains_test;