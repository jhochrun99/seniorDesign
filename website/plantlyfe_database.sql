CREATE TABLE User(
    username VARCHAR(20),
    password CHAR(64),
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE Plants(
    plantOwner VARCHAR(20),
    plantName VARCHAR(20),
    plantID INT,
    PRIMARY KEY (plantID),
    FOREIGN KEY (plantOwner) REFERENCES User(username)
);

CREATE TABLE PlantInfo(
    plantID INT,
    soil INT,
    temperature INT,
    humidity INT,
    light_needs INT,
    water_level VARCHAR(5),
    measurement_time TIMESTAMP,
    PRIMARY KEY (plantID, measurement_time),
    FOREIGN KEY (plantID) REFERENCES Plants(plantID)
);