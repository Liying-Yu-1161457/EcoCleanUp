
-- 1. INSERT ADMINISTRATORS (2)

INSERT INTO users (username, password_hash, email, role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('admin01Tanya', '$2b$12$u0TrrF0UEP9o.78eRmG0SunjuCn79ZVjlMQNbl/YhvuRrqM.mpIlS', 'Tanya@ecocleanup.nz', 'admin', 'active', 'Tanya Herring', '15 Victoria Street West, Auckland CBD, Auckland 1010', '09 366 2000', 'community engagement, strategic planning', NULL),
('admin02Audra', '$2b$12$mM6/EIm/U4A.JkMbN60H5eSCvHTkxCGdcJuomnKf4nAYjRwhhUApG', 'Audra@ecocleanup.nz', 'admin', 'active', 'Audra Villarreal', '2 Lampton Quay, Wellington Central, Wellington 6011', '04 499 4444', 'policy development, environmental law', NULL);


-- 2. INSERT EVENT LEADERS (5)

INSERT INTO users (username, password_hash, email, role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('philip', '$2b$12$/uF0K1P7g9ASHT5PPCRdKuafpxZZR/4nX24OhVn6T67KYMA5FHcma', 'philip.mueller@ecocleanup.nz', 'event_leader', 'active', 'Philip Mueller', '45 College Road, Northcote, Christchurch 8052', '03 365 7889', 'beach cleanups, marine conservation', NULL),
('rose', '$2b$12$8MV2haLZL6pwR7vzHEnxA.v72.Y.690wJcu5BIf3QL1dKLB/57v.q', 'rose.hanson@ecocleanup.nz', 'event_leader', 'active', 'Rose Hanson', '78 Devon Street East, New Plymouth 4310', '027 555 4321', 'park cleanups, tree planting', NULL),
('skyler', '$2b$12$vFjcRDhz00wfsVCUQ/26RObFPhCpXjWt8zpwb6Oc.Fv3DSNgHveLy', 'skyler.mcneil@ecocleanup.nz', 'event_leader', 'active', 'Skyler Mcneil', '123 Grey Street, Hamilton East, Hamilton 3216', '022 123 4567', 'river cleanups, freshwater ecology', NULL),
('fiona', '$2b$12$F9/vUR.ub2mKPJ5JVAZSB.QJNgUCYIvqbEdxWRXsDq90UWhkgmLKm', 'fiona.adams@ecocleanup.nz', 'event_leader', 'active', 'Fiona Adams', '56 King Edward Parade, Devonport, Auckland 0624', '021 987 6543', 'coastal restoration, dune planting', NULL),
('joel', '$2b$12$QwXZpsqw/SMQvssx3TPoleVIi9w7ZXvNlAzadlhvOvLhdIJPmZQi2', 'joel.nielsen@ecocleanup.nz', 'event_leader', 'active', 'Joel Nielsen', '234 High Street, Dunedin Central, Dunedin 9016', '03 477 1122', 'bush regeneration, weed control', NULL);


-- 3. INSERT VOLUNTEERS (20)

INSERT INTO users (username, password_hash, email, role, status, full_name, home_address, contact_number, environmental_interests, profile_image) VALUES
('rudyard', '$2b$12$TXhnp83uBYKqSfvJaXVnm.eTTDWPUPHDfSnY2doTviF9p.KLxeZNO', 'rudyard.burnett@gmail.com', 'volunteer', 'active', 'Rudyard Burnett', '23 Moorehouse Avenue, Addington, Christchurch 8011', '021 345 678', 'beach cleanups, recycling', NULL),
('chelsea', '$2b$12$7CSiDvYIwvfvHd/b8eZJsuO/xrnHyqtKQRUMFr/d5Z7cB3/OrVRQS', 'chelsea.benjamin@gmail.com', 'volunteer', 'active', 'Chelsea Benjamin', '56 Rata Street, Naenae, Lower Hutt 5011', '04 567 8901', 'tree planting, native bush', NULL),
('kerry', '$2b$12$vqmuZNLkT30/cMRBCp3pKe9Tz7ThTxdg05nKkJySBikxepEefDtRi', 'kerry.lowe@gmail.com', 'volunteer', 'active', 'Kerry Lowe', '12 Marine Parade, Mount Maunganui 3116', '027 456 789', 'dune restoration, beach cleanups', NULL),
('cherokee', '$2b$12$9wnz0ueHUFaWk2bTktU6LuAkAWcqnLqI0rydO/i2SAJF.zRrr5rdO', 'cherokee.vargas@gmail.com', 'volunteer', 'active', 'Cherokee Vargas', '89 Karaka Street, Otaki 5512', '06 364 7788', 'river cleanups, freshwater health', NULL),
('nathaniel', '$2b$12$eo9bolxyqhWMknn3FEgXyuIJxv5.V3QTokehUGg42yZWGGR88.aHy', 'nathaniel.myers@gmail.com', 'volunteer', 'active', 'Nathaniel Myers', '34 Shortland Street, Auckland CBD, Auckland 1010', '022 111 2233', 'urban gardening, composting', NULL),
('maya', '$2b$12$UINr7.q1RKVyuLNZ6UsDmuEEIDPIONxeP3hiZdeKYI3KzwOP2GMka', 'maya.chandler@gmail.com', 'volunteer', 'active', 'Maya Chandler', '67 Maunganui Road, Mount Maunganui 3116', '07 575 1234', 'marine conservation, beach cleanups', NULL),
('scarlet', '$2b$12$yH7/5PhBUOPizz0Lcq4E9uTlAYdCZLlmG6t0XCbZAjjthpD2Abt3S', 'scarlet.ware@gmail.com', 'volunteer', 'active', 'Scarlet Ware', '45 Fendalton Road, Fendalton, Christchurch 8041', '03 355 6677', 'park cleanups, bird watching', NULL),
('juliet', '$2b$12$G1m.tZ7u1aA1uuZgGEsnYeuJKuF6UHhSSdID2E5eAuh3lVMk41.BK', 'juliet.acosta@gmail.com', 'volunteer', 'active', 'Juliet Acosta', '123 Khyber Pass Road, Grafton, Auckland 1023', '021 987 123', 'weed control, native planting', NULL),
('haley', '$2b$12$P6mOsT6VRrAiyiB.qaUqQuF8/3ix43.X3473x9q.SHaEhNbEFzE8q', 'haley.mcguire@gmail.com', 'volunteer', 'active', 'Haley Mcguire', '78 Cuba Street, Te Aro, Wellington 6011', '04 382 1234', 'recycling education, zero waste', NULL),
('daniel', '$2b$12$XSBG7lumEfnufhP298OdherhnuHNXwZ/BtHF22PCh3uazvbXPp8wu', 'daniel.mooney@gmail.com', 'volunteer', 'active', 'Daniel Mooney', '23 Taupo Quay, Whanganui 4500', '06 345 6789', 'river care, eel conservation', NULL),
('baker', '$2b$12$lJxx7pNTeT7RlKib0AcnN.mIEU2CsMxQOS1QiuCHbir/DEgCYjd1.', 'baker.beck@gmail.com', 'volunteer', 'active', 'Baker Beck', '56 Victoria Avenue, Remuera, Auckland 1050', '09 520 1234', 'community gardens, native bees', NULL),
('urielle', '$2b$12$0rwMHlHl2Q5En9X9DrpLzejX.KFqFc5NvPsLyW1snPuAiByLk0ICO', 'urielle.lester@gmail.com', 'volunteer', 'active', 'Urielle Lester', '12 Pohutukawa Avenue, Tauranga 3110', '027 888 456', 'dune planting, sea turtle protection', NULL),
('nola', '$2b$12$Z.w3w.Ys44BTQbn1ArVagOY/Z4DfRwwocnwDig8kU45z1d.5ZK2WK', 'nola.perkins@gmail.com', 'volunteer', 'active', 'Nola Perkins', '89 Hereford Street, Christchurch Central 8011', '03 377 8899', 'urban sustainability, food forests', NULL),
('emerson', '$2b$12$3o7hC7Wqj8CEtOZ8R03UeOkc8NkvB6auLpfwC30MTsvISRCAWNFe6', 'emerson.allison@gmail.com', 'volunteer', 'active', 'Emerson Allison', '34 Maungawhau Road, Mount Eden, Auckland 1024', '022 444 5678', 'wetland restoration, bird monitoring', NULL),
('kiona', '$2b$12$GOvOo6ZiAkV827BBGMBdmuMQ81DsShhmlkVfsF6hSvYb/5v6oNGZW', 'kiona.sherman@gmail.com', 'volunteer', 'active', 'Kiona Sherman', '67 Clyde Road, Ilam, Christchurch 8041', '021 222 3344', 'alpine cleanups, track maintenance', NULL),
('tana', '$2b$12$2ze23L4dympjkqx7Js5iieQaujycEOe1hbnl7mVNGp9lhvJ9VhdaS', 'tana.pratt@gmail.com', 'volunteer', 'active', 'Tana Pratt', '45 The Terrace, Wellington Central 6011', '04 499 7788', 'plastic free initiatives, zero waste', NULL),
('ava', '$2b$12$A.UZCdYv1rTFCmZzSUrekeQhTIJXJ5ZvaQvPyxkepNO0ElbGMm43i', 'ava.delaney@gmail.com', 'volunteer', 'active', 'Ava Delaney', '123 High Street, Lower Hutt 5010', '04 567 2233', 'park cleanups, community events', NULL),
('bell', '$2b$12$jia3sN5txCiLw1RF8mqPSe12fNLetc4w3ljTMwYbokS3avdd9YQQO', 'bell.lamb@gmail.com', 'volunteer', 'active', 'Bell Lamb', '78 Featherston Street, Palmerston North 4410', '06 358 9900', 'stream care, native planting', NULL),
('rogan', '$2b$12$wDgQY.q92CHKtpYG5mH0SuLK54NAvy/dyiaPwlT2IqMqjhLgd1FG6', 'rogan.whitley@gmail.com', 'volunteer', 'active', 'Rogan Whitley', '34 Princess Street, Dunedin 9016', '03 479 1122', 'biodiversity monitoring, pest control', NULL),
('silas', '$2b$12$tpM.FQSGU9SQLGYAQ3EQv.uRLMO9u1hWHGhktdLtM1gbSDuNYon.e', 'silas.bailey@gmail.com', 'volunteer', 'active', 'Silas Bailey', '56 Queen Street, Auckland CBD 1010', '09 377 5566', 'urban forestry, tree planting', NULL);


-- 4. INSERT EVENTS (20)
INSERT INTO events (event_id, event_name, location, event_type, event_date, start_time, end_time, duration, supplies, description, safety_info, status, event_leader_id, created_at) VALUES
(1, 'Sumner Beach Cleanup', 'Sumner Beach, Christchurch', 'beach', '2025-12-15', '09:00', '12:00', 3, 'Gloves, bags, hi-vis vests', 'Monthly beach cleanup focusing on plastic waste', 'Bring sunscreen and water. Meet at surf club.', 'completed', 1, '2025-11-01 10:00:00'),
(2, 'Wellington Waterfront Restoration', 'Frank Kitts Park, Wellington', 'park', '2025-12-18', '10:00', '14:00', 4, 'Gloves, weeding tools, native plants', 'Planting native species along waterfront', 'Wear sturdy shoes. Training provided.', 'completed', 2, '2025-11-05 14:30:00'),
(3, 'Hamilton River Care', 'Riverbank, Hamilton Gardens', 'river', '2025-12-10', '09:30', '12:30', 3, 'Gloves, bags, litter pickers', 'Cleaning Waikato River banks', 'Stay away from water edge. Adult supervision.', 'completed', 3, '2025-11-10 09:15:00'),
(4, 'Devonport Coastal Clean', 'Devonport Beach, Auckland', 'beach', '2025-12-22', '08:00', '11:00', 3, 'Gloves, bags, sunhats', 'Early morning beach cleanup', 'Sun protection advised. Family friendly.', 'completed', 4, '2025-11-15 16:45:00');

INSERT INTO events (event_id, event_name, location, event_type, event_date, start_time, end_time, duration, supplies, description, safety_info, status, event_leader_id, created_at) VALUES
(5, 'Dunedin Bush Regeneration', 'Town Belt, Dunedin', 'bush', '2026-03-25', '09:00', '13:00', 4, 'Gloves, loppers, weed bags', 'Removing invasive weeds from native bush', 'Long pants recommended. Steep terrain.', 'upcoming', 5, '2026-02-01 11:20:00'),
(6, 'New Plymouth Park Cleanup', 'Pukekura Park, New Plymouth', 'park', '2026-03-27', '10:00', '13:00', 3, 'Gloves, bags, pickers', 'General park maintenance and litter collection', 'Meet at main entrance. All welcome.', 'upcoming', 2, '2026-02-05 13:40:00'),
(7, 'Tauranga Harbour Clean', 'The Strand, Tauranga', 'harbour', '2026-03-29', '09:00', '12:00', 3, 'Gloves, bags, waders (limited)', 'Harbour edge cleanup focusing on plastics', 'Waterproof footwear advised.', 'upcoming', 1, '2026-02-08 09:30:00'),
(8, 'Queenstown Trail Maintenance', 'Queenstown Gardens, Queenstown', 'trail', '2026-04-02', '09:00', '15:00', 6, 'Gloves, tools, lunch provided', 'Maintaining walking tracks and planting', 'Full day event. Lunch provided. Fitness required.', 'upcoming', 3, '2026-02-10 15:15:00');

INSERT INTO events (event_id, event_name, location, event_type, event_date, start_time, end_time, duration, supplies, description, safety_info, status, event_leader_id) VALUES
(9,'Gisborne Beach Clean', 'Midway Beach, Gisborne', 'beach', '2026-04-05', '08:30', '11:30', 3, 'Gloves, bags, sunscreen', 'Morning beach cleanup', 'First sunrise city event. Bring camera.', 'upcoming', 4),
(10,'Nelson Nature Reserve', 'Grampians Reserve, Nelson', 'bush', '2026-04-08', '10:00', '14:00', 4, 'Gloves, weeding tools, water', 'Weed control in native reserve', 'Moderate fitness required. Hills.', 'upcoming', 5),
(11,'Rotorua Lakefront Clean', 'Lake Rotorua, Rotorua', 'lake', '2026-04-10', '09:00', '12:00', 3, 'Gloves, bags, grabbers', 'Cleaning lakefront and geothermal areas', 'Be aware of hot spots. Stay on paths.', 'upcoming', 1),
(12,'Palmerston North River Clean', 'Manawatu River, Palmerston North', 'river', '2026-04-12', '10:00', '13:00', 3, 'Gloves, bags, waders optional', 'Riverbank restoration and cleanup', 'Bring change of clothes. Might get muddy.', 'upcoming', 2),
(13,'Auckland Domain Planting', 'Auckland Domain, Auckland', 'park', '2026-04-15', '09:00', '12:00', 3, 'Gloves, plants, tools', 'Winter planting in historic park', 'Rain or shine. Undercover area available.', 'upcoming', 3),
(14,'Whanganui River Care', 'Whanganui Riverbank, Whanganui', 'river', '2026-04-18', '09:30', '13:30', 4, 'Gloves, bags, secateurs', 'River edge restoration and litter pickup', 'Long sleeves recommended. Native planting.', 'upcoming', 4),
(15,'Timaru Beach Cleanup', 'Caroline Bay, Timaru', 'beach', '2026-04-20', '09:00', '12:00', 3, 'Gloves, bags, sunhats', 'Popular beach spring clean', 'Family friendly. Playground nearby.', 'upcoming', 5),
(16,'Hawkes Bay Shore Clean', 'Napier Marine Parade, Napier', 'coastal', '2026-04-22', '08:00', '11:00', 3, 'Gloves, bags, morning tea', 'Art Deco coastline cleanup', 'Combine with walk. Interesting architecture.', 'upcoming', 1),
(17,'Taupo Lakeside', 'Taupo Lakefront, Taupo', 'lake', '2026-04-25', '09:00', '12:00', 3, 'Gloves, bags, pickers', 'Great Lake cleanup', 'Spectacular views. Photo opportunity.', 'upcoming', 2),
(18,'Invercargill Estuary', 'Estuary Walkway, Invercargill', 'wetland', '2026-04-28', '10:00', '14:00', 4, 'Gloves, boots, bags', 'Estuary and wetland restoration', 'Windy location. Dress warmly.', 'upcoming', 3),
(19,'Blenheim Riverside', 'Taylor River, Blenheim', 'river', '2026-05-01', '09:00', '12:00', 3, 'Gloves, bags, tools', 'Riverside walkway maintenance', 'Meet at the fountain. Coffee nearby.', 'upcoming', 4),
(20,'Wanaka Alpine Cleanup', 'Lake Wanaka Foreshore, Wanaka', 'alpine', '2026-05-05', '09:00', '13:00', 4, 'Gloves, bags, warm layers', 'Beautiful alpine environment cleanup', 'Weather dependent. Check forecast.', 'upcoming', 5);


-- 5. INSERT REGISTRATIONS (25)

INSERT INTO registrations (user_id, event_id, registration_time, attendance_stat) VALUES
(3, 1, '2025-11-20 10:30:00', 'attended'),
(4, 1, '2025-11-21 14:15:00', 'attended'),
(5, 2, '2025-11-22 09:00:00', 'attended'),
(6, 2, '2025-11-22 11:30:00', 'no_show'),  
(7, 3, '2025-11-23 08:45:00', 'attended'),
(8, 3, '2025-11-23 16:20:00', 'attended'),
(9, 4, '2025-11-24 12:10:00', 'attended'),
(10, 4, '2025-11-24 13:30:00', 'attended');

INSERT INTO registrations (user_id, event_id, registration_time, attendance_stat) VALUES
(3, 5, '2026-02-15 09:15:00', 'registered'),
(5, 5, '2026-02-15 11:45:00', 'registered'),
(7, 6, '2026-02-16 10:30:00', 'registered'),
(9, 6, '2026-02-16 13:20:00', 'registered'),
(11, 7, '2026-02-17 09:00:00', 'registered'),
(13, 7, '2026-02-17 16:30:00', 'registered'),
(15, 8, '2026-02-18 08:45:00', 'registered');


-- 6. INSERT FEEDBACK (for past events)

INSERT INTO feedback (user_id, event_id, rating, comments, submitted_at) VALUES
(3, 1, 5, 'Awesome event! Collected 15 bags of rubbish. Will definitely come again.', '2025-12-16 15:30:00'),
(4, 1, 4, 'Well organized. Great to see the community come together.', '2025-12-16 14:20:00'),
(5, 2, 5, 'The planting was fun. The seedlings are looking good!', '2025-12-19 16:45:00'),
(6, 2, 4, 'Good turnout. Would be better with more tools.', '2025-12-19 15:10:00'),
(7, 3, 5, 'Lovely day by the river. Made new friends.', '2025-12-11 13:30:00'),  
(8, 3, 3, 'Good cause but needs better signage to find meeting point.', '2025-12-11 12:15:00'),
(9, 4, 5, 'Perfect weather, perfect company. Devonport looking clean!', '2025-12-23 11:45:00'),
(10, 4, 4, 'Enjoyed it. Coffee after was a nice touch.', '2025-12-23 12:30:00');


-- 7. INSERT OUTCOMES (for completed events)

INSERT INTO outcomes (event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by, recorded_at) VALUES
(1, 12, 15, 8, 'Found interesting marine specimens. Reported to DOC.', 1, '2025-12-16 13:00:00'),
(2, 18, 5, 2, 'Planted 50 native trees. Weed control completed.', 2, '2025-12-19 15:00:00'),
(3, 14, 22, 10, 'Removed shopping trolleys from river. Council notified.', 3, '2025-12-11 14:30:00'),
(4, 20, 18, 12, 'Microplastic survey conducted. Data sent to university.', 4, '2025-12-23 13:15:00');


-- Summary

SELECT 'Database population complete!' as "Status";
SELECT COUNT(*) || ' users' as "Users" FROM users;
SELECT COUNT(*) || ' events' as "Events" FROM events;
SELECT COUNT(*) || ' registrations' as "Registrations" FROM registrations;
SELECT COUNT(*) || ' feedback' as "Feedback" FROM feedback;
SELECT COUNT(*) || ' outcomes' as "Outcomes" FROM outcomes;