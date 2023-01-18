WITH ASCD AS (SELECT DISTINCT C.WORKCENTER, CASE WHEN CAST(C.WORKSTART AS TIME) > '06:30' AND CAST(C.WORKSTART AS TIME)  < '14:30' THEN 1 ELSE 0 END AS VAR1 ,
 CASE WHEN CAST(C.WORKSTART AS TIME) > '14:30' AND CAST(C.WORKSTART AS TIME)  < '23:05' THEN 1 ELSE 0  END AS VAR2
 FROM IASPRDCONF C
WHERE  C.COSTCENTER IN ('CNC','TASLAMA','CNCTORNA')
AND C.WORKSTART > (CASE DATENAME(WEEKDAY, GETDATE()) WHEN 'Monday' 
THEN   CAST(CAST(DATEADD(DAY,-3,GETDATE()) AS DATE) AS DATETIME) ELSE  CAST(CAST(DATEADD(DAY,-1,GETDATE()) AS DATE) AS DATETIME)  END))
SELECT WORKCENTER, COUNT(WORKCENTER) AS VARD FROM ASCD GROUP BY WORKCENTER