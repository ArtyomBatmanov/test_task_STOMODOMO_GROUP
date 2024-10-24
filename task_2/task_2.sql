WITH LatestReceptions AS (
    SELECT
        ID_Patients,
        ID_Doctors,
        ROW_NUMBER() OVER (PARTITION BY ID_Patients ORDER BY StartDateTime DESC) AS rn
    FROM Receptions
)
SELECT ID_Patients, ID_Doctors
FROM LatestReceptions
WHERE rn = 1;
