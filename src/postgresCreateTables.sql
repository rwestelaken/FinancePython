
DROP TABLE company;
DROP TABLE measure;
DROP TABLE equity_price;

CREATE TABLE company( 
	ticker TEXT NOT NULL, 
	name TEXT NOT NULL,   
	industry TEXT NOT NULL);

CREATE TABLE measure( 
	ticker TEXT NOT NULL, 
	start_date DATE NULL, 
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	measure TEXT NOT NULL,
	amount REAL NOT NULL);

CREATE TABLE equity_price( 
	source TEXT NOT NULL, 
	ticker TEXT NOT NULL,
	end_date DATE NOT NULL, 
	end_time TIMESTAMPTZ NOT NULL, 
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	volume REAL NOT NULL,
	dividend REAL NOT NULL,
	split REAL NOT NULL,
	adj_open REAL NOT NULL,
	adj_high REAL NOT NULL,
	adj_low REAL NOT NULL,
	adj_close REAL NOT NULL,
	adj_volume REAL NOT NULL);

SELECT * from company;
SELECT * from measure;
SELECT * from equity_price
