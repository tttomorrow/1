-- @testpoint: pg_stat_get_db_blocks_hit(oid)返回数据库在缓冲区中找到的磁盘块抓取请求的总数。
alter system set autovacuum to off;
-- 先清理环境
drop table if exists sales;
select pg_stat_reset();
--创建表sales
CREATE TABLE sales
(prod_id numeric(6),
 cust_id numeric,
 time_id DATE,
 channel_id CHAR(1),
 promo_id numeric(6),
 quantity_sold numeric(3),
 amount_sold numeric(10,2)
);
-- testpoint1:建表后会计数
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
-- testpoint2:创建索引 0 0
select pg_stat_reset();
create index test_index1 on sales (channel_id);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- testpoint3:插入第一行数据
select pg_stat_reset();
-- 数据插入sales
INSERT INTO sales VALUES(1, 12, '2019-02-01 00:00:00', 'b', 1, 1, 1);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- testpoint4:更新一行数据
select pg_stat_reset();
update sales set time_id = '2019-06-02 10:00:00' where channel_id = 'b';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- 再添加数据
select pg_stat_reset();
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'c', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-03 00:00:00', 'd', 1, 1, 1);
INSERT INTO sales VALUES(1, 12, '2019-02-05 00:00:00', 'e', 1, 1, 3);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- 更新多行
select pg_stat_reset();
update sales set time_id = '2015-06-02 10:00:00' where channel_id = 'c';
update sales set time_id = '2013-06-02 10:00:00' where channel_id = 'd';
update sales set time_id = '2012-06-02 10:00:00' where amount_sold = 3;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- testpoint5:查看删除数据的统计
-- 删除一行
select pg_stat_reset();
delete from sales where channel_id = 'b';
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- 删除多行
select pg_stat_reset();
delete from sales where channel_id = 'c';
delete from sales where channel_id = 'd';
delete from sales where channel_id = 'e';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- testpoint6:查表
select pg_stat_reset();
select * from sales;
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_db_blocks_hit(a.oid) > 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_blocks_hit(a.oid) = 0 from PG_DATABASE a where a.datname = CURRENT_CATALOG;

-- 恢复环境
drop table sales cascade;
alter system set autovacuum to on;