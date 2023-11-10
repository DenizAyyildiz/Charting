SELECT '' AS ANALYZER,  FORMAT(IASPRDCONF.WORKSTART ,'yyyy-MM') AS DATE,
CAST(SUM(IASPRDCONF.OUTPUT +IASPRDCONF.SCRAP+IASPRDCONF.REWORK) AS INT) AS QUANTITY,
CAST(SUM((IASPRDCONF.OUTPUT +IASPRDCONF.SCRAP+IASPRDCONF.REWORK)*B.BRUTWEIGHT)/1000 AS INT) AS TOTALWEIGHT,
0.00 AS CONSUMPTION,0.000 AS kwhkg
FROM IASPRDCONF
LEFT JOIN IASPRDOPR A ON  A.CONFIRMATION = IASPRDCONF.CONFIRMATION
LEFT JOIN IASMATBASIC B ON A.MATERIAL = B.MATERIAL AND B.COMPANY  = '01'
WHERE IASPRDCONF.WORKCENTER IN (XXMATERIALYY)
AND IASPRDCONF.WORKSTART BETWEEN  'xxxx-yy-zz' AND 'aaaa-bb-cc'
GROUP BY FORMAT(IASPRDCONF.WORKSTART,'yyyy-MM')
