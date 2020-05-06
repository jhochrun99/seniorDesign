CREATE TABLE Plants(
    plantName VARCHAR(20),
    plantID INT,
    sunlight INT,
    soilMoisture INT,
    lowestTemp INT,
    highestTemp INT,
    active BOOLEAN,
    PRIMARY KEY (plantID)
);

CREATE TABLE PlantMeasurements(
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