--  @testpoint:openGauss保留关键字current_time同时作为表名和列名带引号,并使用该列结合limit排序,current_time列的值按字母大小排序且只显示前2条数据
drop table if exists "current_time";
create table "current_time"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"current_time" varchar(100) default 'current_time'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--清理表数据
delete from "current_time";

--插入数据
insert into "current_time"(c_id,"current_time") values(1,'hello');
insert into "current_time"(c_id,"current_time") values(2,'china');
insert into "current_time"(c_id,"current_time") values(3,'gauss');

--查看表数据
select "current_time" from "current_time" where "current_time"!='hello' order by "current_time" limit 2 ;

--清理环境
drop table "current_time";