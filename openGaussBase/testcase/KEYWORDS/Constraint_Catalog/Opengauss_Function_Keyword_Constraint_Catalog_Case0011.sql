--  @testpoint:openGauss关键字constraint_catalog(非保留)，同时作为表名和列名带引号，并进行dml操作,constraint_catalog列的值最终显示为1000

drop table if exists "constraint_catalog";
create table "constraint_catalog"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"constraint_catalog" varchar(100) default 'constraint_catalog'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "constraint_catalog"(c_id,"constraint_catalog") values(1,'hello');
insert into "constraint_catalog"(c_id,"constraint_catalog") values(2,'china');
update "constraint_catalog" set "constraint_catalog"=1000 where "constraint_catalog"='hello';
delete from "constraint_catalog" where "constraint_catalog"='china';
select "constraint_catalog" from "constraint_catalog" where "constraint_catalog"!='hello' order by "constraint_catalog";

drop table "constraint_catalog";

