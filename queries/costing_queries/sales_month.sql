SELECT MATGRP2,[a],[b],[c] -- Replace these years with the actual year values relevant to your data
FROM
(
    SELECT MATGRP2,  (CAST(MONTH AS varchar(10))  + '-' + CAST(YEAR AS VARCHAR(10)) ) AS MONTH, EURBALANCE
    FROM VLFSALESFORCOSTING
    WHERE MONTH > MONTH(DATEADD(MONTH, -4, GETDATE())) AND
		YEAR = YEAR(DATEADD(MONTH, -4, GETDATE()))
) AS SourceTable
PIVOT
(
    SUM(EURBALANCE)
    FOR MONTH IN ([a],[b],[c])  -- This should match the years in the SELECT clause
) AS PivotTable;
