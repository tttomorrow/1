-- @testpoint: logistic_regression创建mode带超参batch_size(int)最小值,超参batch_size(int)小于最小值,部分测试点合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0061;
create table t_model_tab_0061(id integer not null,second_attack integer,treatment integer,trait_anxiety integer );
insert into t_model_tab_0061 values (1,1,1,70),(2,1,1,80),(3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),(19,0,0,50),(20,0,0,60);

--step2: logistic_regression创建mode带超参batch_size(int)最小值;expect: 创建成功
create model m_model_min_batch_size_0061  using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0061  with batch_size=1;

--step3: 查找系统表;expect: 返回创建model的modelname值m_model_min_batch_size_0061
select modelname from gs_model_warehouse order by modelname;

--step4: logistic_regression创建mode带超参batch_size(int)小于最小值;expect: 创建失败,报错提示超参batch_size值错误
create model m_model_min_batch_size1_0061  using logistic_regression features treatment,trait_anxiety target second_attack from t_model_tab_0061  with batch_size=0;

--step5: 清理环境;expext: 清理成功
drop table t_model_tab_0061;
drop model m_model_min_batch_size_0061;