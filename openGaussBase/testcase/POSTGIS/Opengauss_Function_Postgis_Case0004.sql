-- @testpoint: 验证integer,char,varchar,text,timestamp without time zone数据类型(合理)的应用

--step1:创建表    expect:成功
drop table if exists t_postgis_0003 cascade;
create table t_postgis_0003 (
    correction_id integer not null,
    user_id character(32) not null,
    element_id uuid not null,
    obj_code character varying(5000) not null,
    description character varying(5000),
    geometry text not null,
    geometry_type character(1),
    review_status character(1) not null,
    update_time timestamp(6) without time zone not null,
    review_user_id character(32),
    obj_status character(1));

--step2:插入合理数据  expect:成功
insert into t_postgis_0003 values(1,'7101','c71ceaca-a175-11e9-a920-797ff7000001','101','说明','空间纠错信息','1','1','2010-10-13','71011','2');
insert into t_postgis_0003 values(1,to_char(lpad('a',32,'x')),'c71ceaca-a175-11e9-a920-797ff7000001','101','说明','空间纠错信息','1','1','2010-10-13','71011','2');

--step3:查看数据   expect:成功
select * from t_postgis_0003;

--step4:清理环境   expect:成功
drop table t_postgis_0003;
