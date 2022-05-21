-- @testpoint: PostGIS功能覆盖,获取geogA的边界,ST_Boundary

--step1:创建表   expect:成功
drop table if exists t_postgis_0022;
create table t_postgis_0022(type varchar,smgeometry geometry);

--step2:插入数据   expect:成功
insert into t_postgis_0022 values('polygon',ST_GeomFromText('polygon((40 120, 90 120, 90 150, 40 150, 40 120))',4490));
insert into t_postgis_0022 values('polygon',ST_GeomFromText('polygon((40 120, 90 120, 90 150, 40 150, 40 120),(70 130, 80 130, 80 140, 70 140, 70 130))',4490));
insert into t_postgis_0022 values('linestring',ST_GeomFromText('linestring(60 60, 65 60, 65 70, 70 70)',4490));
insert into t_postgis_0022 values('multilinestring',ST_GeomFromText('multilinestring((60 60, 65 60, 65 70, 70 70),(80 80, 85 80, 85 90, 90 90),(50 50, 55 50, 55 60, 60 60))',4490));
insert into t_postgis_0022 values('point',ST_GeomFromText('point(30 30)',4490));

--step3:结合表查看数据   expect:成功
--计算面smgeometry的边界，以EWKT形式显示
select ST_AsEWKT(ST_Boundary(smgeometry)) as boundary from t_postgis_0022 where type='polygon';

--计算线smgeometry的边界，以EWKT形式显示
select ST_AsEWKT(ST_Boundary(smgeometry)) as boundary from t_postgis_0022 where type='linestring' or type='multilinestring';

--计算点smgeometry的边界，以EWKT形式显示
select ST_AsEWKT(ST_Boundary(smgeometry)) as boundary from t_postgis_0022 where type='point';

--step4:清理环境   expect:成功
drop table t_postgis_0022 cascade;

