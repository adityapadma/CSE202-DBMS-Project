-- NON CONFLICTING TRANSACTIONS
-- 1 
START TRANSACTION;
INSERT INTO Ride_request (request_id, passenger_username, pickup_loc, drop_loc, fare, taxitype, status)
VALUES (51, 'p51', 'A', 'C', 400, 'Sedan', 'Pending');
UPDATE Ride_request SET status = 'Rejected' WHERE request_id = 51;
COMMIT;

-- 2
START TRANSACTION;
UPDATE Driver SET f_name = 'Johnny', l_name = 'Doe' WHERE driver_id ='D12';
UPDATE Driver SET rating = CASE
    WHEN rating < 5 THEN rating + 1
    ELSE rating
END
WHERE driver_id = 'D12';
COMMIT;

-- 3 
start transaction;
-- Delete a ride
delete from payment where ride_id='R40';
DELETE FROM Ride WHERE ride_id = 'R40';
-- Update the ride request status
UPDATE Ride_request SET status = 'Rejected' WHERE request_id = 40;
COMMIT;

-- 4
start transaction;
-- new driver logs in
insert into login(username, passwor, user_type)
values('d41', 123, 'driver');
-- new taxi is assigned to the driver
insert into taxi (taxi_id, number_plate, taxi_type) 
values ('T41', 'HR20', 'XL');
-- driver gives information
insert into driver (driver_id, username, f_name, l_name, ph_num, rating, taxi_id)
values ('D41', 'd41', 'Hira', 'Lal', 2397496326, 4, 'T41');
-- new driver is given a ride
INSERT INTO Ride (ride_id, request_ID, driver_ID, pickup_time, drop_time)
VALUES ('R41', 41, 'D41', '7mins', '22mins');
-- status of the ride is changed as the ride is givena to a new driver
UPDATE Ride_request SET status = 'Accepted' WHERE request_id = 51;
commit;

-- 5 
start transaction;
update ride_request set fare= fare-100 where request_id=51;
update ride_request set fare= fare+100 where request_id=52;
commit;

-- CONFLICTING TRANSACTIONS
-- 1
start transaction;
UPDATE ride_request SET status = 'Rejected' WHERE request_id= 32;
UPDATE driver SET rating = rating - 1 WHERE driver_id = 'D32';
COMMIT;
start transaction;
UPDATE driver SET rating = rating + 1 WHERE driver_id = 'D32';
UPDATE ride_request SET status = 'Accepted' WHERE request_id = 32 ;
COMMIT;

-- 2
start transaction;
UPDATE passenger SET f_name = 'Alice' WHERE username = 'p11';
UPDATE ride_request SET drop_loc = 'C' WHERE request_id = 11;
COMMIT;
start transaction;
UPDATE ride_request SET drop_loc = 'B' WHERE request_id = 11;
UPDATE passenger SET f_name = 'Bob' WHERE username = 'p11';
COMMIT;

-- -----------------------------------------------------------------------------------------------------------------------------------------

-- Transaction 1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO Ride_request (request_id, passenger_username, pickup_loc, drop_loc, fare, taxitype, status)
VALUES (51, 'p51', 'A', 'C', 400, 'Sedan', 'Pending');
UPDATE Ride_request SET status = 'Accepted' WHERE request_id = 51;
COMMIT;

-- Transaction 2
start transaction;
update ride_request set fare= fare-100 where request_id=51;
update ride_request set fare= fare+100 where request_id=52;
commit;


-- Conflict Serializable
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
INSERT INTO Ride_request (request_id, passenger_username, pickup_loc, drop_loc, fare, taxitype, status)
VALUES (51, 'p51', 'A', 'C', 400, 'Sedan', 'Pending');
UPDATE Ride_request SET status = 'Accepted' WHERE request_id = 51;
COMMIT;
start transaction;
update ride_request set fare= fare-100 where request_id=51;
update ride_request set fare= fare+100 where request_id=52;
commit;

-- Non Conflict Serializable
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
INSERT INTO Ride_request (request_id, passenger_username, pickup_loc, drop_loc, fare, taxitype, status)
VALUES (51, 'p51', 'A', 'C', 400, 'Sedan', 'Pending');
UPDATE Ride_request SET status = 'Accepted' WHERE request_id = 51;
COMMIT;
start transaction;
update ride_request set fare= fare-100 where request_id=51;
update ride_request set fare= fare+100 where request_id=52;
commit;

