--  @testpoint:openGauss关键字diagnostics(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,diagnostics列的值按字母大小排序且只显示前2条数据

drop table if exists "diagnostics";
create table "diagnostics"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"diagnostics" varchar(100) default 'diagnostics'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
delete from "diagnostics";
insert into "diagnostics"(c_id,"diagnostics") values(1,'hello');
insert into "diagnostics"(c_id,"diagnostics") values(2,'china');
insert into "diagnostics"(c_id,"diagnostics") values(3,'gauss');
select "diagnostics" from "diagnostics" where "diagnostics"!='hello' order by "diagnostics" limit 2 ;

drop table "diagnostics";

