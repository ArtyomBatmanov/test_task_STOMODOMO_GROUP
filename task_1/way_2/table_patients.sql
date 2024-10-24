create TABLE Patients (
    PeopleID INT PRIMARY KEY,
    MedicalCardNumber VARCHAR(50) NOT NULL,
    FOREIGN KEY (PeopleID) REFERENCES People(ID) ON delete CASCADE
);
