-- @testpoint: linear_regression创建mode,带超参verbose

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0116;
create table t_model_tab_0116(id int,tax int,bedroom int,bath float,price int,size int,lot int,mark text);
insert into t_model_tab_0116 values (1,590,2,1,50000,70,22100,'a+'),(2,1050,3,2,85000,1410,12000,'a+'),(3,20,3,1,22500,1060,3500,'a-'),(4,870,2,2,90000,1300,17500,'a+'),(5,1320,3,2,133000,150,30000,'a+'),(6,1350,2,1,90500,820,25700,'a-'), (7,2790,3,2.5 ,260000,2130,25000,'a'),(8,680,2 ,1,142500,170,22000,'a-'),(9,1840,3,2 ,60000,1500,19000,'a+'),(10,3680,4,2,240000,2790,20000,'a-'),(11,1660,3,1,87000,1030,17500,'a+');

--step2: linear_regression创建mode带超参verbose值为true;expect: 创建成功
create model m_model_verbose_0116 using linear_regression features 1,tax,bath,size target price from t_model_tab_0116  with verbose = true;

--step3: 查找系统表的hyperparametersvalues值;expect: 返回内容含verbose的值
select hyperparametersvalues from gs_model_warehouse where modelname = 'm_model_verbose_0116';

--step4: linear_regression创建mode带超参verbose值为false;expect: 创建成功
create model m_model_verbose1_0116 using linear_regression features 1,tax,bath,size target price from t_model_tab_0116  with verbose = false;

--step5: 查找系统表的hyperparametersvalues值;expect: 返回内容含verbose的值
select hyperparametersvalues from gs_model_warehouse where modelname = 'm_model_verbose1_0116';

--step6: 查找系统表;expect: 返回创建model的modelname值m_model_verbose_0116,m_model_verbose1_0116
select modelname from gs_model_warehouse order by modelname;

--step7: 清理环境;expext: 清理成功
drop table t_model_tab_0116;
drop model m_model_verbose_0116;
drop model m_model_verbose1_0116;