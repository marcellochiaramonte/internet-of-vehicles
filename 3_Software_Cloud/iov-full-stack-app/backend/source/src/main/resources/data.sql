	INSERT INTO vehicle (model, make, id, icon_color) VALUES
	  ('i-MiEV', 'Mitsubishi','1234','red'),
	  ('iOn', 'Peugeot','1235','blue'),
	  ('Ampera', 'Opel','1236','white'),
      ('Stromos', 'German E-Cars','54567','green');                                  ;

    INSERT INTO metric (id, name, unit_type, data_type) values
    ('101','car_on','boolean','boolean'),
    ('102','brake_pedal_position','boolean','boolean'),
    ('103','accelerator_pedal_position','boolean','boolean'),
    ('104','brake_pedal_switch','boolean','boolean'),
    ('105','charger_temperature','boolean','boolean'),
    ('106','charger_detection','boolean','boolean'),
    ('107','motor_temperature','boolean','boolean'),
    ('108','motor_rpm','boolean','boolean'),
    ('109','handbrake','boolean','boolean'),
    ('110','battery_soc','percent','float'),
    ('111','speed','km/h','integer'),
    ('112','odometer','km','long'),
    ('113','transmission','volts','float'),
    ('114','quick_charge','volts','float'),
    ('115','charge_current_limit','volts','float');


  INSERT INTO vehicle_event (uuid,timestamp,value,metric_id,vehicle_id) values
    ('79ade66b-3cf0-46bb-bb7b-183bac203fb0','1614265926','82','110','1234'),
    ('9a1e0d0e-e408-4b67-8c4d-377bb09e3fe1','1614266106','79','110','1234'),
    ('ebdd6127-3fa1-46b3-a20d-062a654b6820','1614266286','78','110','1234'),
   ('9870ed76-f5f9-4fd3-9912-027b245f6991','1614266526','77','110','1234'),
   ('fc0d5be2-67b1-4179-8dc4-10a6cbec1d30','1614266706','74','110','1234'),
   ('dd1a11c3-a1a2-468a-8e3f-a8db7f8f4836','1614266946','73','110','1234'),
   ('118fb9d7-116d-493f-9c99-01163c3c0592','1614267186','72','110','1234'),
   ('a06a9840-de52-4d90-86dd-be63bc369637','1614267300','70','110','1234'),
   ('b2eb924c-3720-4919-b42b-4fee78749e4e','1614267546','68','110','1234'),
   ('d4477c31-8921-4ee3-8edb-1de56e620f17','1614267786','67','110','1234'),
   ('e4925cb8-ecf2-4ac7-a7e0-88ace8fbf31d','1614267966','65','110','1234');

 --   INSERT INTO vehicle_event (timestamp,value,metric_id,vehicle_id) values
 --   ('1612587791','35','11','1234'),
  --  ('1612224991','40','11','1234'),
  --  ('1612322791','70','11','1234'),
  --  ('1612421791','100','11','1234'),
  --  ('1612520791','80','11','1234'),
  --  ('1612691764','75','11','1234');

