# def key_facts(FYEAR,DATE_TO,TABLE):

#     keystr = f'''

#     DECLARE @NINE INTEGER
#     DECLARE @FYEAR  VARCHAR (4)
#     DECLARE @END  VARCHAR (10)
#     DECLARE @table VARCHAR (15)
#     DECLARE @sql NVARCHAR(MAX)

#     SET @NINE = '8388607'
# 	--CAST(0x7fffffff AS INT) -- numeric value to be suppressed
#     SET @FYEAR = '{FYEAR}'	                 -- represents a financial year, the year selected is the first year of the period e.g. 2012-13 is @FYEAR 2012
# 	SET @END = '{DATE_TO}'				 -- year and month of the last month for this dateset
# 	SET @table = '{TABLE}'	         -- processing run with X suffix

#     SET NOCOUNT ON

#     EXEC('
#     SELECT * INTO ##proms_processing_KF1a
#     FROM (
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,''Provider'' AS [Organisation Type], 
#         Q._Q1_PROCODE AS [Organisation Code], ''Index'' AS Measure,	CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) BETWEEN 1 AND 5 THEN '+@NINE+'
#         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) END AS Improved,
                    
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) 
#                 END AS Unchanged,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5
#                         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 
#                 END AS Worsened,
                
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(Q.Q2_EQ5D_INDEX) 
#                 END AS TOTAL
#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._INDEX_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._Q1_PROCODE

#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,''CCG of GP Practice'' AS [Organisation Type], 
#         P.ccg_code AS [Organisation Code],''Index'' AS Measure,
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 
#                 END AS Improved,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END)
#                 END AS Unchanged,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 
#                 END AS Worsened,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_INDEX) 
#                 END AS TOTAL
#         FROM proms.QUESTS_'+@table+' Q

#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P
#         ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._INDEX_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code

#     UNION
    
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,''England'' AS [Organisation Type], 
#         ''England'' AS [Organisation Code],''Index'' AS Measure,
        
#         COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) AS Improved,
#             COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) AS Unchanged,
#             COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) AS Worsened,
#             COUNT(Q.Q2_EQ5D_INDEX) AS TOTAL
        
#     FROM proms.QUESTS_'+@table+' Q
#     WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' 
#     AND Q._INDEX_CHANGE_FLAG = 1 AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

#     GROUP BY Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE

#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,''Provider'' AS [Organisation Type],   
#         Q._Q1_PROCODE AS [Organisation Code],''VAS'' AS Measure,
        
#         CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#             AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 
#             THEN '+@NINE+'
#             ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 
#             END AS Improved,

#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                 AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 
#                 THEN '+@NINE+'
#                 ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 
#             END AS Unchanged,

#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 
#             END AS Worsened,

#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 
#             END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._SCALE_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY Q._Q1_FYEAR, Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._Q1_PROCODE

#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE, ''CCG of GP Practice'' AS [Organisation Type], 
#         P.ccg_code AS [Organisation Code],''VAS'' AS Measure,
        
#         CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#             AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 
#             THEN '+@NINE+'
#             ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 
#         END AS Improved,
                
#         CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#             AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 
#             THEN '+@NINE+'
#             ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 
#         END AS Unchanged,   

#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 
#                 END AS Worsened,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 
#                 END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P
#         ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._SCALE_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code

#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  ''England'' AS [Organisation Type], 
#         ''England'' AS [Organisation Code],''VAS'' AS Measure,
        
#             COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) AS Improved,
#                 COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) AS Unchanged,
#                 COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) AS Worsened,
#                 COUNT(Q.Q2_EQ5D_HEALTH_SCALE) AS TOTAL
            
#         FROM proms.QUESTS_'+@table+' Q
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._SCALE_CHANGE_FLAG = 1 AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE

#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  ''Provider'' AS [Organisation Type], 	 
#                 Q._Q1_PROCODE AS [Organisation Code], Q._CS_CODE AS Measure,
#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 
#                 END AS Improved,
                        
#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 
#                 END AS Unchanged,

#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) 
#                 END AS Worsened,

#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_CS_SCORE) 
#                 END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE, Q._Q1_PROCODE,Q._CS_CODE
        
#     UNION
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE, ''CCG of GP Practice'' AS [Organisation Type],	
#         P.ccg_code AS [Organisation Code], Q._CS_CODE AS Measure,

#             CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                 AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 
#                     END AS Improved,

#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         AND COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 
#                     END AS Unchanged,
                    
#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR   Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV''THEN ''D'' END) 
#                     END AS Worsened,

#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(Q.Q2_CS_SCORE) 
#                     END AS TOTAL
                    
#         FROM proms.QUESTS_'+@table+' Q
#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code,Q._CS_CODE

#     UNION
    
#         SELECT Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,''England'' AS [Organisation Type], 
#         ''England'' AS [Organisation Code],Q._CS_CODE AS Measure,

#                     COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) AS Improved,
#                     COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) AS Unchanged,
#                     COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) AS Worsened,
#                     COUNT(Q.Q2_CS_SCORE) AS TOTAL
                
#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1
#         GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._CS_CODE
#     )_

#     SELECT * INTO ##proms_processing_KF1b
#     FROM ( SELECT Q.PROMS_PROC_CODE,''Provider'' AS [Organisation Type], Q._Q1_PROCODE AS [Organisation Code],
#     ''Index'' AS Measure,	
#             CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 
#                 END AS Improved,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) 
#                 END AS Unchanged,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5
#                         AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 
#                 END AS Worsened,
                    
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(Q.Q2_EQ5D_INDEX) 
#                 END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._INDEX_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,Q._Q1_PROCODE

#     UNION
    
#         SELECT Q.PROMS_PROC_CODE,''CCG of GP Practice'' AS [Organisation Type], P.ccg_code AS [Organisation Code],
#         ''Index'' AS Measure,
#         CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 
#                 END AS Improved,
                    
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END)
#                 END AS Unchanged,
                    
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 
#                 END AS Worsened,
                    
#                 CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_INDEX) 
#                 END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._INDEX_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code
    
#     UNION
    
#         SELECT Q.PROMS_PROC_CODE,''England'' AS [Organisation Type], ''England'' AS [Organisation Code],
#         ''Index'' AS Measure,
#             COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) AS Improved,
#             COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) AS Unchanged,
#             COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) AS Worsened,
#             COUNT(Q.Q2_EQ5D_INDEX) AS TOTAL
            
#     FROM proms.QUESTS_'+@table+' Q
#     WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._INDEX_CHANGE_FLAG = 1
#     AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#     GROUP BY Q.PROMS_PROC_CODE
    
#     UNION
#         SELECT Q.PROMS_PROC_CODE, ''Provider'' AS [Organisation Type], Q._Q1_PROCODE AS [Organisation Code],
#             ''VAS'' AS Measure,
#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 
#             END AS Improved,
                
#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                 AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 
#                 THEN '+@NINE+'
#                 ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 
#             END AS Unchanged,
                
#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 
#             END AS Worsened,

#             CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 
#             END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'
#         AND Q._SCALE_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY Q._Q1_FYEAR, Q.PROMS_PROC_CODE,Q._Q1_PROCODE

#     UNION
    
#         SELECT Q.PROMS_PROC_CODE, ''CCG of GP Practice'' AS [Organisation Type], P.ccg_code AS [Organisation Code],
#                 ''VAS'' AS Measure,
#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 
#                 END AS Improved,
                
#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 
#                 END AS Unchanged,
                
#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 
#                 END AS Worsened,

#                 CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 
#                 END AS TOTAL

#         FROM proms.QUESTS_'+@table+' Q
#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' 
#         AND Q._SCALE_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code

#     UNION
    
#         SELECT Q.PROMS_PROC_CODE, ''England'' AS [Organisation Type], ''England'' AS [Organisation Code],
#         ''VAS'' AS Measure,

#                 COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) AS Improved,
#                 COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) AS Unchanged,
#                 COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) AS Worsened,
#                 COUNT(Q.Q2_EQ5D_HEALTH_SCALE) AS TOTAL
            
#         FROM proms.QUESTS_'+@table+' Q WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' 
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCALE_CHANGE_FLAG = 1 
#         AND Q.PROMS_PROC_CODE in (''hr'',''kr'')
#         GROUP BY Q.PROMS_PROC_CODE
            
#     UNION
#         SELECT Q.PROMS_PROC_CODE, ''Provider'' AS [Organisation Type], Q._Q1_PROCODE AS [Organisation Code],
#         Q._CS_CODE AS Measure,

#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 
#                 END AS Improved,

#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 
#                 END AS Unchanged,
                
#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) 
#                 END AS Worsened,
                        
#                 CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                     THEN '+@NINE+'
#                     ELSE COUNT(Q.Q2_CS_SCORE) 
#                 END AS TOTAL
                        
#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1 AND Q._Q1_PROCODE IS NOT NULL
#         GROUP BY  Q.PROMS_PROC_CODE, Q._Q1_PROCODE,Q._CS_CODE
        
#     UNION
    
#         SELECT Q.PROMS_PROC_CODE, ''CCG of GP Practice'' AS [Organisation Type],P.ccg_code AS [Organisation Code],
#         Q._CS_CODE AS Measure,
#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 
#                     END AS Improved,
#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         AND COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 
#                     END AS Unchanged,

#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 
#                         THEN '+@NINE+
#                         ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                         OR   Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV''THEN ''D'' END) 
#                     END AS Worsened,
                            
#                     CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 
#                         THEN '+@NINE+'
#                         ELSE COUNT(Q.Q2_CS_SCORE) 
#                     END AS TOTAL
                    
#         FROM proms.QUESTS_'+@table+' Q
#         LEFT JOIN proms.HES_PROCEDURES_'+@table+' P ON Q._P_REF_PROM = P._P_REF_PROM
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1 AND P.ccg_code IS NOT NULL
#         GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code,Q._CS_CODE
        
#     UNION
    
#         SELECT Q.PROMS_PROC_CODE, ''England'' AS [Organisation Type], ''England'' AS [Organisation Code],
#         Q._CS_CODE AS Measure,

#                     COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) AS Improved,
#                     COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) AS Unchanged,
#                     COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 
#                     OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) AS Worsened,
#                     COUNT(Q.Q2_CS_SCORE) AS TOTAL
                
#         FROM proms.QUESTS_'+@table+' Q
#         WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'') AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\' 
#         AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\' AND Q._SCORE_CHANGE_FLAG = 1
#         GROUP BY  Q.PROMS_PROC_CODE,Q._CS_CODE
#     ) KF1

#     SELECT * INTO ##proms_processing_KF2
#     FROM ( SELECT RP.[Description] AS [Procedure], K.[Organisation Type],[Organisation Code],
    
#     CASE WHEN K.[Organisation Type]= ''England'' THEN ''England''
#                 WHEN K.[Organisation Type]= ''CCG of GP Practice'' AND K.[Organisation Code]= ''---'' THEN ''Unknown''
#                 ELSE ISNULL(O.OrgName,''Unknown'')
#             END AS [Organsation Name],
#             RM.[Description] AS [Measure], K.[Improved],K.[Unchanged],K.[Worsened],K.[Total],

#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Improved] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS IFLAG,
#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Unchanged] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS UFLAG,
#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Worsened] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS WFLAG
        
#     FROM ##proms_processing_KF1b K
#     LEFT JOIN proms.REF_ORGS_'+@table+' O ON o.OrgCode = K.[Organisation Code]
#     LEFT JOIN proms.REF_PROCEDURES RP ON K.PROMS_PROC_CODE = RP.PROMs_PROC_CODE
#     LEFT JOIN proms.REF_MEASURES RM ON K.[Measure] = RM.Measure

#     union

#     SELECT RP.[Description] AS [Procedure], K.[Organisation Type],[Organisation Code],
    
#     CASE WHEN K.[Organisation Type]= ''England'' THEN ''England''
#                 WHEN K.[Organisation Type]= ''CCG of GP Practice'' AND K.[Organisation Code]= ''---'' THEN ''Unknown''
#                 ELSE ISNULL(O.OrgName,''Unknown'')
#             END AS [Organsation Name],
#             RM.[Description] AS [Measure],K.[Improved],K.[Unchanged],K.[Worsened],K.[Total],

#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Improved] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS IFLAG,
#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Unchanged] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS UFLAG,
#             CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Worsened] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS WFLAG
        
#     FROM ##proms_processing_KF1a K
#     LEFT JOIN proms.REF_ORGS_'+@table+' O ON o.OrgCode = K.[Organisation Code]
#     LEFT JOIN proms.REF_PROCEDURES RP ON K._PRIM_REV_PROC_CODE = RP.PROMs_PROC_CODE
#     LEFT JOIN proms.REF_MEASURES RM ON K.[Measure] = RM.Measure

#     where k._PRIM_REV_PROC_CODE not in (''hr'',''kr'')
#     )KF2

#     DROP TABLE ##proms_processing_KF1a
#     DROP TABLE ##proms_processing_KF1b
#     --Contains all the Improved Flags that need secondary suppression

#     SELECT * INTO #KFX FROM ( SELECT
#         CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY IFLAG) = 1 
#             THEN IFLAG END AS IFLAG
#     FROM ##proms_processing_KF2)KFX

#     --Contains all the Unchanged Flags that need secondary suppression

#     SELECT * INTO #KFY
#     FROM ( SELECT
#         CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY UFLAG) = 1 
#             THEN UFLAG END AS UFLAG
#     FROM ##proms_processing_KF2)KFY

#     --Contains all the Worsened Flags that need secondary suppression

#     SELECT * INTO #KFZ
#     FROM ( SELECT
#         CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY WFLAG) = 1 
#             THEN WFLAG END AS WFLAG
#     FROM ##proms_processing_KF2)KFZ

#     SELECT * INTO #KF3
#     FROM ( SELECT 
#                 CASE WHEN KF2.[Organisation Type] = ''England''
#                     THEN KF2.[Organisation Type]+KF2.[Organsation Name]+KF2.[Procedure]+KF2.[Measure]
#                     ELSE KF2.[Organisation Type]+KF2.[Organsation Name]+'' (''+KF2.[Organisation Code]+'')''+KF2.[Procedure]+KF2.[Measure]
#                 END AS [Lookup],
#                 KF2.[Procedure],KF2.[Organisation Type],KF2.[Organisation Code],KF2.[Organsation Name],KF2.[Measure],
#                 KF2.[Improved],KF2.[Unchanged],KF2.[Worsened],KF2.[Total],KFX.IFLAG,KFY.UFLAG,KFZ.WFLAG
#         FROM ##proms_processing_KF2 KF2
#         LEFT JOIN #KFX KFX ON KF2.IFLAG = KFX.IFLAG
#         LEFT JOIN #KFY KFY ON KF2.UFLAG = KFY.UFLAG
#         LEFT JOIN #KFZ KFZ ON KF2.WFLAG = KFZ.WFLAG
#     )KF3

#     DROP TABLE ##proms_processing_KF2
#     DROP TABLE #KFX
#     DROP TABLE #KFY
#     DROP TABLE #KFZ

#     --Applies secondary suppression for Provider Improved, if needed
#     --Identifies Procedures and Measures to be supressed

#     SELECT * INTO #IFLAG FROM (
#         SELECT IFLAG
#         FROM #KF3 
#         WHERE IFLAG IS NOT NULL
#     )KF3A

#     --Applies suppression to seleced dataset and joins to main data set
#     SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],
#             CASE WHEN IFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Improved] END AS [Improved],
#             [Unchanged],[Worsened],

#             CASE WHEN IFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],
#             IFLAG,UFLAG,WFLAG
#     INTO #KF4
#     FROM (SELECT KF3B.[Lookup],KF3B.[Procedure],KF3B.[Organisation Type],KF3B.[Organisation Code],
#     KF3B.[Organsation Name],KF3B.[Measure],KF3B.[Improved],KF3B.[Unchanged],KF3B.[Worsened],KF3B.[Total],
#     KF3A.IFLAG,KF3B.UFLAG,KF3B.WFLAG,
    
#     ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure] ORDER BY [Total]ASC)AS CLASS
#         FROM #KF3 KF3B
#         LEFT JOIN #IFLAG KF3A ON KF3A.IFLAG = KF3B.[Procedure]+KF3B.Measure
#         WHERE KF3B.WFLAG IS NULL AND KF3B.[Organisation Type]= ''Provider'' AND KF3B.Improved > 0
#         AND KF3B.Improved < '+@NINE+'
#     )_

#     UNION

#     SELECT [Lookup],[Procedure], [Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#     [Unchanged],[Worsened],[Total],IFLAG,UFLAG,WFLAG 
#     FROM #KF3
#     WHERE [Lookup] NOT IN
#     ( SELECT KF3B.[Lookup]
#     FROM #KF3 KF3B
#             LEFT JOIN #IFLAG KF3A ON KF3A.IFLAG = KF3B.[Procedure]+KF3B.Measure
#             WHERE KF3B.WFLAG IS NULL AND KF3B.[Organisation Type]= ''Provider'' AND KF3B.Improved > 0
#             AND KF3B.Improved < '+@NINE+'
#     )

#     DROP TABLE #KF3
#     DROP TABLE #IFLAG

#     --SELECT * FROM #KF4
#     --DROP TABLE #KF4

#     --Applies secondary suppression for Provider Unchanged, if needed
#     --Identifies Procedures and Measures to be supressed

#     SELECT * INTO #UFLAG
#     FROM ( SELECT UFLAG
#     FROM #KF4 
#         WHERE UFLAG IS NOT NULL
#     )KF4A

#     --SELECT * FROM #UFLAG
#     --Applies suppression to seleced dataset and joins to main data set
#     SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#             CASE WHEN UFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Unchanged] END AS [Unchanged],
#             [Worsened],
#             CASE WHEN UFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],
#             IFLAG,UFLAG,WFLAG
#     INTO #KF5
#     FROM(SELECT KF4B.[Lookup],KF4B.[Procedure],KF4B.[Organisation Type],KF4B.[Organisation Code],
#     KF4B.[Organsation Name],KF4B.[Measure],KF4B.[Improved],KF4B.[Unchanged],KF4B.[Worsened],KF4B.[Total],
#     KF4B.IFLAG,KF4A.UFLAG,KF4B.WFLAG,

#         ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure]
#                                 ORDER BY [Total]ASC)AS CLASS
#         FROM #KF4 KF4B
#         LEFT JOIN #UFLAG KF4A ON KF4A.UFLAG = KF4B.[Procedure]+KF4B.Measure
#         WHERE KF4B.WFLAG IS NULL AND KF4B.[Organisation Type]= ''Provider'' AND KF4B.Unchanged > 0
#         AND KF4B.Improved < '+@NINE+'
#     )_

#     UNION

#     SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#     [Unchanged],[Worsened],[Total],IFLAG,UFLAG,WFLAG 
#     FROM #KF4
#     WHERE [Lookup] NOT In (
#         SELECT KF4B.[Lookup]
#             FROM #KF4 KF4B
#             LEFT JOIN #UFLAG KF4A ON KF4A.UFLAG = KF4B.[Procedure]+KF4B.Measure
#             WHERE KF4B.WFLAG IS NULL AND KF4B.[Organisation Type]= ''Provider'' AND KF4B.Unchanged > 0
#             AND KF4B.Unchanged < '+@NINE+'
#     )

#     DROP TABLE #KF4
#     DROP TABLE #UFLAG

#     --Applies secondary suppression for Provider Worsened, if needed
#     --Identifies Procedures and Measures to be supressed

#     SELECT * INTO #WFLAG
#     FROM ( SELECT WFLAG
#     FROM #KF5 
#     WHERE WFLAG IS NOT NULL
#     )KF5A

#     --Applies suppression to seleced dataset and joins to main data set

#     SELECT [Lookup], [Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#     [Unchanged],
#             CASE WHEN WFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Worsened] END AS [Worsened],
#             CASE WHEN WFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],
#             IFLAG,UFLAG,WFLAG
#     INTO #KF6
#     FROM (SELECT KF5B.[Lookup],KF5B.[Procedure],KF5B.[Organisation Type],KF5B.[Organisation Code],
#     KF5B.[Organsation Name],KF5B.[Measure],KF5B.[Improved],KF5B.[Unchanged],KF5B.[Worsened],KF5B.[Total],
#     KF5B.IFLAG,KF5B.UFLAG,KF5A.WFLAG,

#             ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure]
#                                 ORDER BY [Total]ASC)AS CLASS
#         FROM #KF5 KF5B
#         LEFT JOIN #WFLAG KF5A ON KF5A.WFLAG = KF5B.[Procedure]+KF5B.Measure
#         WHERE KF5B.WFLAG IS NULL AND KF5B.[Organisation Type]= ''Provider'' AND KF5B.Worsened > 0
#         AND KF5B.Worsened < '+@NINE+'
#     )_

#     UNION

#     SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#     [Unchanged],[Worsened],[Total],IFLAG,UFLAG,WFLAG 
#     FROM #KF5
#     WHERE [Lookup] NOT IN
#     ( SELECT KF5B.[Lookup]
#         FROM #KF5 KF5B
#         LEFT JOIN #WFLAG KF5A ON KF5A.WFLAG = KF5B.[Procedure]+KF5B.Measure
#         WHERE KF5B.WFLAG IS NULL AND KF5B.[Organisation Type]= ''Provider'' AND KF5B.Worsened > 0
#         AND KF5B.Worsened < '+@NINE+'
#     )

#     DROP TABLE #KF5
#     DROP TABLE #WFLAG

#     SELECT * INTO #KF6a
#     FROM ( SELECT ''ENGLANDENGLAND''+[Procedure]+[Measure] AS ''Lookup'',
#             CASE WHEN SUM(ENGIFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGIFLAG,
#             CASE WHEN SUM(ENGUFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGUFLAG,
#             CASE WHEN SUM(ENGWFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGWFLAG,
#             CASE WHEN (SUM(ENGIFLAG) = 1 OR SUM(ENGUFLAG) = 1 OR SUM(ENGWFLAG) = 1) THEN '+@NINE+' ELSE 0 END AS ENGTFLAG
#     FROM (SELECT  [Procedure],[Measure],
#             CASE WHEN [Improved] = '+@NINE+' THEN 1 ELSE 0 END AS ENGIFLAG,
#             CASE WHEN [Unchanged] = '+@NINE+' THEN 1 ELSE 0 END AS ENGUFLAG,
#             CASE WHEN [Worsened] = '+@NINE+' THEN 1 ELSE 0 END AS ENGWFLAG
#     FROM #KF6
#     WHERE [Organisation Type] = ''Provider''
#     )_
#     GROUP BY [Procedure],[Measure] 
#     )_
#     SELECT * INTO #KF6b
#     FROM (SELECT KF6.[Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],
#             CASE WHEN ENGIFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Improved] END AS [Improved] ,
#             CASE WHEN ENGUFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Unchanged] END AS [Unchanged] ,
#             CASE WHEN ENGWFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Worsened] END AS [Worsened] ,
#             CASE WHEN ENGTFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Total] END AS [Total]
#     FROM #KF6 KF6
#     LEFT JOIN #KF6a KF6a ON KF6.[Lookup] = KF6a.[Lookup]
#     )_

#     DROP TABLE #KF6a

#     SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],[Organsation Name],[Measure],[Improved],
#     [Unchanged],[Worsened],[Total],
#         CASE WHEN [Improved] = '+@NINE+' OR [Total] = '+@NINE+'
#             THEN '+@NINE+'
#             ELSE CAST(CAST([Improved] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))
#         END AS [% Improved],

#         CASE WHEN [Unchanged] = '+@NINE+' OR [Total] = '+@NINE+'
#             THEN '+@NINE+'
#             ELSE CAST(CAST([Unchanged] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))
#         END AS [% Unchanged],
        
#         CASE WHEN [Worsened] = '+@NINE+' OR [Total] = '+@NINE+'
#             THEN '+@NINE+'
#             ELSE CAST(CAST([Worsened] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))
#         END AS [% Worsened]

#     INTO #KF7
#     FROM #KF6b

#     DROP TABLE #KF6b

#     select * into #KF8 from (
#         SELECT [Lookup],[Procedure],[Organisation Type],[Organisation Code],

#         CASE WHEN [Organisation Code] = ''England''
#             THEN ''England''
#             ELSE [Organsation Name]+'' (''+ [Organisation Code]+'')''
#         END AS [Organsation Name],
#         [Measure],
#         CASE WHEN [Improved] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([Improved] AS varchar (10))
#         END AS [Improved],
        
#         CASE WHEN [Unchanged] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([Unchanged] AS varchar (10))
#         END AS [Unchanged],

#         CASE WHEN [Worsened] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([Worsened] AS varchar (10))
#         END AS [Worsened],
        
#         CASE WHEN [Total] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([Total] AS varchar (10))
#         END AS [Total],
        
#         CASE WHEN [% Improved] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([% Improved] AS varchar (10))+''%''
#         END AS [% Improved],
        
#         CASE WHEN [% Unchanged] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([% Unchanged] AS varchar (10))+''%''
#         END AS [% Unchanged],
        
#         CASE WHEN [% Worsened] = '+@NINE+'
#             THEN ''*''
#             ELSE CAST([% Worsened] AS varchar (10))+''%''
#         END AS [% Worsened]
#     FROM #KF7)_

#     DROP TABLE #KF7

#     select * into #KF9a1 from #KF8 where [procedure]=''Hip Replacement''
#     select * into #KF9a2 from #KF8 where [procedure]=''Hip Replacement Primary''
#     select * into #KF9a3 from #KF8 where [procedure]=''Hip Replacement Revision''
#     select * into #KF9b1 from #KF8 where [procedure]=''Knee Replacement''
#     select * into #KF9b2 from #KF8 where [procedure]=''Knee Replacement Primary''
#     select * into #KF9b3 from #KF8 where [procedure]=''Knee Replacement Revision''
#     select * into #KF10 from (
#         select * from #KF9a1 
#     union
#     select b.[lookup],b.[Procedure],b.[Organisation Type],b.[Organisation Code],b.[Organsation Name],b.[Measure]
#     ,case when c.[Improved] = ''*'' then ''*'' else b.[Improved] end as [Improved]
#     ,case when c.[Unchanged] = ''*'' then ''*'' else b.[Unchanged] end as [Unchanged]
#     ,case when c.[Worsened] = ''*'' then ''*'' else b.[Worsened] end as [Worsened]
#     ,case when c.[Total] = ''*'' then ''*'' else b.[Total] end as [Total]
#     ,case when c.[% Improved] = ''*'' then ''*'' else b.[% Improved] end as [% Improved]
#     ,case when c.[% Unchanged] = ''*'' then ''*'' else b.[% Unchanged] end as [% Unchanged]
#     ,case when c.[% Worsened] = ''*'' then ''*'' else b.[% Worsened] end as [% Worsened]

#     from #KF9a2 b 

#     left join #KF9a3 c on b.[Organisation Code]=c.[Organisation Code] and b.[Measure]=c.[Measure]

#     union 

#     select * from #KF9a3
#     union
#     select * from #KF9b1 
#     union
#     select b.[lookup],b.[Procedure],b.[Organisation Type],b.[Organisation Code],b.[Organsation Name],b.[Measure]
#     ,case when c.[Improved] = ''*''then ''*''else b.[Improved] end as [Improved]
#     ,case when c.[Unchanged] = ''*''then ''*''else b.[Unchanged] end as [Unchanged]
#     ,case when c.[Worsened] = ''*''then ''*''else b.[Worsened] end as [Worsened]
#     ,case when c.[Total] = ''*''then ''*''else b.[Total] end as [Total]
#     ,case when c.[% Improved] = ''*''then ''*''else b.[% Improved] end as [% Improved]
#     ,case when c.[% Unchanged] = ''*''then ''*''else b.[% Unchanged] end as [% Unchanged]
#     ,case when c.[% Worsened] = ''*''then ''*''else b.[% Worsened] end as [% Worsened]
#     from #KF9b2 b 

#     left join #KF9b3 c on b.[Organisation Code]=c.[Organisation Code] and b.[Measure]=c.[Measure]
#     union 
#     select * from #KF9b3)_

#     select * from #KF10
#     --WHERE [Organsation Name] = ''England''
#     ORDER BY
#             CASE WHEN [Organsation Name] = ''England'' THEN 1
#                 ELSE 2
#             END ASC,
#             [Organisation Type],[Procedure],Measure

#     DROP TABLE #KF6
#     DROP TABLE #KF8
#     DROP TABLE #KF9a1
#     DROP TABLE #KF9a2
#     DROP TABLE #KF9a3
#     DROP TABLE #KF9b1
#     DROP TABLE #KF9b2
#     DROP TABLE #KF9b3
#     Drop Table #KF10')
#     '''
#     return keystr

def key_facts(FYEAR,DATE_TO,TABLE):

    keystr = f'''

    DECLARE @NINE INTEGER

    DECLARE @FYEAR  VARCHAR (4)

    DECLARE @END  VARCHAR (10)

    DECLARE @table VARCHAR (15)

    DECLARE @sql NVARCHAR(MAX)


    ----------------------- Update these variables as required --------------------------


    SET @NINE = '8388607'

	--CAST(0x7fffffff AS INT) -- numeric value to be suppressed

    SET @FYEAR = '{FYEAR}'	                 -- represents a financial year, the year selected is the first year of the period e.g. 2012-13 is @FYEAR 2012

	SET @END = '{DATE_TO}'				 -- year and month of the last month for this dateset

	SET @table = '{TABLE}'	         -- processing run with X suffix

    -------------------------------------------------------------------------------------

    SET NOCOUNT ON


    EXEC('

    SELECT * INTO ##proms_processing_KF1a

    FROM

    (

        SELECT 

                    Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,

                ''Provider'' AS [Organisation Type], 

                Q._Q1_PROCODE AS [Organisation Code],

                ''Index'' AS Measure,		

                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 

                END AS Improved,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) 

                END AS Unchanged,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 

                END AS Worsened,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(Q.Q2_EQ5D_INDEX) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._INDEX_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._Q1_PROCODE


    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,

                ''CCG of GP Practice'' AS [Organisation Type], 

                P.ccg_code AS [Organisation Code],

                ''Index'' AS Measure,

                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 

                END AS Improved,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END)

                END AS Unchanged,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 

                END AS Worsened,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_INDEX) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._INDEX_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code

    
    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,

            ''England'' AS [Organisation Type], 

            ''England'' AS [Organisation Code],

            ''Index'' AS Measure,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) AS Improved,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) AS Unchanged,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) AS Worsened,

            COUNT(Q.Q2_EQ5D_INDEX) AS TOTAL

            
    FROM proms.QUESTS_'+@table+' Q

    WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

    AND Q._INDEX_CHANGE_FLAG = 1

    AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

    GROUP BY Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE

    
    UNION

        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

            ''Provider'' AS [Organisation Type],   

            Q._Q1_PROCODE AS [Organisation Code],

            ''VAS'' AS Measure,

            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 

            END AS Improved,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 

                THEN '+@NINE+'

                ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 

            END AS Unchanged,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 

            END AS Worsened,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 

            END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY Q._Q1_FYEAR, Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._Q1_PROCODE

    
    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

                ''CCG of GP Practice'' AS [Organisation Type], 

                P.ccg_code AS [Organisation Code],

                ''VAS'' AS Measure,

                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 

                END AS Improved,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 

                END AS Unchanged,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 

                END AS Worsened,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code


    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

                ''England'' AS [Organisation Type], 

                ''England'' AS [Organisation Code],

                ''VAS'' AS Measure,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) AS Improved,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) AS Unchanged,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) AS Worsened,

                COUNT(Q.Q2_EQ5D_HEALTH_SCALE) AS TOTAL

            
        FROM proms.QUESTS_'+@table+' Q

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE

            
    UNION

        SELECT 

                Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

                ''Provider'' AS [Organisation Type], 	 

                Q._Q1_PROCODE AS [Organisation Code],

                Q._CS_CODE AS Measure,

                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 

                END AS Improved,

                        
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 

                END AS Unchanged,

                
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) 

                END AS Worsened,

                        
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_CS_SCORE) 

                END AS TOTAL

                        
        FROM proms.QUESTS_'+@table+' Q

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE, Q._Q1_PROCODE,Q._CS_CODE

        
    UNION

    
        SELECT 

                    Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

                    ''CCG of GP Practice'' AS [Organisation Type],	

                    P.ccg_code AS [Organisation Code],

                    Q._CS_CODE AS Measure,

                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 

                    END AS Improved,

                            
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 

                    END AS Unchanged,

                    
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR   Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV''THEN ''D'' END) 

                    END AS Worsened,

                            
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(Q.Q2_CS_SCORE) 

                    END AS TOTAL

                    
        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,P.ccg_code,Q._CS_CODE

        
    UNION

    
        SELECT 

                    Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,  

                    ''England'' AS [Organisation Type], 

                    ''England'' AS [Organisation Code],

                    Q._CS_CODE AS Measure,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) AS Improved,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) AS Unchanged,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) AS Worsened,


                    COUNT(Q.Q2_CS_SCORE) AS TOTAL

                
        FROM proms.QUESTS_'+@table+' Q

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        GROUP BY  Q.PROMS_PROC_CODE,Q._PRIM_REV_PROC_CODE,Q._CS_CODE

    )_



    SELECT * INTO ##proms_processing_KF1b

    FROM

    (

        SELECT 

                    Q.PROMS_PROC_CODE,

                ''Provider'' AS [Organisation Type], 

                Q._Q1_PROCODE AS [Organisation Code],

                ''Index'' AS Measure,		

                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 

                END AS Improved,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) 

                END AS Unchanged,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5

                        AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 

                END AS Worsened,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(Q.Q2_EQ5D_INDEX) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._INDEX_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,Q._Q1_PROCODE


    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,

                ''CCG of GP Practice'' AS [Organisation Type], 

                P.ccg_code AS [Organisation Code],

                ''Index'' AS Measure,

                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) 

                END AS Improved,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END)

                END AS Unchanged,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) 

                END AS Worsened,

                    
                CASE WHEN COUNT(Q.Q2_EQ5D_INDEX) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_INDEX) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._INDEX_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code

    
    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,

            ''England'' AS [Organisation Type], 

            ''England'' AS [Organisation Code],

            ''Index'' AS Measure,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX > Q.Q1_EQ5D_INDEX THEN ''I'' END) AS Improved,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX = Q.Q1_EQ5D_INDEX THEN ''S'' END) AS Unchanged,

            COUNT(CASE WHEN Q.Q2_EQ5D_INDEX < Q.Q1_EQ5D_INDEX THEN ''D'' END) AS Worsened,

            COUNT(Q.Q2_EQ5D_INDEX) AS TOTAL

            
    FROM proms.QUESTS_'+@table+' Q

    WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

    AND Q._INDEX_CHANGE_FLAG = 1

    AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

    GROUP BY Q.PROMS_PROC_CODE

    
    UNION

        SELECT 

                Q.PROMS_PROC_CODE, 

            ''Provider'' AS [Organisation Type],   

            Q._Q1_PROCODE AS [Organisation Code],

            ''VAS'' AS Measure,

            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 

            END AS Improved,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 

                THEN '+@NINE+'

                ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 

            END AS Unchanged,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 

            END AS Worsened,

                
            CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 

            END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY Q._Q1_FYEAR, Q.PROMS_PROC_CODE,Q._Q1_PROCODE

    
    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE,

                ''CCG of GP Practice'' AS [Organisation Type], 

                P.ccg_code AS [Organisation Code],

                ''VAS'' AS Measure,

                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) 

                END AS Improved,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) 

                END AS Unchanged,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END)BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) 

                END AS Worsened,

                
                CASE WHEN COUNT(Q.Q2_EQ5D_HEALTH_SCALE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_EQ5D_HEALTH_SCALE) 

                END AS TOTAL


        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code


    UNION

    
        SELECT 

                Q.PROMS_PROC_CODE, 

                ''England'' AS [Organisation Type], 

                ''England'' AS [Organisation Code],

                ''VAS'' AS Measure,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE > Q.Q1_EQ5D_HEALTH_SCALE THEN ''I'' END) AS Improved,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE = Q.Q1_EQ5D_HEALTH_SCALE THEN ''S'' END) AS Unchanged,

                COUNT(CASE WHEN Q.Q2_EQ5D_HEALTH_SCALE < Q.Q1_EQ5D_HEALTH_SCALE THEN ''D'' END) AS Worsened,

                COUNT(Q.Q2_EQ5D_HEALTH_SCALE) AS TOTAL

            
        FROM proms.QUESTS_'+@table+' Q

        WHERE  Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCALE_CHANGE_FLAG = 1

        AND Q.PROMS_PROC_CODE in (''hr'',''kr'')

        GROUP BY Q.PROMS_PROC_CODE

            
    UNION

        SELECT 

                Q.PROMS_PROC_CODE,

                ''Provider'' AS [Organisation Type], 	 

                Q._Q1_PROCODE AS [Organisation Code],

                Q._CS_CODE AS Measure,

                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 

                END AS Improved,

                        
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 

                END AS Unchanged,

                
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) 

                END AS Worsened,

                        
                CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                    THEN '+@NINE+'

                    ELSE COUNT(Q.Q2_CS_SCORE) 

                END AS TOTAL

                        
        FROM proms.QUESTS_'+@table+' Q

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        AND Q._Q1_PROCODE IS NOT NULL

        GROUP BY  Q.PROMS_PROC_CODE, Q._Q1_PROCODE,Q._CS_CODE

        
    UNION

    
        SELECT 

                    Q.PROMS_PROC_CODE, 

                    ''CCG of GP Practice'' AS [Organisation Type],	

                    P.ccg_code AS [Organisation Code],

                    Q._CS_CODE AS Measure,

                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) 

                    END AS Improved,

                            
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) 

                    END AS Unchanged,

                    
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        AND  COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                        OR   Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV''THEN ''D'' END) 

                    END AS Worsened,

                            
                    CASE WHEN COUNT(Q.Q2_CS_SCORE) BETWEEN 1 AND 5 

                        THEN '+@NINE+'

                        ELSE COUNT(Q.Q2_CS_SCORE) 

                    END AS TOTAL

                    
        FROM proms.QUESTS_'+@table+' Q

        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P

        ON Q._P_REF_PROM = P._P_REF_PROM

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        AND P.ccg_code IS NOT NULL

        GROUP BY  Q.PROMS_PROC_CODE,P.ccg_code,Q._CS_CODE

        
    UNION

    
        SELECT 

                    Q.PROMS_PROC_CODE,

                    ''England'' AS [Organisation Type], 

                    ''England'' AS [Organisation Code],

                    Q._CS_CODE AS Measure,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''I'' END) AS Improved,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE = Q.Q1_CS_SCORE THEN ''S'' END) AS Unchanged,


                    COUNT(CASE WHEN Q.Q2_CS_SCORE < Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE IN (''KR'',''HR'') 

                    OR Q.Q2_CS_SCORE > Q.Q1_CS_SCORE AND Q.PROMS_PROC_CODE = ''VV'' THEN ''D'' END) AS Worsened,


                    COUNT(Q.Q2_CS_SCORE) AS TOTAL

                
        FROM proms.QUESTS_'+@table+' Q

        WHERE Q.PROMS_PROC_CODE IN (''hr'',''kr'')

        AND Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'

        AND Q._Q1_YEAR_MONTH <= \'\'\'+@END+\'\'\'

        AND Q._SCORE_CHANGE_FLAG = 1

        GROUP BY  Q.PROMS_PROC_CODE,Q._CS_CODE

    ) KF1


    SELECT * INTO ##proms_processing_KF2

    FROM

    (

    SELECT

            RP.[Description] AS [Procedure],

            K.[Organisation Type],

            [Organisation Code],

        
            CASE WHEN K.[Organisation Type]= ''England'' THEN ''England''

                WHEN K.[Organisation Type]= ''CCG of GP Practice'' AND K.[Organisation Code]= ''---'' THEN ''Unknown''

                ELSE ISNULL(O.OrgName,''Unknown'')

            END AS [Organsation Name],

        
            RM.[Description] AS [Measure],

            K.[Improved],

            K.[Unchanged],

            K.[Worsened],

            K.[Total],

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Improved] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS IFLAG,

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Unchanged] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS UFLAG,

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Worsened] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS WFLAG

        
    FROM ##proms_processing_KF1b K

    LEFT JOIN proms.REF_ORGS_'+@table+' O

    ON o.OrgCode = K.[Organisation Code]

    LEFT JOIN proms.REF_PROCEDURES RP

    ON K.PROMS_PROC_CODE = RP.PROMs_PROC_CODE

    LEFT JOIN proms.REF_MEASURES RM

    ON K.[Measure] = RM.Measure


    union


    SELECT

            RP.[Description] AS [Procedure],

            K.[Organisation Type],

            [Organisation Code],

        
            CASE WHEN K.[Organisation Type]= ''England'' THEN ''England''

                WHEN K.[Organisation Type]= ''CCG of GP Practice'' AND K.[Organisation Code]= ''---'' THEN ''Unknown''

                ELSE ISNULL(O.OrgName,''Unknown'')

            END AS [Organsation Name],

        
            RM.[Description] AS [Measure],

            K.[Improved],

            K.[Unchanged],

            K.[Worsened],

            K.[Total],

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Improved] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS IFLAG,

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Unchanged] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS UFLAG,

            CASE WHEN K.[Organisation Type] = ''Provider'' AND K.[Worsened] = '+@NINE+' THEN RP.[Description]+RM.[Description] END AS WFLAG

        
    FROM ##proms_processing_KF1a K

    LEFT JOIN proms.REF_ORGS_'+@table+' O

    ON o.OrgCode = K.[Organisation Code]

    LEFT JOIN proms.REF_PROCEDURES RP

    ON K._PRIM_REV_PROC_CODE = RP.PROMs_PROC_CODE

    LEFT JOIN proms.REF_MEASURES RM

    ON K.[Measure] = RM.Measure

    where k._PRIM_REV_PROC_CODE not in (''hr'',''kr'')



    )KF2


    DROP TABLE ##proms_processing_KF1a

    DROP TABLE ##proms_processing_KF1b


    --Contains all the Improved Flags that need secondary suppression

    SELECT * INTO #KFX

    FROM

    (

    SELECT

        CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY IFLAG) = 1 

            THEN IFLAG END AS IFLAG

    FROM ##proms_processing_KF2)KFX

    --Contains all the Unchanged Flags that need secondary suppression

    SELECT * INTO #KFY

    FROM

    (

    SELECT

        CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY UFLAG) = 1 

            THEN UFLAG END AS UFLAG

    FROM ##proms_processing_KF2)KFY

    --Contains all the Worsened Flags that need secondary suppression

    SELECT * INTO #KFZ

    FROM

    (

    SELECT

        CASE WHEN COUNT('+@NINE+') OVER (PARTITION BY WFLAG) = 1 

            THEN WFLAG END AS WFLAG

    FROM ##proms_processing_KF2)KFZ


    SELECT * INTO #KF3

    FROM

    (

        SELECT 

                CASE WHEN KF2.[Organisation Type] = ''England''

                    THEN KF2.[Organisation Type]+KF2.[Organsation Name]+KF2.[Procedure]+KF2.[Measure]

                    ELSE KF2.[Organisation Type]+KF2.[Organsation Name]+'' (''+KF2.[Organisation Code]+'')''+KF2.[Procedure]+KF2.[Measure]

                END AS [Lookup],

                KF2.[Procedure],

                KF2.[Organisation Type],

                KF2.[Organisation Code],

                KF2.[Organsation Name],

                KF2.[Measure],

                KF2.[Improved],

                KF2.[Unchanged],

                KF2.[Worsened],

                KF2.[Total],

                KFX.IFLAG,

                KFY.UFLAG,

                KFZ.WFLAG


        FROM ##proms_processing_KF2 KF2

        LEFT JOIN #KFX KFX

        ON KF2.IFLAG = KFX.IFLAG

        LEFT JOIN #KFY KFY

        ON KF2.UFLAG = KFY.UFLAG

        LEFT JOIN #KFZ KFZ

        ON KF2.WFLAG = KFZ.WFLAG

    )KF3


    DROP TABLE ##proms_processing_KF2

    DROP TABLE #KFX

    DROP TABLE #KFY

    DROP TABLE #KFZ



    --Applies secondary suppression for Provider Improved, if needed

    --Identifies Procedures and Measures to be supressed


    SELECT * INTO #IFLAG

    FROM

    (

        SELECT

            IFLAG

        FROM #KF3 

        WHERE IFLAG IS NOT NULL

    )KF3A


    --Applies suppression to seleced dataset and joins to main data set

    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            CASE WHEN IFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Improved] END AS [Improved],

            [Unchanged],

            [Worsened],

            CASE WHEN IFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],

            IFLAG,

            UFLAG,

            WFLAG

    INTO #KF4

    FROM

    (

        SELECT 

                KF3B.[Lookup],

                KF3B.[Procedure],

                KF3B.[Organisation Type],

                KF3B.[Organisation Code],

                KF3B.[Organsation Name],

                KF3B.[Measure],

                KF3B.[Improved],

                KF3B.[Unchanged],

                KF3B.[Worsened],

                KF3B.[Total],

                KF3A.IFLAG,

                KF3B.UFLAG,

                KF3B.WFLAG,

                ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure]

                                    ORDER BY [Total]ASC)AS CLASS

        FROM #KF3 KF3B

        LEFT JOIN #IFLAG KF3A

        ON KF3A.IFLAG = KF3B.[Procedure]+KF3B.Measure

        WHERE KF3B.WFLAG IS NULL

        AND KF3B.[Organisation Type]= ''Provider''

        AND KF3B.Improved > 0

        AND KF3B.Improved < '+@NINE+'

    )_


    UNION


    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            [Improved],

            [Unchanged],

            [Worsened],

            [Total],

            IFLAG,

            UFLAG,

            WFLAG 

    FROM #KF3

    WHERE [Lookup] NOT IN

    (

        SELECT 

            KF3B.[Lookup]

            FROM #KF3 KF3B

            LEFT JOIN #IFLAG KF3A

            ON KF3A.IFLAG = KF3B.[Procedure]+KF3B.Measure

            WHERE KF3B.WFLAG IS NULL

            AND KF3B.[Organisation Type]= ''Provider''

            AND KF3B.Improved > 0

            AND KF3B.Improved < '+@NINE+'

    )


    DROP TABLE #KF3

    DROP TABLE #IFLAG



    --SELECT * FROM #KF4

    --DROP TABLE #KF4

    --Applies secondary suppression for Provider Unchanged, if needed

    --Identifies Procedures and Measures to be supressed


    SELECT * INTO #UFLAG

    FROM

    (

        SELECT

            UFLAG

        FROM #KF4 

        WHERE UFLAG IS NOT NULL

    )KF4A



    --SELECT * FROM #UFLAG

    --Applies suppression to seleced dataset and joins to main data set

    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            [Improved],

            CASE WHEN UFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Unchanged] END AS [Unchanged],

            [Worsened],

            CASE WHEN UFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],

            IFLAG,

            UFLAG,

            WFLAG

    INTO #KF5

    FROM

    (

        SELECT 

            KF4B.[Lookup],

            KF4B.[Procedure],

            KF4B.[Organisation Type],

            KF4B.[Organisation Code],

            KF4B.[Organsation Name],

            KF4B.[Measure],

            KF4B.[Improved],

            KF4B.[Unchanged],

            KF4B.[Worsened],

            KF4B.[Total],

            KF4B.IFLAG,

            KF4A.UFLAG,

            KF4B.WFLAG,

            ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure]

                                ORDER BY [Total]ASC)AS CLASS

        FROM #KF4 KF4B

        LEFT JOIN #UFLAG KF4A

        ON KF4A.UFLAG = KF4B.[Procedure]+KF4B.Measure

        WHERE KF4B.WFLAG IS NULL

        AND KF4B.[Organisation Type]= ''Provider''

        AND KF4B.Unchanged > 0

        AND KF4B.Improved < '+@NINE+'

    )_


    UNION


    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            [Improved],

            [Unchanged],

            [Worsened],

            [Total],

            IFLAG,

            UFLAG,

            WFLAG 

    FROM #KF4

    WHERE [Lookup] NOT IN

    (

        SELECT 

            KF4B.[Lookup]

            FROM #KF4 KF4B

            LEFT JOIN #UFLAG KF4A

            ON KF4A.UFLAG = KF4B.[Procedure]+KF4B.Measure

            WHERE KF4B.WFLAG IS NULL

            AND KF4B.[Organisation Type]= ''Provider''

            AND KF4B.Unchanged > 0

            AND KF4B.Unchanged < '+@NINE+'

    )


    DROP TABLE #KF4

    DROP TABLE #UFLAG


    --Applies secondary suppression for Provider Worsened, if needed

    --Identifies Procedures and Measures to be supressed


    SELECT * INTO #WFLAG

    FROM

    (

    SELECT

        WFLAG

    FROM #KF5 

    WHERE WFLAG IS NOT NULL

    )KF5A


    --Applies suppression to seleced dataset and joins to main data set


    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            [Improved],

            [Unchanged],

            CASE WHEN WFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Worsened] END AS [Worsened],

            CASE WHEN WFLAG IS NOT NULL AND CLASS = 1 THEN '+@NINE+' ELSE [Total] END AS [Total],

            IFLAG,

            UFLAG,

            WFLAG

    INTO #KF6

    FROM

    (

        SELECT 

            KF5B.[Lookup],

            KF5B.[Procedure],

            KF5B.[Organisation Type],

            KF5B.[Organisation Code],

            KF5B.[Organsation Name],

            KF5B.[Measure],

            KF5B.[Improved],

            KF5B.[Unchanged],

            KF5B.[Worsened],

            KF5B.[Total],

            KF5B.IFLAG,

            KF5B.UFLAG,

            KF5A.WFLAG,

            ROW_NUMBER()OVER(PARTITION BY [Procedure], [Measure]

                                ORDER BY [Total]ASC)AS CLASS

        FROM #KF5 KF5B

        LEFT JOIN #WFLAG KF5A

        ON KF5A.WFLAG = KF5B.[Procedure]+KF5B.Measure

        WHERE KF5B.WFLAG IS NULL

        AND KF5B.[Organisation Type]= ''Provider''

        AND KF5B.Worsened > 0

        AND KF5B.Worsened < '+@NINE+'

    )_


    UNION


    SELECT 

            [Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            [Improved],

            [Unchanged],

            [Worsened],

            [Total],

            IFLAG,

            UFLAG,

            WFLAG 

    FROM #KF5

    WHERE [Lookup] NOT IN

    (

    SELECT 

        KF5B.[Lookup]

        FROM #KF5 KF5B

        LEFT JOIN #WFLAG KF5A

        ON KF5A.WFLAG = KF5B.[Procedure]+KF5B.Measure

        WHERE KF5B.WFLAG IS NULL

        AND KF5B.[Organisation Type]= ''Provider''

        AND KF5B.Worsened > 0

        AND KF5B.Worsened < '+@NINE+'

    )


    DROP TABLE #KF5

    DROP TABLE #WFLAG


    SELECT * INTO #KF6a

    FROM

    (

    SELECT	

            ''ENGLANDENGLAND''+[Procedure]+[Measure] AS ''Lookup'',

            CASE WHEN SUM(ENGIFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGIFLAG,

            CASE WHEN SUM(ENGUFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGUFLAG,

            CASE WHEN SUM(ENGWFLAG) = 1 THEN '+@NINE+' ELSE 0 END AS ENGWFLAG,

            CASE WHEN (SUM(ENGIFLAG) = 1 OR SUM(ENGUFLAG) = 1 OR SUM(ENGWFLAG) = 1) THEN '+@NINE+' ELSE 0 END AS ENGTFLAG

    FROM

    (

    SELECT  

            [Procedure],

            [Measure],

            CASE WHEN [Improved] = '+@NINE+' THEN 1 ELSE 0 END AS ENGIFLAG,

            CASE WHEN [Unchanged] = '+@NINE+' THEN 1 ELSE 0 END AS ENGUFLAG,

            CASE WHEN [Worsened] = '+@NINE+' THEN 1 ELSE 0 END AS ENGWFLAG


    FROM #KF6

    WHERE [Organisation Type] = ''Provider''

    )_

    GROUP BY [Procedure],[Measure] 

    )_


    SELECT * INTO #KF6b

    FROM

    (

    SELECT

            KF6.[Lookup],

            [Procedure],

            [Organisation Type],

            [Organisation Code],

            [Organsation Name],

            [Measure],

            CASE WHEN ENGIFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Improved] END AS [Improved] ,

            CASE WHEN ENGUFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Unchanged] END AS [Unchanged] ,

            CASE WHEN ENGWFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Worsened] END AS [Worsened] ,

            CASE WHEN ENGTFLAG = '+@NINE+' THEN '+@NINE+' ELSE [Total] END AS [Total]



    FROM #KF6 KF6

    LEFT JOIN #KF6a KF6a

    ON KF6.[Lookup] = KF6a.[Lookup]

    )_

    DROP TABLE #KF6a


    SELECT


        [Lookup],

        [Procedure],

        [Organisation Type],

        [Organisation Code],

        [Organsation Name],

        [Measure],

        [Improved],

        [Unchanged],

        [Worsened],

        [Total],

        CASE WHEN [Improved] = '+@NINE+' OR [Total] = '+@NINE+'

            THEN '+@NINE+'

            ELSE CAST(CAST([Improved] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))

        END AS [% Improved],

        
        CASE WHEN [Unchanged] = '+@NINE+' OR [Total] = '+@NINE+'

            THEN '+@NINE+'

            ELSE CAST(CAST([Unchanged] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))

        END AS [% Unchanged],

        
        CASE WHEN [Worsened] = '+@NINE+' OR [Total] = '+@NINE+'

            THEN '+@NINE+'

            ELSE CAST(CAST([Worsened] AS DECIMAL (10,1))/CAST([Total] AS DECIMAL (10,1))*100 AS DECIMAL (10,1))

        END AS [% Worsened]


    INTO #KF7

    FROM #KF6b


    DROP TABLE #KF6b


    select * into #KF8 from (


    SELECT


        [Lookup],

        [Procedure],

        [Organisation Type],

        [Organisation Code],

        CASE WHEN [Organisation Code] = ''England''

            THEN ''England''

            ELSE [Organsation Name]+'' (''+ [Organisation Code]+'')''

        END AS [Organsation Name],

        [Measure],

        CASE WHEN [Improved] = '+@NINE+'

            THEN ''*''

            ELSE CAST([Improved] AS varchar (10))

        END AS [Improved],

        
        CASE WHEN [Unchanged] = '+@NINE+'

            THEN ''*''

            ELSE CAST([Unchanged] AS varchar (10))

        END AS [Unchanged],

        
        CASE WHEN [Worsened] = '+@NINE+'

            THEN ''*''

            ELSE CAST([Worsened] AS varchar (10))

        END AS [Worsened],

        
        CASE WHEN [Total] = '+@NINE+'

            THEN ''*''

            ELSE CAST([Total] AS varchar (10))

        END AS [Total],

        
        CASE WHEN [% Improved] = '+@NINE+'

            THEN ''*''

            ELSE CAST([% Improved] AS varchar (10))+''%''

        END AS [% Improved],

        
        CASE WHEN [% Unchanged] = '+@NINE+'

            THEN ''*''

            ELSE CAST([% Unchanged] AS varchar (10))+''%''

        END AS [% Unchanged],

        
        CASE WHEN [% Worsened] = '+@NINE+'

            THEN ''*''

            ELSE CAST([% Worsened] AS varchar (10))+''%''

        END AS [% Worsened]

        
    FROM #KF7)_


    DROP TABLE #KF7


    select * into #KF9a1 from #KF8 where [procedure]=''Hip Replacement''

    select * into #KF9a2 from #KF8 where [procedure]=''Hip Replacement Primary''

    select * into #KF9a3 from #KF8 where [procedure]=''Hip Replacement Revision''


    select * into #KF9b1 from #KF8 where [procedure]=''Knee Replacement''

    select * into #KF9b2 from #KF8 where [procedure]=''Knee Replacement Primary''

    select * into #KF9b3 from #KF8 where [procedure]=''Knee Replacement Revision''



    select * into #KF10 from (


    select * from #KF9a1 

    union

    select 

    b.[lookup]

    ,b.[Procedure]

    ,b.[Organisation Type]

    ,b.[Organisation Code]

    ,b.[Organsation Name]

    ,b.[Measure]

    ,case when c.[Improved] = ''*'' then ''*'' else b.[Improved] end as [Improved]

    ,case when c.[Unchanged] = ''*'' then ''*'' else b.[Unchanged] end as [Unchanged]

    ,case when c.[Worsened] = ''*'' then ''*'' else b.[Worsened] end as [Worsened]

    ,case when c.[Total] = ''*'' then ''*'' else b.[Total] end as [Total]

    ,case when c.[% Improved] = ''*'' then ''*'' else b.[% Improved] end as [% Improved]

    ,case when c.[% Unchanged] = ''*'' then ''*'' else b.[% Unchanged] end as [% Unchanged]

    ,case when c.[% Worsened] = ''*'' then ''*'' else b.[% Worsened] end as [% Worsened]


    from #KF9a2 b 

    left join #KF9a3 c on b.[Organisation Code]=c.[Organisation Code] and b.[Measure]=c.[Measure]


    union 

    select * from #KF9a3


    union


    select * from #KF9b1 

    union

    select 

    b.[lookup]

    ,b.[Procedure]

    ,b.[Organisation Type]

    ,b.[Organisation Code]

    ,b.[Organsation Name]

    ,b.[Measure]

    ,case when c.[Improved] = ''*''then ''*''else b.[Improved] end as [Improved]

    ,case when c.[Unchanged] = ''*''then ''*''else b.[Unchanged] end as [Unchanged]

    ,case when c.[Worsened] = ''*''then ''*''else b.[Worsened] end as [Worsened]

    ,case when c.[Total] = ''*''then ''*''else b.[Total] end as [Total]

    ,case when c.[% Improved] = ''*''then ''*''else b.[% Improved] end as [% Improved]

    ,case when c.[% Unchanged] = ''*''then ''*''else b.[% Unchanged] end as [% Unchanged]

    ,case when c.[% Worsened] = ''*''then ''*''else b.[% Worsened] end as [% Worsened]


    from #KF9b2 b 

    left join #KF9b3 c on b.[Organisation Code]=c.[Organisation Code] and b.[Measure]=c.[Measure]


    union 

    select * from #KF9b3)_


    select * from #KF10

    --WHERE [Organsation Name] = ''England''

    ORDER BY

            CASE WHEN [Organsation Name] = ''England'' THEN 1

                ELSE 2

            END ASC,

            [Organisation Type],

            [Procedure],

            Measure



    DROP TABLE #KF6

    DROP TABLE #KF8

    DROP TABLE #KF9a1

    DROP TABLE #KF9a2

    DROP TABLE #KF9a3

    DROP TABLE #KF9b1

    DROP TABLE #KF9b2

    DROP TABLE #KF9b3

    Drop Table #KF10')

    '''

    return keystr
