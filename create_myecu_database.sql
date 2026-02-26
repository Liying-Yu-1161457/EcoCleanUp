-- create enums
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE attendance_stat AS ENUM ('registered', 'attended', 'no_show');


-- 1. users

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash CHAR(60) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  role user_role NOT NULL DEFAULT 'volunteer',
  status user_status NOT NULL DEFAULT 'active',
  full_name VARCHAR(100) NOT NULL,
  home_address TEXT,
  contact_number VARCHAR(20),
  environmental_interests TEXT,   
  profile_image VARCHAR(255),     
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. events
CREATE TABLE events (
  event_id SERIAL PRIMARY KEY,
  event_name VARCHAR(100) NOT NULL,
  location VARCHAR(255) NOT NULL,  
  event_type VARCHAR(50) NOT NULL,
  event_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  duration INTEGER,
  supplies TEXT,
  description TEXT,
  safety_info TEXT,
  status VARCHAR(20) DEFAULT 'upcoming',
  event_leader_id INTEGER REFERENCES users(user_id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. registrations 
CREATE TABLE registrations (
  registration_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  event_id INTEGER REFERENCES events(event_id),
  registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  attendance_stat attendance_stat DEFAULT 'registered',
  UNIQUE(user_id, event_id)
);

-- 4. feedback 
CREATE TABLE feedback (
  feedback_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(user_id),
  event_id INTEGER REFERENCES events(event_id),
  rating INTEGER DEFAULT 0,
  comments TEXT,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. outcomes 
CREATE TABLE outcomes (
  outcome_id SERIAL PRIMARY KEY,
  event_id INTEGER REFERENCES events(event_id) UNIQUE,
  num_attendees INTEGER DEFAULT 0,
  bags_collected INTEGER DEFAULT 0,
  recyclables_sorted INTEGER DEFAULT 0,
  other_achievements TEXT,
  recorded_by INTEGER REFERENCES users(user_id),
  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create indexs
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_registrations_user ON registrations(user_id);
CREATE INDEX idx_registrations_event ON registrations(event_id);
CREATE INDEX idx_feedback_event ON feedback(event_id);


