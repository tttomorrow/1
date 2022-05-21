--  @testpoint:openGauss关键字timezone_hour(非保留),同时作为表名和列名带引号，建表成功

drop table if exists "timezone_hour" CASCADE;
create table "timezone_hour"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"timezone_hour" varchar(100) default 'timezone_hour'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
select * from "timezone_hour";
drop table "timezone_hour" CASCADE;

