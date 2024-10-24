SELECT r1.ID_Patients, r1.ID_Doctors
FROM Receptions r1
WHERE r1.StartDateTime = (
    SELECT MAX(r2.StartDateTime)
    FROM Receptions r2
    WHERE r2.ID_Patients = r1.ID_Patients);
