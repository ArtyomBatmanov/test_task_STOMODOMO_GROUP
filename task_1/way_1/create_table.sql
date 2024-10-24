CREATE TABLE People (
    ID SERIAL PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    BirthDate DATE NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    MedicalCardNumber VARCHAR(50),
    INN VARCHAR(20),
    Role VARCHAR(20) CHECK (Role IN ('Пациент', 'Сотрудник', 'Оба')) NOT NULL
);
