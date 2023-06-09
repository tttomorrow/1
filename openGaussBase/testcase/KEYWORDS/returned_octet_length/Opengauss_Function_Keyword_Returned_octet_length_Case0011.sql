--  @testpoint:openGauss关键字returned_octet_length(非保留)，同时作为表名和列名带引号，并进行dml操作,returned_octet_length列的值最终显示为1000

drop table if exists "returned_octet_length";
create table "returned_octet_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"returned_octet_length" varchar(100) default 'returned_octet_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "returned_octet_length"(c_id,"returned_octet_length") values(1,'hello');
insert into "returned_octet_length"(c_id,"returned_octet_length") values(2,'china');
update "returned_octet_length" set "returned_octet_length"=1000 where "returned_octet_length"='hello';
delete from "returned_octet_length" where "returned_octet_length"='china';
select "returned_octet_length" from "returned_octet_length" where "returned_octet_length"!='hello' order by "returned_octet_length";

drop table "returned_octet_length";

