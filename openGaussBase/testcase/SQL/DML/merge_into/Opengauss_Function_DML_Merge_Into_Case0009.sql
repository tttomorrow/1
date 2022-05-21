-- @testpoint: 目标表和源表都不存在进行merge into操作,合理报错
--step1: 进行merge into 操作 expect: 失败
merge into t_mergeinto_09_01 t1   using t_mergeinto_09_01 t2
on (t1.product_id = t2.product_id)
when matched then
  update set t1.product_name = t2.product_name, t1.category = t2.category
  where t1.product_name != 'play gym'
when not matched then
  insert values (t2.product_id, t2.product_name, t2.category)
  where t2.category = 'books';