CREATE TABLE Employees (
    PeopleID INT PRIMARY KEY,
    inn VARCHAR(20) NOT NULL,
    FOREIGN KEY (PeopleID) REFERENCES People(ID) ON delete CASCADE
);
