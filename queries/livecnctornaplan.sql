SELECT B.WORKCENTER,B.MATERIAL,A.DRAWNUM,B.BLOCKQTY,B.PRODUCTBLOCKQTY,(B.BLOCKQTY - B.PRODUCTBLOCKQTY) AS REMAINPLN ,MAX(B.FINISHDAY)  AS FINISHDAY ,B.STEXT
	FROM VLFPLANSOURCE B
	LEFT OUTER JOIN IASMATBASIC A ON A.MATERIAL = B.MATERIAL
	LEFT OUTER JOIN VLFSTOCKFLOW F ON F.MATERIAL = A.MATERIAL
	LEFT OUTER JOIN VLFSTOCKFLOW F2 ON (F.NUMBER + 1) = F2.NUMBER
		AND F.ANAMAMUL = F2.ANAMAMUL
	LEFT OUTER JOIN VLFDEPOLAR D ON F2.MATERIAL = D.MATERIAL
	LEFT OUTER JOIN IASPRDOPR K ON K.MATERIAL = B.MATERIAL
	WHERE B.CLOSED = 0
		AND B.PLNQTY > 0
		AND B.ISDELAYED = 0
		AND A.COMPANY = '01'
		AND A.CLIENT = '00'
		AND B.WORKCENTER LIKE ('CNCTO%')
		AND B.BEGINDAY <= '2024-11-11 12:00:06'
		AND B.BEGINDAY >= '2024-05-15 12:00:06'
		GROUP BY  B.WORKCENTER,B.MATERIAL,A.DRAWNUM,B.BLOCKQTY,B.PRODUCTBLOCKQTY,B.STEXT
		ORDER BY B.WORKCENTER,B.MATERIAL


