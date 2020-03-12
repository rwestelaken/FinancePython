
DROP TABLE Company;
DROP TABLE Measures;

CREATE TABLE Company( 
	Ticker TEXT NOT NULL, 
	Name TEXT NOT NULL,   
	Industry TEXT NOT NULL);

INSERT INTO Company(Ticker, Name, Industry) 
	VALUES ('AAA','AAA','Finance');

CREATE TABLE Measures( 
	Ticker TEXT NOT NULL, 
	StartDate DATE NULL, 
	EndDate DATE NOT NULL, 
	EndTime TIMESTAMPTZ NOT NULL, 
	Measuare TEXT NOT NULL,
	Amount REAL NOT NULL);

INSERT INTO Measures(Ticker, StartDate, EndDate, EndTime, Measuare, Amount) 
	VALUES ('AAA', NULL, '2020-10-01', '2020-01-01 22:10:25-04', 'Price', 123.456);
INSERT INTO Measures(Ticker, StartDate, EndDate, EndTime, Measuare, Amount)  
	VALUES ('AAA', '2020-01-01', '2020-01-31', '2020-01-31 11:59:59-04', 'Income', 123.456 );

SELECT * from Company;
SELECT * from Measures;
