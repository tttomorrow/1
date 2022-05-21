-- @testpoint: 创建model，features指定多个特征列,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0012;
create table t_model_tab_0012(id integer not null,
    "position" double precision[] not null,
    closest_centroid integer not null,
    l1_distance double precision not null,
    l2_distance double precision not null,
    l2_squared_distance double precision not null,
    linf_distance double precision not null );
insert into t_model_tab_0012 values (214,'{82.2331969052000034,52.153098620199998,64.0339866000999933,-.325498639699999981,-64.6012142075999947,81.5499670644999952,59.6012626708999989}',3,10.0679804578999992,4.35061571650000012,18.9278571126999999,2.38415523010000019);

--step2: 创建model,features指定指定多个特征列;expect: 合理报错
create model m_model_features_multi_column_0012 using kmeans features position,closest_centroid from(select position,l1_distance,closest_centroid from t_model_tab_0012)  with max_iterations  = 1,num_features = 7;

--step3: 清理环境;expect: 清理环境成功
drop table t_model_tab_0012;