h_joints = readtable("horizontal_joints.csv");
v_joints = readtable("vertical_joints.csv");

tick_vector = h_joints.Var1(2 : 201);

%processing 6 horizontal joints
h_zerothjoint = h_joints.Var2(2 : 201);
h_firstjoint = h_joints.Var3(2 : 201);
h_secondjoint= h_joints.Var4(2 : 201);
h_thirdjoint = h_joints.Var5(2 : 201);
h_fourthjoint = h_joints.Var6(2 : 201);
h_fifthjoint = h_joints.Var7(2 : 201);
ts_h0 = timeseries(h_zerothjoint, tick_vector);
ts_h1 = timeseries(h_firstjoint, tick_vector);
ts_h2 = timeseries(h_secondjoint, tick_vector);
ts_h3 = timeseries(h_thirdjoint, tick_vector);
ts_h4 = timeseries(h_fourthjoint, tick_vector);
ts_h5 = timeseries(h_fifthjoint, tick_vector);


%processing 5 vertical joints
v_zerothjoint = v_joints.Var2(2 : 201);
v_firstjoint = v_joints.Var3(2 : 201);
v_secondjoint= v_joints.Var4(2 : 201);
v_thirdjoint = v_joints.Var5(2 : 201);
v_fourthjoint = v_joints.Var6(2 : 201);

ts_v0 = timeseries(v_zerothjoint, tick_vector);
ts_v1 = timeseries(v_firstjoint, tick_vector);
ts_v2 = timeseries(v_secondjoint, tick_vector);
ts_v3 = timeseries(v_thirdjoint, tick_vector);
ts_v4 = timeseries(v_fourthjoint, tick_vector);