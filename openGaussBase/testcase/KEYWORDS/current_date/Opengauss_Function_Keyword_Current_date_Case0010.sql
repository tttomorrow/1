--  @testpoint:openGauss保留关键字current_date同时作为表名和列名带引号，建表成功
drop table if exists "current_date";
create table "current_date"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"current_date" varchar(100) default 'current_date'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--查看表数据
select "current_date" from "current_date";

--清理环境
drop table "current_date";