-- @testpoint: 创建model，指定训练模型特征为*,合理报错

--step1: 建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_model_tab_0016;
create table t_model_tab_0016(id integer,fixed_acidity double precision,volatile_acidity double precision,citric_acid double precision,residual_sugar
double precision,chlorides double precision,free_sulfur_dioxide double precision,total_sulfur_dioxide double precision,density double precision,ph double precision,
sulphates double precision,alcohol double precision,quality double precision,class text);
insert into t_model_tab_0016 values (0,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,5,'red'),(1, 7.8,0.88,0.0,2.6,0.098,25.0,67.0,0.9968,3.2,0.68,9.8,5,'red'),(2,7.8,0.76,0.04,2.3,0.092,15.0,54.0,0.997,3.26,0.65,9.8,5, 'red'),(3, 11.2,0.28,0.56,1.9,0.075,17.0,60.0,0.998,3.16,0.58,9.8,6, 'red'),(4,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,5, 'red'),(5, 7.4,0.66,0.0,1.8,0.075,13.0,40.0,0.9978,3.51,0.56,9.4,5, 'red'),(6, 7.9,0.6,0.06,1.6,0.069,15.0,59.0,0.9964,3.3,0.46,9.4,5, 'red'),(7, 7.3,0.65,0.0,1.2,0.065,15.0,21.0,0.9946,3.39,0.47,10.0,7, 'red'),(8,7.8,0.58,0.02,2.0,0.073,9.0,18.0,0.9968,3.36,0.57,9.5,7, 'red'),(9, 7.5,0.5,0.36,6.1,0.071,17.0,102.0,0.9978,3.35,0.8,10.5,5, 'red'),(10,6.7,0.58,0.08,1.8,0.09699999999999999,15.0,65.0,0.9959,3.28,0.54,9.2,5, 'red');

--step2: 创建model,指定训练模型特征为*;expect: 合理报错
create model m_model_characteristic_0016 using linear_regression features * target price from t_model_tab_0016);

--step3: 清理环境;expect: 清理环境成功
drop table t_model_tab_0016;