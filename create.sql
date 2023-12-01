CREATE TABLE Occurrence (
    id SERIAL PRIMARY KEY,
    gbifID BIGINT ,
    accessRights TEXT,
    license TEXT,
    rightsHolder TEXT,
    institutionCode TEXT,
    collectionCode TEXT,
    basisOfRecord TEXT,
    occurrenceID TEXT,
    catalogNumber TEXT,
    occurrenceStatus TEXT,
    datasetKey UUID,
    publishingCountry TEXT,
    lastInterpreted TEXT,
    issue TEXT,
    hasCoordinate BOOLEAN,
    hasGeospatialIssues BOOLEAN,
    protocol TEXT,
    lastParsed TIMESTAMP,
    lastCrawled TIMESTAMP,
    recordedBy TEXT,
    preparations TEXT,
    higherGeography TEXT,
    countryCode TEXT,
    stateProvince TEXT,
    locality TEXT,
    repatriated BOOLEAN,
    county TEXT,
    eventDate DATE,
    year DOUBLE PRECISION,
    month DOUBLE PRECISION,
    decimalLatitude DOUBLE PRECISION,
    decimalLongitude DOUBLE PRECISION,
    day DOUBLE PRECISION,
    eventRemarks TEXT,
    typeStatus TEXT,
    infraspecificEpithet TEXT
);



CREATE TABLE Kingdom (
    kingdom_id SERIAL PRIMARY KEY,
    kingdom TEXT
);

CREATE TABLE Phylum (
    phylum_id SERIAL PRIMARY KEY,
    phylum TEXT
);

CREATE TABLE Classe (
    classe_id SERIAL PRIMARY KEY,
    classe TEXT
);

CREATE TABLE Ordem (
    ordem_id SERIAL PRIMARY KEY,
    ordem TEXT
);

CREATE TABLE Familia (
    familia_id SERIAL PRIMARY KEY,
    familia TEXT
);

CREATE TABLE Genus (
    genus_id SERIAL PRIMARY KEY,
    genus TEXT
);

CREATE TABLE Taxonomy (
    id SERIAL PRIMARY KEY,
    taxonKey INTEGER,
    kingdom_id INTEGER REFERENCES Kingdom(kingdom_id),
    scientificName TEXT,
    iucnRedListCategory TEXT,
    specificEpithet TEXT,
    species TEXT
);

CREATE TABLE OccurrenceTaxonomy (
    id INTEGER REFERENCES Occurrence(id),
    taxonid INTEGER REFERENCES Taxonomy(id),
    PRIMARY KEY (id, taxonid)
);

-- Create Log table
CREATE TABLE OccurrenceLog (
    log_id SERIAL PRIMARY KEY,
    event_type TEXT, -- Insert, Update, Delete
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER, -- You may need to adjust this based on your user management system
    table_name TEXT,
    record_id INTEGER,
    new_data JSONB, -- Store new data for updates or inserted data
    old_data JSONB -- Store old data for updates or deleted data
);

-- Trigger function for logging
CREATE OR REPLACE FUNCTION log_occurrence_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO OccurrenceLog (event_type, user_id, table_name, record_id, new_data)
        VALUES ('Insert', CURRENT_USER, TG_TABLE_NAME, NEW.id, TO_JSONB(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO OccurrenceLog (event_type, user_id, table_name, record_id, new_data, old_data)
        VALUES ('Update', CURRENT_USER, TG_TABLE_NAME, NEW.id, TO_JSONB(NEW), TO_JSONB(OLD));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO OccurrenceLog (event_type, user_id, table_name, record_id, old_data)
        VALUES ('Delete', CURRENT_USER, TG_TABLE_NAME, OLD.id, TO_JSONB(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the log_occurrence_changes function
CREATE TRIGGER log_occurrence_changes_trigger
AFTER INSERT OR UPDATE OR DELETE ON Occurrence
FOR EACH ROW
EXECUTE FUNCTION log_occurrence_changes();

