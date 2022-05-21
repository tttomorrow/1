-- @testpoint: 测试指定分区索引名与否对重建分区哈希索引的影响（后跟table关键字）

--创建分区表
drop table if exists t_hash_index_0048;
create table t_hash_index_0048(id01 int, id02 char) with(orientation=row)
partition by range(id02)
(
    partition p01 values less than ('g'),
    partition p02 values less than ('n'),
    partition p03 values less than ('z')
);

--创建哈希索引
create index i_hash_index_0048 on t_hash_index_0048 using hash(id02) local
(
    partition index_p01,
    partition index_p02,
    partition index_p03
);

--重建哈希索引(指定分区名称)
reindex table t_hash_index_0048 partition p01;
--重建哈希索引(未指定分区名称)
reindex table t_hash_index_0048;

--删除哈希索引
drop index i_hash_index_0048;
 
--删除表、表空间
drop table t_hash_index_0048 cascade;
