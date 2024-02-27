
WITH MaterialSelection AS (SELECT
    'XYZ' AS MACHINE,
    'XXYY' AS MACHINE_NAME,
    MATERIAL,
    CONFIRMATION,
    CONVERT(VARCHAR(5),MIN(CURDATETIME),108) AS STARTTIME ,
	CONVERT(VARCHAR(5),MAX(CURDATETIME),108) AS ENDTIME,
    CONVERT(VARCHAR(5), MAX(CASE WHEN CURDATETIME < 'XXXX-XX-XX 07:00:00.000' THEN CURDATETIME END), 108) AS MaxTime,
	CONVERT(VARCHAR(5), MIN(CASE WHEN CURDATETIME > 'XXXX-XX-XX 07:00:00.000' THEN CURDATETIME END), 108) AS MinTime,
    DATEDIFF(MINUTE,MAX(CASE WHEN CURDATETIME < 'XXXX-XX-XX 07:00:00.000' THEN CURDATETIME END),  MIN(CASE WHEN CURDATETIME >  'XXXX-XX-XX 07:00:00.000' THEN CURDATETIME END)) AS MinDifference
FROM
    [dbo].[XYZ]
WHERE
    CURDATETIME >= 'XXXX-XX-XX'
    AND CURDATETIME < 'YYYY-YY-YY'
GROUP BY
    MATERIAL, CONFIRMATION
HAVING
    MIN(CURDATETIME) < 'XXXX-XX-XX 07:00:00.000'
    AND MAX(CURDATETIME) > 'XXXX-XX-XX 07:00:00.000'
)
SELECT * FROM MaterialSelection
WHERE MinDifference < 30
