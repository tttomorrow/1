--  @testpoint:openGauss保留关键字user同时作为表名和列名带引号，并进行dml操作,user列的值最终显示为1000
drop table if exists "user";
create table "user"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"user" varchar(100) default 'user'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "user"(c_id,"user") values(1,'hello');
insert into "user"(c_id,"user") values(2,'china');
update "user" set "user"=1000 where "user"='hello';
delete from "user" where "user"='china';
select "user" from "user" where "user"!='hello' order by "user";

drop table "user";