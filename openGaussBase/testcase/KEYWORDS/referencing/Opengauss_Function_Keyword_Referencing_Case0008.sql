--  @testpoint:openGauss关键字referencing(非保留)，作为列名带引号并且删除时使用该列,建表成功，referencing列值是'hello'的删除成功

drop table if exists referencing_test;
create table referencing_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"referencing" varchar(100) default 'referencing'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into referencing_test(c_id,"referencing") values(1,'hello');
insert into referencing_test(c_id) values(2);
delete from referencing_test where "referencing"='hello';
select * from referencing_test order by "referencing";
drop table referencing_test;


