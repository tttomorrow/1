-- @testpoint: 建表指定compression参数

--step1:创建一种复合类型;expect:成功
drop type if exists type_case0003 cascade;
create type type_case0003 as (a int, b text);

--step2:行存表指定compression参数，压缩为pglz格式;expect:成功
drop table if exists tb_grammar0003_01;
create table tb_grammar0003_01 (a double) compression = pglz;

--step3:插入数据;expect:成功
insert into tb_grammar0003_01 values(112.568);

--step4:建表添加if not exists，表不存在，会有notice提示， compression = zstd;expect:成功
create table  if not exists tb_grammar0003_02 (a double) with (orientation=row) compression = zstd ;

--step5:行存表指定compression参数，压缩为pglz格式，使用自定义数据类型，并添加engine参数;expect:成功
drop table if exists tb_grammar0003_03;
create table tb_grammar0003_03 of type_case0003 compression = pglz engine= 自定义;

--step6:复制已有的表数据再次建表;expect:成功
drop table if exists tb_grammar0003_04;
create table tb_grammar0003_04 compression = zstd engine= 复制 as select a from tb_grammar0003_01;

--step7:查询数据;expect:成功
select a from tb_grammar0003_04;

--step8:建表指定compression = zstd，添加if not exists，无notice提示;expect:成功
create table if not exists tb_grammar0003_05 (a text(10)) compression = zstd engine= 第5个表;

--step9:建表指定compression = zstd，使用自定义类型;expect:成功
drop table if exists tb_grammar0003_06;
create table tb_grammar0003_06 of type_case0003 compression = pglz  engine= 第6个表;

--step10:建表压缩参数值为none;expect:成功
drop table if exists tb_grammar0003_07;
create table tb_grammar0003_07(a double) compression = 'none';

