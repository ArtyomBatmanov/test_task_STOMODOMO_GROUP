CREATE TABLE Roles (
    PeopleID INT,
    Role VARCHAR(20) CHECK (Role IN ('Пациент', 'Сотрудник', 'Оба')) NOT NULL,
    PRIMARY KEY (PeopleID, Role),
    FOREIGN KEY (PeopleID) REFERENCES People(ID) ON delete CASCADE
);
