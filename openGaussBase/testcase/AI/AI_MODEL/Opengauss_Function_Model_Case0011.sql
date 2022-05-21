-- @testpoint: 创建model，features指定子查询中不被选中的列名,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0011;
create table t_model_tab_0011(id int,tax int,bedroom int,bath float,price int,size int,lot int, test text);
insert into t_model_tab_0011 values (1,590,2,1,50000,770 ,22100,'hello'),(2,1050,3,2,8500,1410,12000,'hello2'),(3,20,3,1,22500,1060,3500,'test');

--step2: 创建model，features指定子查询中不被选中的列名;expect: 合理报错
create model m_model_features_0011 using linear_regression features tax,bath,size target price from (select tax,bath,price from t_model_tab_0011 );

--step3: 清理环境;expect: 清理环境成功
drop table t_model_tab_0011;