--  @testpoint:openGauss关键字clean(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,clean列的值按字母大小排序且只显示前2条数据
--创建表
drop table if exists "clean";
create table "clean"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"clean" varchar(100) default 'clean'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--清除表数据
delete from "clean";

--向保重插入数据
insert into "clean"(c_id,"clean") values(1,'hello');
insert into "clean"(c_id,"clean") values(2,'china');
insert into "clean"(c_id,"clean") values(3,'gauss');

--查看表内容
select "clean" from "clean" where "clean"!='hello' order by "clean" limit 2 ;

--清除环境
drop table "clean";
