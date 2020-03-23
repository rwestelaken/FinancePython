
DROP TABLE company;
DROP TABLE measure;
DROP TABLE equity_price;

CREATE TABLE company( 
	ticker TEXT NOT NULL, 
	name TEXT NOT NULL,   
	industry TEXT NOT NULL)

CREATE TABLE measure( 
	source TEXT NOT NULL,
	ticker TEXT NOT NULL, 
	start_date DATE NULL, 
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	measure TEXT NOT NULL,
	amount REAL NOT NULL);

CREATE TABLE price( 
	source TEXT NOT NULL, 
	ticker TEXT NOT NULL,
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	volume REAL NOT NULL,
	adj_close REAL NOT NULL);

CREATE TABLE dividend(
	source TEXT NOT NULL, 
	ticker TEXT NOT NULL,
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	amount REAL NOT NULL,

CREATE TABLE split(
	source TEXT NOT NULL, 
	ticker TEXT NOT NULL,
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	amount REAL NOT NULL)

SELECT * from company;
SELECT * from measure;
SELECT * from equity_price
