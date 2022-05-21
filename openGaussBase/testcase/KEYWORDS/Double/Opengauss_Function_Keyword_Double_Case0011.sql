--  @testpoint:openGauss关键字double(非保留)，同时作为表名和列名带引号，并进行dml操作,double列的值最终显示为1000

drop table if exists "double";
create table "double"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"double" varchar(100) default 'double'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "double"(c_id,"double") values(1,'hello');
insert into "double"(c_id,"double") values(2,'china');
update "double" set "double"=1000 where "double"='hello';
delete from "double" where "double"='china';
select "double" from "double" where "double"!='hello' order by "double";

drop table "double";

