def equality(startfyear,table):
    yearmonth=f'{int(startfyear)+1}-03'
    equality_str = f'''
        DECLARE @FYEAR  VARCHAR (4);
        DECLARE @END  VARCHAR (10);
        DECLARE @table VARCHAR (15);
        DECLARE @sql NVARCHAR(MAX);

        ----------------------- Update these variables as required --------------------------

        SET @FYEAR = '{startfyear}'		    -- represents a financial year, the year selected is the first year of the period e.g. 2012-13 is @FYEAR 2012
        SET @END = '{yearmonth}'		-- year and month of the last month for this dateset
        SET @table = '{table}'	-- processing run with X suffix
        -------------------------------------------------------------------------------------
        --a full years data will take just over 13 minutes to run


        SET @sql =
        '
        SELECT * INTO ##proms_processing_EQ1
        FROM
        (
            SELECT 
                    P._AGE_GROUP_5YR AS AGE,
                    P._AGE_GENDER_5YR AS AGE_GENDER,
                    CAST(Q.Q1_DISABILITY AS VARCHAR) AS DISABILITY,
                    P.ETHNICITY,
                    CAST(P.SEX AS VARCHAR) AS GENDER,
                    P._IMD_GROUP AS IMD,
                    RP.[Description] AS [Procedure],
                    RM.[Description] AS ''CS_Measure'',
                    Q.Q1_EQ5D_INDEX,
                    Q.Q2_EQ5D_INDEX,
                    Q.EQ5D_INDEX_CHANGE,
                    CASE WHEN Q.EQ5D_INDEX_CHANGE > 0 THEN ''I'' 
                        WHEN Q.EQ5D_INDEX_CHANGE = 0 THEN ''U''
                        WHEN Q.EQ5D_INDEX_CHANGE < 0 THEN ''W''
                    END AS EQ5D_INDEX_CHANGE_FLAG,
                    Q._INDEX_CHANGE_FLAG AS ''IFLAG'',
                    Q.Q1_EQ5D_HEALTH_SCALE,
                    Q.Q2_EQ5D_HEALTH_SCALE,
                    Q.EQ5D_SCALE_CHANGE,
                    CASE WHEN Q.EQ5D_SCALE_CHANGE > 0 THEN ''I'' 
                        WHEN Q.EQ5D_SCALE_CHANGE = 0 THEN ''U''
                        WHEN Q.EQ5D_SCALE_CHANGE < 0 THEN ''W''
                    END AS EQ5D_SCALE_CHANGE_FLAG,
                    Q._SCALE_CHANGE_FLAG AS ''SFLAG'',
                    Q.Q1_CS_SCORE,
                    Q.Q2_CS_SCORE,
                    Q._CS_SCORE_CHANGE,
                    CASE WHEN Q._CS_SCORE_CHANGE > 0 THEN ''I'' 
                        WHEN Q._CS_SCORE_CHANGE = 0 THEN ''U''
                        WHEN Q._CS_SCORE_CHANGE < 0 THEN ''W''
                    END AS _CS_SCORE_CHANGE_FLAG,
                    Q._SCORE_CHANGE_FLAG AS ''CFLAG''
                    
                FROM proms.QUESTS_'+@table+' Q
                LEFT JOIN proms.HES_PROCEDURES_'+@table+' P
                ON Q._P_REF_PROM = P._P_REF_PROM
                LEFT JOIN proms.REF_PROCEDURES RP
                ON Q.PROMS_PROC_CODE = RP.PROMs_PROC_CODE
                LEFT JOIN proms.REF_MEASURES RM
                ON Q._CS_CODE = RM.Measure
                WHERE Q._Q1_FYEAR = \'\'\'+@FYEAR+\'\'\'
                AND Q._EPISODE_MATCHED = 1
                AND P._P_REF_PROM IS NOT NULL

        )_
        '
        EXEC sp_executesql @sql;

        CREATE TABLE #EQ2
        (
            [Dimension] varchar (50),
            [Value] varchar (95),
            [Procedure] varchar (25),
            [Measure] varchar (45),
            [Q1_EQ5D_INDEX] decimal (30,10),
            [Q2_EQ5D_INDEX] decimal (30,10),
            [HealthGain] decimal (30,10),
            [Improved] integer,
            [Unchanged] integer,
            [Worsened] integer	
        )

        INSERT INTO #EQ2
        SELECT
                'Age' AS Dimension,
                AGE AS Value,
                [Procedure],
                'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
            
        FROM ##proms_processing_EQ1
        WHERE AGE IS NOT NULL
        AND IFLAG = 1

        INSERT INTO #EQ2
        SELECT
                'Age and Gender' AS Dimension,
                AGE_GENDER AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE AGE_GENDER IS NOT NULL
        AND IFLAG = 1

        INSERT INTO #EQ2
        SELECT
                'Disability' AS Dimension,
                DISABILITY AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE DISABILITY IS NOT NULL
        AND IFLAG = 1

        INSERT INTO #EQ2
        SELECT
                'Ethnicity' AS Dimension,
                ETHNICITY AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE ETHNICITY IS NOT NULL
        AND IFLAG = 1

        INSERT INTO #EQ2
        SELECT
                'Gender' AS Dimension,
                GENDER AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE GENDER IS NOT NULL
        AND IFLAG = 1

        INSERT INTO #EQ2
        SELECT
                'Index of Multiple Deprivation' AS Dimension,
                IMD AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE IMD IS NOT NULL
        AND IFLAG = 1
            
        INSERT INTO #EQ2
        SELECT
                'ENGLAND' AS Dimension,
                'ENGLAND' AS Value,
                [Procedure],
            'EQ-5D Index' AS Measure,
                Q1_EQ5D_INDEX,
                Q2_EQ5D_INDEX,
                EQ5D_INDEX_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_INDEX_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE IFLAG = 1

        --EQ VAS

        CREATE TABLE #EQ3
        (
            [Dimension] varchar (50),
            [Value] varchar (95),
            [Procedure] varchar (25),
            [Measure] varchar (45),
            [Q1_EQ5D_HEALTH_SCALE] decimal (30,10),
            [Q2_EQ5D_HEALTH_SCALE] decimal (30,10),
            [HealthGain] decimal (30,10),
            [Improved] integer,
            [Unchanged] integer,
            [Worsened] integer	
        )

        INSERT INTO #EQ3
        SELECT
                'Age' AS Dimension,
                AGE AS Value,
                [Procedure],
                'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
            
        FROM ##proms_processing_EQ1
        WHERE AGE IS NOT NULL
        AND SFLAG = 1

        INSERT INTO #EQ3
        SELECT
                'Age and Gender' AS Dimension,
                AGE_GENDER AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE AGE_GENDER IS NOT NULL
        AND SFLAG = 1

        INSERT INTO #EQ3
        SELECT
                'Disability' AS Dimension,
                DISABILITY AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE DISABILITY IS NOT NULL
        AND SFLAG = 1

        INSERT INTO #EQ3
        SELECT
                'Ethnicity' AS Dimension,
                ETHNICITY AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE ETHNICITY IS NOT NULL
        AND SFLAG = 1

        INSERT INTO #EQ3
        SELECT
                'Gender' AS Dimension,
                GENDER AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE GENDER IS NOT NULL
        AND SFLAG = 1

        INSERT INTO #EQ3
        SELECT
                'Index of Multiple Deprivation' AS Dimension,
                IMD AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE IMD IS NOT NULL
        AND SFLAG = 1
            
        INSERT INTO #EQ3
        SELECT
                'ENGLAND' AS Dimension,
                'ENGLAND' AS Value,
                [Procedure],
            'EQ VAS' AS Measure,
                Q1_EQ5D_HEALTH_SCALE,
                Q2_EQ5D_HEALTH_SCALE,
                EQ5D_SCALE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN EQ5D_SCALE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE SFLAG = 1

        --CS

        CREATE TABLE #EQ4
        (
            [Dimension] varchar (50),
            [Value] varchar (95),
            [Procedure] varchar (25),
            [Measure] varchar (45),
            [Q1_CS_SCORE] decimal (30,10),
            [Q2_CS_SCORE] decimal (30,10),
            [HealthGain] decimal (30,10),
            [Improved] integer,
            [Unchanged] integer,
            [Worsened] integer	
        )

        INSERT INTO #EQ4
        SELECT
                'Age' AS Dimension,
                AGE AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
            
        FROM ##proms_processing_EQ1
        WHERE AGE IS NOT NULL
        AND CFLAG = 1

        INSERT INTO #EQ4
        SELECT
                'Age and Gender' AS Dimension,
                AGE_GENDER AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE AGE_GENDER IS NOT NULL
        AND CFLAG = 1

        INSERT INTO #EQ4
        SELECT
                'Disability' AS Dimension,
                DISABILITY AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE DISABILITY IS NOT NULL
        AND CFLAG = 1

        INSERT INTO #EQ4
        SELECT
                'Ethnicity' AS Dimension,
                ETHNICITY AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE ETHNICITY IS NOT NULL
        AND CFLAG = 1

        INSERT INTO #EQ4
        SELECT
                'Gender' AS Dimension,
                GENDER AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE GENDER IS NOT NULL
        AND CFLAG = 1

        INSERT INTO #EQ4
        SELECT
                'Index of Multiple Deprivation' AS Dimension,
                IMD AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE IMD IS NOT NULL
        AND CFLAG = 1
            
        INSERT INTO #EQ4
        SELECT
                'ENGLAND' AS Dimension,
                'ENGLAND' AS Value,
                [Procedure],
                CS_Measure AS Measure,
                Q1_CS_SCORE,
                Q2_CS_SCORE,
                _CS_SCORE_CHANGE AS 'HEALTH_GAIN',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'I' THEN 1 ELSE 0 END AS 'Improved', 
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'U' THEN 1 ELSE 0 END AS 'Unchanged',
                CASE WHEN _CS_SCORE_CHANGE_FLAG = 'W' THEN 1 ELSE 0 END AS 'Worsened'
        FROM ##proms_processing_EQ1
        WHERE CFLAG = 1

        DROP TABLE ##proms_processing_EQ1


        -------------------------------------------------------------------------------------------------------------
        ------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E3
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC) - FLOOR(MIN(Q1PCALC)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_INDEX]) - MIN([Q1_EQ5D_INDEX])))+ MIN([Q1_EQ5D_INDEX]) AS DECIMAL (10,3))AS 'Q1 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_INDEX]) AS Q1RANK,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC'	
            FROM #EQ2
            )T WHERE Q1RANK BETWEEN FLOOR(Q1PCALC) AND CEILING(Q1PCALC)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E4
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC25) - FLOOR(MIN(Q1PCALC25)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_INDEX]) - MIN([Q1_EQ5D_INDEX])))+ MIN([Q1_EQ5D_INDEX]) AS DECIMAL (10,3))AS 'Q1 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_INDEX]) AS Q1RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC25'	
            FROM #EQ2
            )T WHERE Q1RANK25 BETWEEN FLOOR(Q1PCALC25) AND CEILING(Q1PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E5
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC50) - FLOOR(MIN(Q1PCALC50)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_INDEX]) - MIN([Q1_EQ5D_INDEX])))+ MIN([Q1_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q1 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_INDEX]) AS Q1RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC50'		
            FROM #EQ2
            )T WHERE Q1RANK50 BETWEEN FLOOR(Q1PCALC50) AND CEILING(Q1PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E6
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC75) - FLOOR(MIN(Q1PCALC75)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_INDEX]) - MIN([Q1_EQ5D_INDEX])))+ MIN([Q1_EQ5D_INDEX]) AS DECIMAL (10,3))AS 'Q1 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_INDEX]) AS Q1RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC75'	
            FROM #EQ2
            )T WHERE Q1RANK75 BETWEEN FLOOR(Q1PCALC75) AND CEILING(Q1PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E7
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC95) - FLOOR(MIN(Q1PCALC95)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_INDEX]) - MIN([Q1_EQ5D_INDEX])))+ MIN([Q1_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q1 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_INDEX]) AS Q1RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC95'
            FROM #EQ2
            )T WHERE Q1RANK95 BETWEEN FLOOR(Q1PCALC95) AND CEILING(Q1PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E8
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC5) - FLOOR(MIN(Q2PCALC5)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_INDEX]) - MIN([Q2_EQ5D_INDEX])))+ MIN([Q2_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q2 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_INDEX]) AS Q2RANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC5'
            FROM #EQ2
            )T WHERE Q2RANK5 BETWEEN FLOOR(Q2PCALC5) AND CEILING(Q2PCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E9
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC25) - FLOOR(MIN(Q2PCALC25)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_INDEX]) - MIN([Q2_EQ5D_INDEX])))+ MIN([Q2_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q2 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_INDEX]) AS Q2RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC25'	
            FROM #EQ2
            )T WHERE Q2RANK25 BETWEEN FLOOR(Q2PCALC25) AND CEILING(Q2PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E10
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC50) - FLOOR(MIN(Q2PCALC50)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_INDEX]) - MIN([Q2_EQ5D_INDEX])))+ MIN([Q2_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q2 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_INDEX]) AS Q2RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC50'	
            FROM #EQ2
            )T WHERE Q2RANK50 BETWEEN FLOOR(Q2PCALC50) AND CEILING(Q2PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E11
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC75) - FLOOR(MIN(Q2PCALC75)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_INDEX]) - MIN([Q2_EQ5D_INDEX])))+ MIN([Q2_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q2 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_INDEX]) AS Q2RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC75'
            FROM #EQ2
            )T WHERE Q2RANK75 BETWEEN FLOOR(Q2PCALC75) AND CEILING(Q2PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E12
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC95) - FLOOR(MIN(Q2PCALC95)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_INDEX]) - MIN([Q2_EQ5D_INDEX])))+ MIN([Q2_EQ5D_INDEX]) AS DECIMAL (10,3)) AS 'Q2 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_INDEX],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_INDEX]) AS Q2RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC95'	
            FROM #EQ2
            )T WHERE Q2RANK95 BETWEEN FLOOR(Q2PCALC95) AND CEILING(Q2PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E13
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC5) - FLOOR(MIN(HGPCALC5)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC5'	
            FROM #EQ2
            )T WHERE HGRANK5 BETWEEN FLOOR(HGPCALC5) AND CEILING(HGPCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E14
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC25) - FLOOR(MIN(HGPCALC25)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC25'	
            FROM #EQ2
            )T WHERE HGRANK25 BETWEEN FLOOR(HGPCALC25) AND CEILING(HGPCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_			
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E15
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC50) - FLOOR(MIN(HGPCALC50)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC50'
            FROM #EQ2
            )T WHERE HGRANK50 BETWEEN FLOOR(HGPCALC50) AND CEILING(HGPCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E16
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC75) - FLOOR(MIN(HGPCALC75)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC75'
            FROM #EQ2
            )T WHERE HGRANK75 BETWEEN FLOOR(HGPCALC75) AND CEILING(HGPCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_			
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E17
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC95) - FLOOR(MIN(HGPCALC95)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC95'	
            FROM #EQ2
            )T WHERE HGRANK95 BETWEEN FLOOR(HGPCALC95) AND CEILING(HGPCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E18
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Q1 Mean],
                t.[Q2 Mean],
                t.[HG Mean]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    CAST(AVG(Q1_EQ5D_INDEX) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'Q1 Mean',
                    CAST(AVG(Q2_EQ5D_INDEX) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'Q2 Mean',
                    CAST(AVG([HealthGain]) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'HG Mean'
                FROM #EQ2
            )t

            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Q1 Mean],
                    t.[Q2 Mean],
                    t.[HG Mean]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E19
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Improved],
                t.[Unchanged],
                t.[Worsened],
                t.[Improved]+t.[Unchanged]+t.[Worsened] AS [Total]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    SUM(CAST([Improved] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Improved',
                    SUM(CAST([Unchanged] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Unchanged',
                    SUM(CAST([Worsened] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Worsened'
                FROM #EQ2
            )t
            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Improved],
                    t.[Unchanged],
                    t.[Worsened]
        )_
        -------------------------------------------------------------------------------------------------------------

        SELECT * INTO #EQ20
        FROM
        (
            SELECT 
                    a.[Dimension],
                    a.[Value],
                    a.[Procedure],
                    a.[Measure],
                    p.[Q1 Mean],
                    a.[Q1 5%],
                    b.[Q1 1st Quartile],
                    c.[Q1 Median],
                    d.[Q1 3rd Quartile],
                    e.[Q1 95%],
                    p.[Q2 Mean],
                    f.[Q2 5%],
                    g.[Q2 1st Quartile],
                    h.[Q2 Median],
                    i.[Q2 3rd Quartile],
                    j.[Q2 95%],
                    p.[HG Mean],
                    k.[HG 5%],
                    l.[HG 1st Quartile],
                    m.[HG Median],
                    n.[HG 3rd Quartile],
                    o.[HG 95%],
                    q.[Improved],
                    q.[Unchanged],
                    q.[Worsened],
                    q.[Total]

            FROM #E3 a 
            LEFT JOIN #E4 b 
            ON a.[Dimension]  = b.[Dimension]
            AND a.[Value]     = b.[Value]
            AND a.[Procedure] = b.[Procedure]
            AND a.[Measure]   = b.[Measure]
            
            LEFT JOIN #E5 c
            ON a.[Dimension]  = c.[Dimension]
            AND a.[Value]     = c.[Value]
            AND a.[Procedure] = c.[Procedure]
            AND a.[Measure]   = c.[Measure]
            
            LEFT JOIN #E6 d
            ON a.[Dimension]  = d.[Dimension]
            AND a.[Value]     = d.[Value]
            AND a.[Procedure] = d.[Procedure]
            AND a.[Measure]   = d.[Measure]
            
            LEFT JOIN #E7 e
            ON a.[Dimension]  = e.[Dimension]
            AND a.[Value]     = e.[Value]
            AND a.[Procedure] = e.[Procedure]
            AND a.[Measure]   = e.[Measure]
            
            LEFT JOIN #E8 f
            ON a.[Dimension]  = f.[Dimension]
            AND a.[Value]     = f.[Value]
            AND a.[Procedure] = f.[Procedure]
            AND a.[Measure]   = f.[Measure]
            
            LEFT JOIN #E9 g
            ON a.[Dimension]  = g.[Dimension]
            AND a.[Value]     = g.[Value]
            AND a.[Procedure] = g.[Procedure]
            AND a.[Measure]   = g.[Measure]
            
            LEFT JOIN #E10 h
            ON a.[Dimension]  = h.[Dimension]
            AND a.[Value]     = h.[Value]
            AND a.[Procedure] = h.[Procedure]
            AND a.[Measure]   = h.[Measure]
            
            LEFT JOIN #E11 i
            ON a.[Dimension]  = i.[Dimension]
            AND a.[Value]     = i.[Value]
            AND a.[Procedure] = i.[Procedure]
            AND a.[Measure]   = i.[Measure]
            
            LEFT JOIN #E12 j
            ON a.[Dimension]  = j.[Dimension]
            AND a.[Value]     = j.[Value]
            AND a.[Procedure] = j.[Procedure]
            AND a.[Measure]   = j.[Measure]
            
            LEFT JOIN #E13 k
            ON a.[Dimension]  = k.[Dimension]
            AND a.[Value]     = k.[Value]
            AND a.[Procedure] = k.[Procedure]
            AND a.[Measure]   = k.[Measure]
            
            LEFT JOIN #E14 l
            ON a.[Dimension]  = l.[Dimension]
            AND a.[Value]     = l.[Value]
            AND a.[Procedure] = l.[Procedure]
            AND a.[Measure]   = l.[Measure]
            
            LEFT JOIN #E15 m
            ON a.[Dimension]  = m.[Dimension]
            AND a.[Value]     = m.[Value]
            AND a.[Procedure] = m.[Procedure]
            AND a.[Measure]   = m.[Measure]
            
            LEFT JOIN #E16 n
            ON a.[Dimension]  = n.[Dimension]
            AND a.[Value]     = n.[Value]
            AND a.[Procedure] = n.[Procedure]
            AND a.[Measure]   = n.[Measure]
            
            LEFT JOIN #E17 o
            ON a.[Dimension]  = o.[Dimension]
            AND a.[Value]     = o.[Value]
            AND a.[Procedure] = o.[Procedure]
            AND a.[Measure]   = o.[Measure]
            
            LEFT JOIN #E18 p
            ON a.[Dimension]  = p.[Dimension]
            AND a.[Value]     = p.[Value]
            AND a.[Procedure] = p.[Procedure]
            AND a.[Measure]   = p.[Measure]
            
            LEFT JOIN #E19 q
            ON a.[Dimension]  = q.[Dimension]
            AND a.[Value]     = q.[Value]
            AND a.[Procedure] = q.[Procedure]
            AND a.[Measure]   = q.[Measure]
            
        )_

        DROP TABLE #EQ2
        DROP TABLE #E3
        DROP TABLE #E4
        DROP TABLE #E5
        DROP TABLE #E6
        DROP TABLE #E7
        DROP TABLE #E8
        DROP TABLE #E9
        DROP TABLE #E10
        DROP TABLE #E11
        DROP TABLE #E12
        DROP TABLE #E13
        DROP TABLE #E14
        DROP TABLE #E15
        DROP TABLE #E16
        DROP TABLE #E17
        DROP TABLE #E18
        DROP TABLE #E19

        -------------------------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------------------------

        SELECT * INTO #E103
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC) - FLOOR(MIN(Q1PCALC)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_HEALTH_SCALE]) - MIN([Q1_EQ5D_HEALTH_SCALE])))+ MIN([Q1_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3)) AS 'Q1 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_HEALTH_SCALE]) AS Q1RANK,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC'	
            FROM #EQ3
            )T WHERE Q1RANK BETWEEN FLOOR(Q1PCALC) AND CEILING(Q1PCALC)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E104
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC25) - FLOOR(MIN(Q1PCALC25)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_HEALTH_SCALE]) - MIN([Q1_EQ5D_HEALTH_SCALE])))+ MIN([Q1_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q1 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_HEALTH_SCALE]) AS Q1RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC25'
            FROM #EQ3
            )T WHERE Q1RANK25 BETWEEN FLOOR(Q1PCALC25) AND CEILING(Q1PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ------------------------------------------------------------------------------------------------------------

        SELECT * INTO #E105
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC50) - FLOOR(MIN(Q1PCALC50)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_HEALTH_SCALE]) - MIN([Q1_EQ5D_HEALTH_SCALE])))+ MIN([Q1_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q1 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_HEALTH_SCALE]) AS Q1RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC50'	
            FROM #EQ3
            )T WHERE Q1RANK50 BETWEEN FLOOR(Q1PCALC50) AND CEILING(Q1PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------

        SELECT * INTO #E106
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC75) - FLOOR(MIN(Q1PCALC75)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_HEALTH_SCALE]) - MIN([Q1_EQ5D_HEALTH_SCALE])))+ MIN([Q1_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q1 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_HEALTH_SCALE]) AS Q1RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC75'
            FROM #EQ3
            )T WHERE Q1RANK75 BETWEEN FLOOR(Q1PCALC75) AND CEILING(Q1PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E107
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC95) - FLOOR(MIN(Q1PCALC95)) AS FLOAT) * 
                    (MAX([Q1_EQ5D_HEALTH_SCALE]) - MIN([Q1_EQ5D_HEALTH_SCALE])))+ MIN([Q1_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q1 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_EQ5D_HEALTH_SCALE]) AS Q1RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC95'
            FROM #EQ3
            )T WHERE Q1RANK95 BETWEEN FLOOR(Q1PCALC95) AND CEILING(Q1PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E108
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC5) - FLOOR(MIN(Q2PCALC5)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_HEALTH_SCALE]) - MIN([Q2_EQ5D_HEALTH_SCALE])))+ MIN([Q2_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q2 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_HEALTH_SCALE]) AS Q2RANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC5'
            FROM #EQ3
            )T WHERE Q2RANK5 BETWEEN FLOOR(Q2PCALC5) AND CEILING(Q2PCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E109
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC25) - FLOOR(MIN(Q2PCALC25)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_HEALTH_SCALE]) - MIN([Q2_EQ5D_HEALTH_SCALE])))+ MIN([Q2_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q2 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_HEALTH_SCALE]) AS Q2RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC25'
            FROM #EQ3
            )T WHERE Q2RANK25 BETWEEN FLOOR(Q2PCALC25) AND CEILING(Q2PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1010
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC50) - FLOOR(MIN(Q2PCALC50)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_HEALTH_SCALE]) - MIN([Q2_EQ5D_HEALTH_SCALE])))+ MIN([Q2_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q2 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_HEALTH_SCALE]) AS Q2RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC50'	
            FROM #EQ3
            )T WHERE Q2RANK50 BETWEEN FLOOR(Q2PCALC50) AND CEILING(Q2PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1011
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC75) - FLOOR(MIN(Q2PCALC75)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_HEALTH_SCALE]) - MIN([Q2_EQ5D_HEALTH_SCALE])))+ MIN([Q2_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q2 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_HEALTH_SCALE]) AS Q2RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC75'
            FROM #EQ3
            )T WHERE Q2RANK75 BETWEEN FLOOR(Q2PCALC75) AND CEILING(Q2PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1012
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC95) - FLOOR(MIN(Q2PCALC95)) AS FLOAT) * 
                    (MAX([Q2_EQ5D_HEALTH_SCALE]) - MIN([Q2_EQ5D_HEALTH_SCALE])))+ MIN([Q2_EQ5D_HEALTH_SCALE]) AS DECIMAL (10,3))AS 'Q2 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_EQ5D_HEALTH_SCALE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_EQ5D_HEALTH_SCALE]) AS Q2RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC95'
            FROM #EQ3
            )T WHERE Q2RANK95 BETWEEN FLOOR(Q2PCALC95) AND CEILING(Q2PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1013
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC5) - FLOOR(MIN(HGPCALC5)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3))AS 'HG 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC5'
            FROM #EQ3
            )T WHERE HGRANK5 BETWEEN FLOOR(HGPCALC5) AND CEILING(HGPCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1014
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC25) - FLOOR(MIN(HGPCALC25)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3))AS 'HG 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC25'
            FROM #EQ3
            )T WHERE HGRANK25 BETWEEN FLOOR(HGPCALC25) AND CEILING(HGPCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_			
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1015
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC50) - FLOOR(MIN(HGPCALC50)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3))AS 'HG Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC50'
            FROM #EQ3
            )T WHERE HGRANK50 BETWEEN FLOOR(HGPCALC50) AND CEILING(HGPCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1016
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC75) - FLOOR(MIN(HGPCALC75)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3))AS 'HG 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC75'	
            FROM #EQ3
            )T WHERE HGRANK75 BETWEEN FLOOR(HGPCALC75) AND CEILING(HGPCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1017
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC95) - FLOOR(MIN(HGPCALC95)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3))AS 'HG 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC95'	
            FROM #EQ3
            )T WHERE HGRANK95 BETWEEN FLOOR(HGPCALC95) AND CEILING(HGPCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1018
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Q1 Mean],
                t.[Q2 Mean],
                t.[HG Mean]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    CAST(AVG(Q1_EQ5D_HEALTH_SCALE) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'Q1 Mean',
                    CAST(AVG(Q2_EQ5D_HEALTH_SCALE) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'Q2 Mean',
                    CAST(AVG([HealthGain]) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT) AS 'HG Mean'
                FROM #EQ3
            )t

            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Q1 Mean],
                    t.[Q2 Mean],
                    t.[HG Mean]
        )_
        ------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1019
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Improved],
                t.[Unchanged],
                t.[Worsened],
                t.[Improved]+t.[Unchanged]+t.[Worsened] AS [Total]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    SUM(CAST([Improved] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Improved',
                    SUM(CAST([Unchanged] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Unchanged',
                    SUM(CAST([Worsened] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Worsened'
                FROM #EQ3
            )t
            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Improved],
                    t.[Unchanged],
                    t.[Worsened]
        )_
        -------------------------------------------------------------------------------------------------------------------------------
        INSERT INTO #EQ20

        SELECT 
                a.[Dimension],
                a.[Value],
                a.[Procedure],
                a.[Measure],
                p.[Q1 Mean],
                a.[Q1 5%],
                b.[Q1 1st Quartile],
                c.[Q1 Median],
                d.[Q1 3rd Quartile],
                e.[Q1 95%],
                p.[Q2 Mean],
                f.[Q2 5%],
                g.[Q2 1st Quartile],
                h.[Q2 Median],
                i.[Q2 3rd Quartile],
                j.[Q2 95%],
                p.[HG Mean],
                k.[HG 5%],
                l.[HG 1st Quartile],
                m.[HG Median],
                n.[HG 3rd Quartile],
                o.[HG 95%],
                q.[Improved],
                q.[Unchanged],
                q.[Worsened],
                q.[Total]

        FROM #E103 a 
        LEFT JOIN #E104 b 
        ON a.[Dimension]  = b.[Dimension]
        AND a.[Value]     = b.[Value]
        AND a.[Procedure] = b.[Procedure]
        AND a.[Measure]   = b.[Measure]
            
        LEFT JOIN #E105 c
        ON a.[Dimension]  = c.[Dimension]
        AND a.[Value]     = c.[Value]
        AND a.[Procedure] = c.[Procedure]
        AND a.[Measure]   = c.[Measure]

        LEFT JOIN #E106 d
        ON a.[Dimension]  = d.[Dimension]
        AND a.[Value]     = d.[Value]
        AND a.[Procedure] = d.[Procedure]
        AND a.[Measure]   = d.[Measure]

        LEFT JOIN #E107 e
        ON a.[Dimension]  = e.[Dimension]
        AND a.[Value]     = e.[Value]
        AND a.[Procedure] = e.[Procedure]
        AND a.[Measure]   = e.[Measure]

        LEFT JOIN #E108 f
        ON a.[Dimension]  = f.[Dimension]
        AND a.[Value]     = f.[Value]
        AND a.[Procedure] = f.[Procedure]
        AND a.[Measure]   = f.[Measure]

        LEFT JOIN #E109 g
        ON a.[Dimension]  = g.[Dimension]
        AND a.[Value]     = g.[Value]
        AND a.[Procedure] = g.[Procedure]
        AND a.[Measure]   = g.[Measure]

        LEFT JOIN #E1010 h
        ON a.[Dimension]  = h.[Dimension]
        AND a.[Value]     = h.[Value]
        AND a.[Procedure] = h.[Procedure]
        AND a.[Measure]   = h.[Measure]

        LEFT JOIN #E1011 i
        ON a.[Dimension]  = i.[Dimension]
        AND a.[Value]     = i.[Value]
        AND a.[Procedure] = i.[Procedure]
        AND a.[Measure]   = i.[Measure]

        LEFT JOIN #E1012 j
        ON a.[Dimension]  = j.[Dimension]
        AND a.[Value]     = j.[Value]
        AND a.[Procedure] = j.[Procedure]
        AND a.[Measure]   = j.[Measure]

        LEFT JOIN #E1013 k
        ON a.[Dimension]  = k.[Dimension]
        AND a.[Value]     = k.[Value]
        AND a.[Procedure] = k.[Procedure]
        AND a.[Measure]   = k.[Measure]

        LEFT JOIN #E1014 l
        ON a.[Dimension]  = l.[Dimension]
        AND a.[Value]     = l.[Value]
        AND a.[Procedure] = l.[Procedure]
        AND a.[Measure]   = l.[Measure]

        LEFT JOIN #E1015 m
        ON a.[Dimension]  = m.[Dimension]
        AND a.[Value]     = m.[Value]
        AND a.[Procedure] = m.[Procedure]
        AND a.[Measure]   = m.[Measure]

        LEFT JOIN #E1016 n
        ON a.[Dimension]  = n.[Dimension]
        AND a.[Value]     = n.[Value]
        AND a.[Procedure] = n.[Procedure]
        AND a.[Measure]   = n.[Measure]

        LEFT JOIN #E1017 o
        ON a.[Dimension]  = o.[Dimension]
        AND a.[Value]     = o.[Value]
        AND a.[Procedure] = o.[Procedure]
        AND a.[Measure]   = o.[Measure]

        LEFT JOIN #E1018 p
        ON a.[Dimension]  = p.[Dimension]
        AND a.[Value]     = p.[Value]
        AND a.[Procedure] = p.[Procedure]
        AND a.[Measure]   = p.[Measure]

        LEFT JOIN #E1019 q
        ON a.[Dimension]  = q.[Dimension]
        AND a.[Value]     = q.[Value]
        AND a.[Procedure] = q.[Procedure]
        AND a.[Measure]   = q.[Measure]


        DROP TABLE #EQ3
        DROP TABLE #E103
        DROP TABLE #E104
        DROP TABLE #E105
        DROP TABLE #E106
        DROP TABLE #E107
        DROP TABLE #E108
        DROP TABLE #E109
        DROP TABLE #E1010
        DROP TABLE #E1011
        DROP TABLE #E1012
        DROP TABLE #E1013
        DROP TABLE #E1014
        DROP TABLE #E1015
        DROP TABLE #E1016
        DROP TABLE #E1017
        DROP TABLE #E1018
        DROP TABLE #E1019

        -----------------------------------------------------------------------------------------------------------------------------------
        -----------------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E113
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC) - FLOOR(MIN(Q1PCALC)) AS FLOAT) * 
                    (MAX([Q1_CS_SCORE]) - MIN([Q1_CS_SCORE])))+ MIN([Q1_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q1 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_CS_SCORE]) AS Q1RANK,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC'
            FROM #EQ4
            )T WHERE Q1RANK BETWEEN FLOOR(Q1PCALC) AND CEILING(Q1PCALC)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -----------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E114
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC25) - FLOOR(MIN(Q1PCALC25)) AS FLOAT) * 
                    (MAX([Q1_CS_SCORE]) - MIN([Q1_CS_SCORE])))+ MIN([Q1_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q1 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_CS_SCORE]) AS Q1RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC25'
            FROM #EQ4
            )T WHERE Q1RANK25 BETWEEN FLOOR(Q1PCALC25) AND CEILING(Q1PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E115
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC50) - FLOOR(MIN(Q1PCALC50)) AS FLOAT) * 
                    (MAX([Q1_CS_SCORE]) - MIN([Q1_CS_SCORE])))+ MIN([Q1_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q1 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_CS_SCORE]) AS Q1RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC50'
            FROM #EQ4
            )T WHERE Q1RANK50 BETWEEN FLOOR(Q1PCALC50) AND CEILING(Q1PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------
        SELECT * INTO #E116
        FROM 
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC75) - FLOOR(MIN(Q1PCALC75)) AS FLOAT) * 
                    (MAX([Q1_CS_SCORE]) - MIN([Q1_CS_SCORE])))+ MIN([Q1_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q1 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_CS_SCORE]) AS Q1RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC75'
            FROM #EQ4
            )T WHERE Q1RANK75 BETWEEN FLOOR(Q1PCALC75) AND CEILING(Q1PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E117
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q1PCALC95) - FLOOR(MIN(Q1PCALC95)) AS FLOAT) * 
                    (MAX([Q1_CS_SCORE]) - MIN([Q1_CS_SCORE])))+ MIN([Q1_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q1 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q1_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q1_CS_SCORE]) AS Q1RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q1PCALC95'
            FROM #EQ4
            )T WHERE Q1RANK95 BETWEEN FLOOR(Q1PCALC95) AND CEILING(Q1PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E118
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC5) - FLOOR(MIN(Q2PCALC5)) AS FLOAT) * 
                    (MAX([Q2_CS_SCORE]) - MIN([Q2_CS_SCORE])))+ MIN([Q2_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q2 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_CS_SCORE]) AS Q2RANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC5'
            FROM #EQ4
            )T WHERE Q2RANK5 BETWEEN FLOOR(Q2PCALC5) AND CEILING(Q2PCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E119
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC25) - FLOOR(MIN(Q2PCALC25)) AS FLOAT) * 
                    (MAX([Q2_CS_SCORE]) - MIN([Q2_CS_SCORE])))+ MIN([Q2_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q2 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_CS_SCORE]) AS Q2RANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC25'
            FROM #EQ4
            )T WHERE Q2RANK25 BETWEEN FLOOR(Q2PCALC25) AND CEILING(Q2PCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1110
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC50) - FLOOR(MIN(Q2PCALC50)) AS FLOAT) * 
                    (MAX([Q2_CS_SCORE]) - MIN([Q2_CS_SCORE])))+ MIN([Q2_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q2 Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_CS_SCORE]) AS Q2RANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC50'
            FROM #EQ4
            )T WHERE Q2RANK50 BETWEEN FLOOR(Q2PCALC50) AND CEILING(Q2PCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1111
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC75) - FLOOR(MIN(Q2PCALC75)) AS FLOAT) * 
                    (MAX([Q2_CS_SCORE]) - MIN([Q2_CS_SCORE])))+ MIN([Q2_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q2 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_CS_SCORE]) AS Q2RANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC75'
            FROM #EQ4
            )T WHERE Q2RANK75 BETWEEN FLOOR(Q2PCALC75) AND CEILING(Q2PCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1112
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(Q2PCALC95) - FLOOR(MIN(Q2PCALC95)) AS FLOAT) * 
                    (MAX([Q2_CS_SCORE]) - MIN([Q2_CS_SCORE])))+ MIN([Q2_CS_SCORE]) AS DECIMAL (10,3)) AS 'Q2 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [Q2_CS_SCORE],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [Q2_CS_SCORE]) AS Q2RANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'Q2PCALC95'
            FROM #EQ4
            )T WHERE Q2RANK95 BETWEEN FLOOR(Q2PCALC95) AND CEILING(Q2PCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1113
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC5) - FLOOR(MIN(HGPCALC5)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 5%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK5,
                0.05 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC5'
            FROM #EQ4
            )T WHERE HGRANK5 BETWEEN FLOOR(HGPCALC5) AND CEILING(HGPCALC5)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1114
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC25) - FLOOR(MIN(HGPCALC25))AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 1st Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK25,
                0.25 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC25'
            FROM #EQ4
            )T WHERE HGRANK25 BETWEEN FLOOR(HGPCALC25) AND CEILING(HGPCALC25)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1115
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC50) - FLOOR(MIN(HGPCALC50)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG Median'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK50,
                0.50 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC50'
            FROM #EQ4
            )T WHERE HGRANK50 BETWEEN FLOOR(HGPCALC50) AND CEILING(HGPCALC50)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1116
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC75) - FLOOR(MIN(HGPCALC75)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 3rd Quartile'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK75,
                0.75 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC75'
            FROM #EQ4
            )T WHERE HGRANK75 BETWEEN FLOOR(HGPCALC75) AND CEILING(HGPCALC75)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        ---------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1117
        FROM
        (	
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST((CAST(MIN(HGPCALC95) - FLOOR(MIN(HGPCALC95)) AS FLOAT) * 
                    (MAX([HealthGain]) - MIN([HealthGain])))+ MIN([HealthGain]) AS DECIMAL (10,3)) AS 'HG 95%'
            FROM
            (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                [HealthGain],
                ROW_NUMBER()OVER (PARTITION BY [Procedure],[Dimension],[Value] ORDER BY [HealthGain]) AS HGRANK95,
                0.95 * (COUNT(*) OVER (PARTITION BY [Procedure],[Dimension],[Value]) - 1) + 1  AS 'HGPCALC95'
            FROM #EQ4
            )T WHERE HGRANK95 BETWEEN FLOOR(HGPCALC95) AND CEILING(HGPCALC95)
            
            GROUP BY
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure]
        )_
        -----------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1118
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Q1 Mean],
                t.[Q2 Mean],
                t.[HG Mean]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    CAST(AVG(Q1_CS_SCORE) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT)  AS 'Q1 Mean',
                    CAST(AVG(Q2_CS_SCORE) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT)  AS 'Q2 Mean',
                    CAST(AVG([HealthGain]) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS FLOAT)  AS 'HG Mean'
                FROM #EQ4
            )t

            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Q1 Mean],
                    t.[Q2 Mean],
                    t.[HG Mean]
        )_
        -----------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #E1119
        FROM
        (
            SELECT
                t.[Dimension],
                t.[Value],
                t.[Procedure],
                t.[Measure],
                t.[Improved],
                t.[Unchanged],
                t.[Worsened],
                t.[Improved]+t.[Unchanged]+t.[Worsened] AS [Total]
            FROM(
                SELECT
                    [Dimension],
                    [Value],
                    [Procedure],
                    [Measure],
                    SUM(CAST([Improved] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Improved',
                    SUM(CAST([Unchanged] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Unchanged',
                    SUM(CAST([Worsened] AS DECIMAL (10,1))) OVER (PARTITION BY [Procedure],[Dimension],[Value]) AS 'Worsened'
                FROM #EQ4
            )t
            GROUP BY
                    t.[Dimension],
                    t.[Value],
                    t.[Procedure],
                    t.[Measure],
                    t.[Improved],
                    t.[Unchanged],
                    t.[Worsened]
        )_
        -----------------------------------------------------------------------------------------------------------------------------
        INSERT INTO #EQ20

            SELECT 
                    a.[Dimension],
                    a.[Value],
                    a.[Procedure],
                    a.[Measure],
                    p.[Q1 Mean],
                    a.[Q1 5%],
                    b.[Q1 1st Quartile],
                    c.[Q1 Median],
                    d.[Q1 3rd Quartile],
                    e.[Q1 95%],
                    p.[Q2 Mean],
                    f.[Q2 5%],
                    g.[Q2 1st Quartile],
                    h.[Q2 Median],
                    i.[Q2 3rd Quartile],
                    j.[Q2 95%],
                    p.[HG Mean],
                    k.[HG 5%],
                    l.[HG 1st Quartile],
                    m.[HG Median],
                    n.[HG 3rd Quartile],
                    o.[HG 95%],
                    q.[Improved],
                    q.[Unchanged],
                    q.[Worsened],
                    q.[Total]

            FROM #E113 a 
            LEFT JOIN #E114 b 
            ON a.[Dimension]  = b.[Dimension]
            AND a.[Value]     = b.[Value]
            AND a.[Procedure] = b.[Procedure]
            AND a.[Measure]   = b.[Measure]
            
            LEFT JOIN #E115 c
            ON a.[Dimension]  = c.[Dimension]
            AND a.[Value]     = c.[Value]
            AND a.[Procedure] = c.[Procedure]
            AND a.[Measure]   = c.[Measure]
            
            LEFT JOIN #E116 d
            ON a.[Dimension]  = d.[Dimension]
            AND a.[Value]     = d.[Value]
            AND a.[Procedure] = d.[Procedure]
            AND a.[Measure]   = d.[Measure]
            
            LEFT JOIN #E117 e
            ON a.[Dimension]  = e.[Dimension]
            AND a.[Value]     = e.[Value]
            AND a.[Procedure] = e.[Procedure]
            AND a.[Measure]   = e.[Measure]
            
            LEFT JOIN #E118 f
            ON a.[Dimension]  = f.[Dimension]
            AND a.[Value]     = f.[Value]
            AND a.[Procedure] = f.[Procedure]
            AND a.[Measure]   = f.[Measure]
            
            LEFT JOIN #E119 g
            ON a.[Dimension]  = g.[Dimension]
            AND a.[Value]     = g.[Value]
            AND a.[Procedure] = g.[Procedure]
            AND a.[Measure]   = g.[Measure]
            
            LEFT JOIN #E1110 h
            ON a.[Dimension]  = h.[Dimension]
            AND a.[Value]     = h.[Value]
            AND a.[Procedure] = h.[Procedure]
            AND a.[Measure]   = h.[Measure]
            
            LEFT JOIN #E1111 i
            ON a.[Dimension]  = i.[Dimension]
            AND a.[Value]     = i.[Value]
            AND a.[Procedure] = i.[Procedure]
            AND a.[Measure]   = i.[Measure]
            
            LEFT JOIN #E1112 j
            ON a.[Dimension]  = j.[Dimension]
            AND a.[Value]     = j.[Value]
            AND a.[Procedure] = j.[Procedure]
            AND a.[Measure]   = j.[Measure]
            
            LEFT JOIN #E1113 k
            ON a.[Dimension]  = k.[Dimension]
            AND a.[Value]     = k.[Value]
            AND a.[Procedure] = k.[Procedure]
            AND a.[Measure]   = k.[Measure]
            
            LEFT JOIN #E1114 l
            ON a.[Dimension]  = l.[Dimension]
            AND a.[Value]     = l.[Value]
            AND a.[Procedure] = l.[Procedure]
            AND a.[Measure]   = l.[Measure]
            
            LEFT JOIN #E1115 m
            ON a.[Dimension]  = m.[Dimension]
            AND a.[Value]     = m.[Value]
            AND a.[Procedure] = m.[Procedure]
            AND a.[Measure]   = m.[Measure]
            
            LEFT JOIN #E1116 n
            ON a.[Dimension]  = n.[Dimension]
            AND a.[Value]     = n.[Value]
            AND a.[Procedure] = n.[Procedure]
            AND a.[Measure]   = n.[Measure]
            
            LEFT JOIN #E1117 o
            ON a.[Dimension]  = o.[Dimension]
            AND a.[Value]     = o.[Value]
            AND a.[Procedure] = o.[Procedure]
            AND a.[Measure]   = o.[Measure]
            
            LEFT JOIN #E1118 p
            ON a.[Dimension]  = p.[Dimension]
            AND a.[Value]     = p.[Value]
            AND a.[Procedure] = p.[Procedure]
            AND a.[Measure]   = p.[Measure]
            
            LEFT JOIN #E1119 q
            ON a.[Dimension]  = q.[Dimension]
            AND a.[Value]     = q.[Value]
            AND a.[Procedure] = q.[Procedure]
            AND a.[Measure]   = q.[Measure]
            

        DROP TABLE #EQ4
        DROP TABLE #E113
        DROP TABLE #E114
        DROP TABLE #E115
        DROP TABLE #E116
        DROP TABLE #E117
        DROP TABLE #E118
        DROP TABLE #E119
        DROP TABLE #E1110
        DROP TABLE #E1111
        DROP TABLE #E1112
        DROP TABLE #E1113
        DROP TABLE #E1114
        DROP TABLE #E1115
        DROP TABLE #E1116
        DROP TABLE #E1117
        DROP TABLE #E1118
        DROP TABLE #E1119

        --------------------------------------------------------------------------------------------------
        --------------------------------------------------------------------------------------------------

        SELECT * INTO #EQ1213
        FROM
        (
            SELECT
                z.[Dimension],
                z.[Value],
                z.[Procedure],
                z.[Measure],
                x.[Q1 Mean],
                x.[Q1 5%],
                x.[Q1 1st Quartile],
                x.[Q1 Median],
                x.[Q1 3rd Quartile],
                x.[Q1 95%],
                x.[Q2 Mean],
                x.[Q2 5%],
                x.[Q2 1st Quartile],
                x.[Q2 Median],
                x.[Q2 3rd Quartile],
                x.[Q2 95%],
                x.[HG Mean],
                x.[HG 5%],
                x.[HG 1st Quartile],
                x.[HG Median],
                x.[HG 3rd Quartile],
                x.[HG 95%],
                x.[Improved],
                x.[Unchanged],
                x.[Worsened],
                x.[Total]

            FROM proms.REF_EQUALITY z
            LEFT JOIN #EQ20 x
            ON z.[Dimension] = x.[Dimension]
            AND z.[Value] = x.[Value]
            AND z.[Procedure] = x.[Procedure]
            AND z.[Measure] = x.[Measure]	  
            WHERE Inactive IS NULL 
            OR @FYEAR = CASE WHEN RIGHT(Inactive,5)='03-31'
                            THEN LEFT(Inactive,4) - 1
                            ELSE LEFT(Inactive,4)
                        END
            
        )_

        DROP TABLE #EQ20

        SELECT * INTO #TEMP1
        FROM
        (
            SELECT
                [Dimension],
                [Value],
                [Procedure],
                [Measure],
                CAST([Q1 Mean] AS DECIMAL (10,3)) AS [Pre-Op Q Mean],
                CAST([Q1 5%] AS DECIMAL (10,3)) AS [Pre-Op Q 5%],
                CAST([Q1 1st Quartile] AS DECIMAL (10,3)) AS [Pre-Op Q 1st Quartile],
                CAST([Q1 Median] AS DECIMAL (10,3)) AS [Pre-Op Q Median],
                CAST([Q1 3rd Quartile] AS DECIMAL (10,3)) AS [Pre-Op Q 3rd Quartile],
                CAST([Q1 95%] AS DECIMAL (10,3)) AS [Pre-Op Q 95%],
                CAST([Q2 Mean] AS DECIMAL (10,3)) AS [Post-Op Q Mean],
                CAST([Q2 5%] AS DECIMAL (10,3)) AS [Post-Op Q 5%],
                CAST([Q2 1st Quartile] AS DECIMAL (10,3)) AS [Post-Op Q 1st Quartile],
                CAST([Q2 Median] AS DECIMAL (10,3)) AS [Post-Op Q Median],
                CAST([Q2 3rd Quartile] AS DECIMAL (10,3)) AS [Post-Op Q 3rd Quartile],
                CAST([Q2 95%] AS DECIMAL (10,3)) AS [Post-Op Q 95%],
                CAST([HG Mean] AS DECIMAL (10,3)) AS [Heath Gain Mean],
                CAST([HG 5%] AS DECIMAL (10,3)) AS [Heath Gain 5%],
                CAST([HG 1st Quartile] AS DECIMAL (10,3)) AS [Heath Gain 1st Quartile],
                CAST([HG Median] AS DECIMAL (10,3)) AS [Heath Gain Median],
                CAST([HG 3rd Quartile] AS DECIMAL (10,3)) AS [Heath Gain 3rd Quartile],
                CAST([HG 95%] AS DECIMAL (10,3)) AS [Heath Gain 95%],
                [Improved],
                [Unchanged],
                [Worsened],
                [Total]
            FROM #EQ1213
        )_

        DROP TABLE #EQ1213

        SELECT 
            [Dimension],
            [Value],
            [Procedure],
            [Measure],
            ISNULL(CAST([Pre-Op Q Mean] AS varchar (20)),'') AS [Pre-Op Q Mean],
            ISNULL(CAST([Pre-Op Q 5%] AS varchar (20)),'') AS [Pre-Op Q 5%],
            ISNULL(CAST([Pre-Op Q 1st Quartile] AS varchar (20)),'') AS [Pre-Op Q 1st Quartile],
            ISNULL(CAST([Pre-Op Q Median] AS varchar (20)),'') AS [Pre-Op Q Median],
            ISNULL(CAST([Pre-Op Q 3rd Quartile] AS varchar (20)),'') AS [Pre-Op Q 3rd Quartile],
            ISNULL(CAST([Pre-Op Q 95%] AS varchar (20)),'') AS [Pre-Op Q 95%],
            ISNULL(CAST([Post-Op Q Mean] AS varchar (20)),'') AS [Post-Op Q Mean],
            ISNULL(CAST([Post-Op Q 5%] AS varchar (20)),'') AS [Post-Op Q 5%],
            ISNULL(CAST([Post-Op Q 1st Quartile] AS varchar (20)),'') AS [Post-Op Q 1st Quartile],
            ISNULL(CAST([Post-Op Q Median] AS varchar (20)),'') AS [Post-Op Q Median],
            ISNULL(CAST([Post-Op Q 3rd Quartile]  AS varchar (20)),'') AS [Post-Op Q 3rd Quartile],
            ISNULL(CAST([Post-Op Q 95%] AS varchar (20)),'') AS [Post-Op Q 95%],
            ISNULL(CAST([Heath Gain Mean] AS varchar (20)),'') AS [Heath Gain Mean],
            ISNULL(CAST([Heath Gain 5%] AS varchar (20)),'') AS [Heath Gain 5%],
            ISNULL(CAST([Heath Gain 1st Quartile] AS varchar (20)),'') AS [Heath Gain 1st Quartile],
            ISNULL(CAST([Heath Gain Median] AS varchar (20)),'') AS [Heath Gain Median],
            ISNULL(CAST([Heath Gain 3rd Quartile] AS varchar (20)),'') AS [Heath Gain 3rd Quartile],
            ISNULL(CAST([Heath Gain 95%] AS varchar (20)),'') AS [Heath Gain 95%],
            ISNULL(CAST([Improved]AS varchar (20)),'') AS [Improved],
            ISNULL(CAST([Unchanged] AS varchar (20)),'') AS [Unchanged],
            ISNULL(CAST([Worsened] AS varchar (20)),'') AS [Worsened],
            ISNULL(CAST([Total] AS varchar (20)),'') AS [Total]

        FROM #TEMP1
        WHERE [Procedure] IN ('Hip Replacement','Knee Replacement')
        ORDER BY 
            CASE WHEN [Dimension] = 'England' THEN 1
                WHEN [Dimension] = 'Age' THEN 2
                WHEN [Dimension] = 'Age and Gender' THEN 3
                WHEN [Dimension] = 'Disability' THEN 4
                WHEN [Dimension] = 'Ethnicity' THEN 5
                WHEN [Dimension] = 'Gender' THEN 6
                WHEN [Dimension] = 'Index of Multiple Deprivation' THEN 7
            END,
            [Value],
            [Procedure],
            [Measure]

        DROP TABLE #TEMP1

    '''
    return equality_str

