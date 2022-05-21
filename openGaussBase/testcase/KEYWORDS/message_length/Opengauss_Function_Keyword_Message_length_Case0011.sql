--  @testpoint:openGauss关键字message_length(非保留)，同时作为表名和列名带引号，并进行dml操作,message_length列的值最终显示为1000

drop table if exists "message_length";
create table "message_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"message_length" varchar(100) default 'message_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "message_length"(c_id,"message_length") values(1,'hello');
insert into "message_length"(c_id,"message_length") values(2,'china');
update "message_length" set "message_length"=1000 where "message_length"='hello';
delete from "message_length" where "message_length"='china';
select "message_length" from "message_length" where "message_length"!='hello' order by "message_length";

drop table "message_length";

