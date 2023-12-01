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
