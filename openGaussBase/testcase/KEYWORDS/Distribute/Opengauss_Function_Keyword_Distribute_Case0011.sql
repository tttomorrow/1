--  @testpoint:openGauss关键字distribute(非保留)，同时作为表名和列名带引号，并进行dml操作,distribute列的值最终显示为1000

drop table if exists "distribute";
create table "distribute"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"distribute" varchar(100) default 'distribute'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "distribute"(c_id,"distribute") values(1,'hello');
insert into "distribute"(c_id,"distribute") values(2,'china');
update "distribute" set "distribute"=1000 where "distribute"='hello';
delete from "distribute" where "distribute"='china';
select "distribute" from "distribute" where "distribute"!='hello' order by "distribute";

drop table "distribute";

