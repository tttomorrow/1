-- @testpoint: kmeans创建mode，带正确的超参num_features

--step1: 创建表并插入数据;expect: 创建表并插入数据成功
drop table if exists t_model_tab_0043;
create table t_model_tab_0043(id integer not null,"position" double precision[] not null,closest_centroid integer not null, l1_distance double precision not null, l2_distance double precision not null,l2_squared_distance double precision not null,linf_distance double precision not null );
insert into t_model_tab_0043 values (214,'{82.2331969052000034,52.153098620199998,64.0343866000999933,-.325498643699999981,-64.6012143075999947,81.5499670644999952,59.6012626708999989}',3,10.0679804558999992,4.35061551650000012,18.9278551126999999,2.38435523010000019);

--step2: kmeans创建mode带正确的超参num_features;expect: 创建成功
create model m_model_kmeans_num_features_0043 using kmeans from (select position from t_model_tab_0043 ) with num_features = 7;

--step3: 查询系统表中的 hyperparametersvalues;expect: 返回的内容中含设置的num_features的值7
select hyperparametersvalues from gs_model_warehouse where modelname='m_model_kmeans_num_features_0043';

--step4: 清理环境;expext: 清理成功
drop table t_model_tab_0043;
drop model m_model_kmeans_num_features_0043;