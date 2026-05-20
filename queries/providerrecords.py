def hr_prov_records(startfyear,table):
    yearmonth=f'{int(startfyear)+1}-03'
    hr_prov_records_str = f'''
        DECLARE @FYEAR  VARCHAR (4);
        DECLARE @END  VARCHAR (10);
        DECLARE @table VARCHAR (15);
        DECLARE @sql NVARCHAR(MAX);

        ----------------------- Update these variables as required --------------------------

        SET @FYEAR = '{startfyear}'		    -- represents a financial year, the year selected is the first year of the period e.g. 2012-13 is @FYEAR 2012
        SET @END = '{yearmonth}'		-- year and month of the last month for this dateset
        SET @table = '{table}'	-- processing run with X suffix
        -------------------------------------------------------------------------------------
        SET NOCOUNT ON
        
        SET @sql =
        '
        SELECT * INTO ##proms_processing_TEMP1
        FROM
        (
        SELECT
                P._P_PROCODE AS ProviderCode,
                RP.Description AS PromsProcGroup,
                P.PROC_REVISION_FLAG,
                \'\'\'+@FYEAR+'/'+RIGHT(+@FYEAR+1,2)+\'\'\' AS ''Year'',
                P._AGE_GROUP_10YR AS AgeBand,
                P.SEX AS Sex,
                ISNULL(Q.Q1_MOBILITY,\'\'\'') AS Q1_MOBILITY,
                ISNULL(Q.Q1_SELF_CARE,\'\'\'') AS Q1_SELF_CARE,
                ISNULL(Q.Q1_ACTIVITY,\'\'\'') AS Q1_ACTIVITY,
                ISNULL(Q.Q1_DISCOMFORT,\'\'\'') AS Q1_DISCOMFORT,
                ISNULL(Q.Q1_ANXIETY,\'\'\'') AS Q1_ANXIETY,
                ISNULL(Q.Q1_EQ5D_PROFILE,\'\'\'') AS Q1_EQ5D_PROFILE,
                ISNULL(CAST(Q.Q1_EQ5D_INDEX AS VARCHAR),\'\'\'') AS Q1_EQ5D_INDEX,
                ISNULL(Q.Q2_MOBILITY,\'\'\'') AS Q2_MOBILITY,
                ISNULL(Q.Q2_SELF_CARE,\'\'\'') AS Q2_SELF_CARE,
                ISNULL(Q.Q2_ACTIVITY,\'\'\'') AS Q2_ACTIVITY,
                ISNULL(Q.Q2_DISCOMFORT,\'\'\'') AS Q2_DISCOMFORT,
                ISNULL(Q.Q2_ANXIETY,\'\'\'') AS Q2_ANXIETY,
                ISNULL(Q.Q2_SATISFACTION,\'\'\'') AS Q2_SATISFACTION,
                ISNULL(Q.Q2_SUCCESS,\'\'\'') AS Q2_SUCCESS,
                ISNULL(Q.Q2_ALLERGY,\'\'\'') AS Q2_ALLERGY,
                ISNULL(Q.Q2_BLEEDING,\'\'\'') AS Q2_BLEEDING,
                ISNULL(Q.Q2_WOUND,\'\'\'') AS Q2_WOUND,
                ISNULL(Q.Q2_URINE,\'\'\'') AS Q2_URINE,
                ISNULL(Q.Q2_FURTHER_SURGERY,\'\'\'') AS Q2_FURTHER_SURGERY,
                ISNULL(Q.Q2_READMITTED,\'\'\'') AS Q2_READMITTED,
                ISNULL(Q.Q2_EQ5D_PROFILE,\'\'\'') AS Q2_EQ5D_PROFILE,
                ISNULL(CAST(Q.Q2_EQ5D_INDEX AS VARCHAR),\'\'\'') AS Q2_EQ5D_INDEX,
                ISNULL(CAST(Q.EQ5D_INDEX_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS HR_EQ_5D_Q2_PREDICTED,
                ISNULL(Q.Q1_EQ5D_HEALTH_SCALE,\'\'\'') AS Q1_EQ5D_HEALTH_SCALE,
                ISNULL(Q.Q2_EQ5D_HEALTH_SCALE,\'\'\'') AS Q2_EQ5D_HEALTH_SCALE,
                ISNULL(CAST(Q.EQ5D_HEALTH_SCALE_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS HR_EQ_VAS_Q2_PREDICTED,
                ISNULL(Q.HR_Q1_PAIN,\'\'\'') AS HR_Q1_PAIN,
                ISNULL(Q.HR_Q1_SUDDEN_PAIN,\'\'\'') AS HR_Q1_SUDDEN_PAIN,
                ISNULL(Q.HR_Q1_NIGHT_PAIN,\'\'\'') AS HR_Q1_NIGHT_PAIN,
                ISNULL(Q.HR_Q1_WASHING,\'\'\'') AS HR_Q1_WASHING,
                ISNULL(Q.HR_Q1_TRANSPORT,\'\'\'') AS HR_Q1_TRANSPORT,
                ISNULL(Q.HR_Q1_DRESSING,\'\'\'') AS HR_Q1_DRESSING,
                ISNULL(Q.HR_Q1_SHOPPING,\'\'\'') AS HR_Q1_SHOPPING,
                ISNULL(Q.HR_Q1_WALKING,\'\'\'') AS HR_Q1_WALKING,
                ISNULL(Q.HR_Q1_LIMPING,\'\'\'') AS HR_Q1_LIMPING,
                ISNULL(Q.HR_Q1_STAIRS,\'\'\'') AS HR_Q1_STAIRS,
                ISNULL(Q.HR_Q1_STANDING,\'\'\'') AS HR_Q1_STANDING,
                ISNULL(Q.HR_Q1_WORK,\'\'\'') AS HR_Q1_WORK,
                ISNULL(CAST(Q.HR_Q1_SCORE AS VARCHAR),\'\'\'') AS HR_Q1_SCORE,
                ISNULL(Q.HR_Q2_PAIN,\'\'\'') AS HR_Q2_PAIN,
                ISNULL(Q.HR_Q2_SUDDEN_PAIN,\'\'\'') AS HR_Q2_SUDDEN_PAIN,
                ISNULL(Q.HR_Q2_NIGHT_PAIN,\'\'\'') AS HR_Q2_NIGHT_PAIN,
                ISNULL(Q.HR_Q2_WASHING,\'\'\'') AS HR_Q2_WASHING,
                ISNULL(Q.HR_Q2_TRANSPORT,\'\'\'') AS HR_Q2_TRANSPORT,
                ISNULL(Q.HR_Q2_DRESSING,\'\'\'') AS HR_Q2_DRESSING,
                ISNULL(Q.HR_Q2_SHOPPING,\'\'\'') AS HR_Q2_SHOPPING,
                ISNULL(Q.HR_Q2_WALKING,\'\'\'') AS HR_Q2_WALKING,
                ISNULL(Q.HR_Q2_LIMPING,\'\'\'') AS HR_Q2_LIMPING,
                ISNULL(Q.HR_Q2_STAIRS,\'\'\'') AS HR_Q2_STAIRS,
                ISNULL(Q.HR_Q2_STANDING,\'\'\'') AS HR_Q2_STANDING,
                ISNULL(Q.HR_Q2_WORK,\'\'\'') AS HR_Q2_WORK,
                ISNULL(CAST(Q.HR_Q2_SCORE AS VARCHAR),\'\'\'') AS HR_Q2_SCORE,
                ISNULL(CAST(Q.HR_SCORE_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS HR_OHS_Q2_PREDICTED,
                
                DW.Q1_ASSISTED,
                ISNULL(DW.Q1_ASSISTED_BY,\'\'\'') AS Q1_ASSISTED_BY,
                DW.Q1_SYMPTOM_PERIOD,
                DW.Q1_PREVIOUS_SURGERY,
                DW.Q1_LIVING_ARRANGEMENTS,
                Q.Q1_DISABILITY,
                ISNULL(DW.HEART_DISEASE,\'\'\'') AS HEART_DISEASE,
                DW.HIGH_BP,
                DW.STROKE,
                DW.CIRCULATION,
                DW.LUNG_DISEASE,
                DW.DIABETES,
                DW.KIDNEY_DISEASE,
                DW.NERVOUS_SYSTEM,
                DW.LIVER_DISEASE,
                DW.CANCER,
                DW.DEPRESSION,
                DW.ARTHRITIS,
                ISNULL(DW.Q2_ASSISTED, \'\'\'') AS Q2_ASSISTED,
                ISNULL(DW.Q2_ASSISTED_BY, \'\'\'') AS Q2_ASSISTED_BY,
                ISNULL(DW.Q2_LIVING_ARRANGEMENTS, \'\'\'') AS Q2_LIVING_ARRANGEMENTS,
                ISNULL(DW.Q2_DISABILITY, \'\'\'') AS Q2_DISABILITY
            
        FROM proms.QUESTS_'+@table+' Q
        INNER JOIN [PromsDW].dbo.QUESTIONNAIRE_'+@table+' DW
        ON Q.PROMS_SERIAL_NO = DW.PROMS_SERIAL_NO
        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P
        ON Q._P_REF_PROM = P._P_REF_PROM
        LEFT JOIN proms.REF_PROCEDURES RP
        ON Q.PROMS_PROC_CODE = RP.PROMs_PROC_CODE
        WHERE Q.PROMS_PROC_CODE IN (''HR-PRIM'',''HR-REV'',''HR'')
        AND P._P_FYEAR_EPIEND = \'\'\'+@FYEAR+\'\'\'
        AND P._P_YEAR_MONTH_EPIEND <= \'\'\'+@END+\'\'\'
        AND Q._Q2_RETURNED_FLAG = 1
        AND P._P_REF_PROM IS NOT NULL
        )_
        '
        EXEC sp_executesql @sql;


        SELECT * INTO #TEMP2
        FROM
        (
        SELECT
                TP1.ProviderCode,
                TP1.PromsProcGroup,
                TP1.PROC_REVISION_FLAG,
                TP1.[Year],
                TP1.AgeBand,
                TP1.Sex,
                TP1.Q1_ASSISTED,
                TP1.Q1_ASSISTED_BY,
                TP1.Q1_SYMPTOM_PERIOD,
                TP1.Q1_PREVIOUS_SURGERY,
                TP1.Q1_LIVING_ARRANGEMENTS,
                TP1.Q1_DISABILITY,
                TP1.HEART_DISEASE,
                TP1.HIGH_BP,
                TP1.STROKE,
                TP1.CIRCULATION,
                TP1.LUNG_DISEASE,
                TP1.DIABETES,
                TP1.KIDNEY_DISEASE,
                TP1.NERVOUS_SYSTEM,
                TP1.LIVER_DISEASE,
                TP1.CANCER,
                TP1.DEPRESSION,
                TP1.ARTHRITIS,
                TP1.Q1_MOBILITY,
                TP1.Q1_SELF_CARE,
                TP1.Q1_ACTIVITY,
                TP1.Q1_DISCOMFORT,
                TP1.Q1_ANXIETY,
                TP1.Q1_EQ5D_PROFILE,
                TP1.Q1_EQ5D_INDEX,
                TP1.Q2_ASSISTED,
                TP1.Q2_ASSISTED_BY,
                TP1.Q2_LIVING_ARRANGEMENTS,
                TP1.Q2_DISABILITY,
                TP1.Q2_MOBILITY,
                TP1.Q2_SELF_CARE,
                TP1.Q2_ACTIVITY,
                TP1.Q2_DISCOMFORT,
                TP1.Q2_ANXIETY,
                TP1.Q2_SATISFACTION,
                TP1.Q2_SUCCESS,
                TP1.Q2_ALLERGY,
                TP1.Q2_BLEEDING,
                TP1.Q2_WOUND,
                TP1.Q2_URINE,
                TP1.Q2_FURTHER_SURGERY,
                TP1.Q2_READMITTED,
                TP1.Q2_EQ5D_PROFILE,
                TP1.Q2_EQ5D_INDEX,
                TP1.HR_EQ_5D_Q2_PREDICTED,
                TP1.Q1_EQ5D_HEALTH_SCALE,
                TP1.Q2_EQ5D_HEALTH_SCALE,
                TP1.HR_EQ_VAS_Q2_PREDICTED,
                TP1.HR_Q1_PAIN,
                TP1.HR_Q1_SUDDEN_PAIN,
                TP1.HR_Q1_NIGHT_PAIN,
                TP1.HR_Q1_WASHING,
                TP1.HR_Q1_TRANSPORT,
                TP1.HR_Q1_DRESSING,
                TP1.HR_Q1_SHOPPING,
                TP1.HR_Q1_WALKING,
                TP1.HR_Q1_LIMPING,
                TP1.HR_Q1_STAIRS,
                TP1.HR_Q1_STANDING,
                TP1.HR_Q1_WORK,
                TP1.HR_Q1_SCORE,
                TP1.HR_Q2_PAIN,
                TP1.HR_Q2_SUDDEN_PAIN,
                TP1.HR_Q2_NIGHT_PAIN,
                TP1.HR_Q2_WASHING,
                TP1.HR_Q2_TRANSPORT,
                TP1.HR_Q2_DRESSING,
                TP1.HR_Q2_SHOPPING,
                TP1.HR_Q2_WALKING,
                TP1.HR_Q2_LIMPING,
                TP1.HR_Q2_STAIRS,
                TP1.HR_Q2_STANDING,
                TP1.HR_Q2_WORK,
                TP1.HR_Q2_SCORE,
                TP1.HR_OHS_Q2_PREDICTED
        FROM
        (
            SELECT
                    ProviderCode,
                    Count = COUNT(*)
            FROM ##proms_processing_TEMP1
            GROUP BY
                    ProviderCode
        ) PC

        JOIN ##proms_processing_TEMP1 TP1
        ON PC.ProviderCode = TP1.ProviderCode
        WHERE COUNT > 5
        )_
        -- Suppresses Provider records where count for Ageband and Sex is between 1 and 5 ----------------

        SELECT * INTO #TEMP3
        FROM
        (
        SELECT
                #TEMP2.ProviderCode,
                #TEMP2.PromsProcGroup,
                #TEMP2.PROC_REVISION_FLAG,
                #TEMP2.[Year],
                CASE WHEN HC.Count BETWEEN 1 AND 5 THEN '*' ELSE #TEMP2.AgeBand END AS 'AgeBand',
                CASE WHEN HC.Count BETWEEN 1 AND 5 THEN '*' ELSE #TEMP2.Sex END AS 'Sex',
                #TEMP2.Q1_ASSISTED,
                #TEMP2.Q1_ASSISTED_BY,
                #TEMP2.Q1_SYMPTOM_PERIOD,
                #TEMP2.Q1_PREVIOUS_SURGERY,
                #TEMP2.Q1_LIVING_ARRANGEMENTS,
                #TEMP2.Q1_DISABILITY,
                #TEMP2.HEART_DISEASE,
                #TEMP2.HIGH_BP,
                #TEMP2.STROKE,
                #TEMP2.CIRCULATION,
                #TEMP2.LUNG_DISEASE,
                #TEMP2.DIABETES,
                #TEMP2.KIDNEY_DISEASE,
                #TEMP2.NERVOUS_SYSTEM,
                #TEMP2.LIVER_DISEASE,
                #TEMP2.CANCER,
                #TEMP2.DEPRESSION,
                #TEMP2.ARTHRITIS,
                #TEMP2.Q1_MOBILITY,
                #TEMP2.Q1_SELF_CARE,
                #TEMP2.Q1_ACTIVITY,
                #TEMP2.Q1_DISCOMFORT,
                #TEMP2.Q1_ANXIETY,
                #TEMP2.Q1_EQ5D_PROFILE,
                #TEMP2.Q1_EQ5D_INDEX,
                #TEMP2.Q2_ASSISTED,
                #TEMP2.Q2_ASSISTED_BY,
                #TEMP2.Q2_LIVING_ARRANGEMENTS,
                #TEMP2.Q2_DISABILITY,
                #TEMP2.Q2_MOBILITY,
                #TEMP2.Q2_SELF_CARE,
                #TEMP2.Q2_ACTIVITY,
                #TEMP2.Q2_DISCOMFORT,
                #TEMP2.Q2_ANXIETY,
                #TEMP2.Q2_SATISFACTION,
                #TEMP2.Q2_SUCCESS,
                #TEMP2.Q2_ALLERGY,
                #TEMP2.Q2_BLEEDING,
                #TEMP2.Q2_WOUND,
                #TEMP2.Q2_URINE,
                #TEMP2.Q2_FURTHER_SURGERY,
                #TEMP2.Q2_READMITTED,
                #TEMP2.Q2_EQ5D_PROFILE,
                #TEMP2.Q2_EQ5D_INDEX,
                #TEMP2.HR_EQ_5D_Q2_PREDICTED,
                #TEMP2.Q1_EQ5D_HEALTH_SCALE,
                #TEMP2.Q2_EQ5D_HEALTH_SCALE,
                #TEMP2.HR_EQ_VAS_Q2_PREDICTED,
                #TEMP2.HR_Q1_PAIN,
                #TEMP2.HR_Q1_SUDDEN_PAIN,
                #TEMP2.HR_Q1_NIGHT_PAIN,
                #TEMP2.HR_Q1_WASHING,
                #TEMP2.HR_Q1_TRANSPORT,
                #TEMP2.HR_Q1_DRESSING,
                #TEMP2.HR_Q1_SHOPPING,
                #TEMP2.HR_Q1_WALKING,
                #TEMP2.HR_Q1_LIMPING,
                #TEMP2.HR_Q1_STAIRS,
                #TEMP2.HR_Q1_STANDING,
                #TEMP2.HR_Q1_WORK,
                #TEMP2.HR_Q1_SCORE,
                #TEMP2.HR_Q2_PAIN,
                #TEMP2.HR_Q2_SUDDEN_PAIN,
                #TEMP2.HR_Q2_NIGHT_PAIN,
                #TEMP2.HR_Q2_WASHING,
                #TEMP2.HR_Q2_TRANSPORT,
                #TEMP2.HR_Q2_DRESSING,
                #TEMP2.HR_Q2_SHOPPING,
                #TEMP2.HR_Q2_WALKING,
                #TEMP2.HR_Q2_LIMPING,
                #TEMP2.HR_Q2_STAIRS,
                #TEMP2.HR_Q2_STANDING,
                #TEMP2.HR_Q2_WORK,
                #TEMP2.HR_Q2_SCORE,
                #TEMP2.HR_OHS_Q2_PREDICTED
        FROM
        (
        SELECT
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex,
                Count = COUNT(*)
        FROM #TEMP2
        GROUP BY
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex
        ) HC
        JOIN #TEMP2
        ON HC.ProviderCode = #TEMP2.ProviderCode
        AND HC.PromsProcGroup = #TEMP2.PromsProcGroup
        AND HC.AgeBand = #TEMP2.AgeBand
        AND HC.Sex = #TEMP2.Sex
        )_
        -------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #TEMP4
        FROM
        (
        SELECT
                nextsup_pref_order = ROW_NUMBER() OVER (PARTITION BY #TEMP3.ProviderCode ORDER BY HC2.Count,#TEMP3.AgeBand, #TEMP3.Sex),
                CASE WHEN HC2.Count BETWEEN 1 AND 5 THEN 1 ELSE 0 END AS SupFlag,
                HC2.Count AS DGcount,
                #TEMP3.ProviderCode,
                #TEMP3.PromsProcGroup,
                #TEMP3.PROC_REVISION_FLAG,
                #TEMP3.[Year],
                #TEMP3.AgeBand,
                #TEMP3.Sex,
                #TEMP3.Q1_ASSISTED,
                #TEMP3.Q1_ASSISTED_BY,
                #TEMP3.Q1_SYMPTOM_PERIOD,
                #TEMP3.Q1_PREVIOUS_SURGERY,
                #TEMP3.Q1_LIVING_ARRANGEMENTS,
                #TEMP3.Q1_DISABILITY,
                #TEMP3.HEART_DISEASE,
                #TEMP3.HIGH_BP,
                #TEMP3.STROKE,
                #TEMP3.CIRCULATION,
                #TEMP3.LUNG_DISEASE,
                #TEMP3.DIABETES,
                #TEMP3.KIDNEY_DISEASE,
                #TEMP3.NERVOUS_SYSTEM,
                #TEMP3.LIVER_DISEASE,
                #TEMP3.CANCER,
                #TEMP3.DEPRESSION,
                #TEMP3.ARTHRITIS,
                #TEMP3.Q1_MOBILITY,
                #TEMP3.Q1_SELF_CARE,
                #TEMP3.Q1_ACTIVITY,
                #TEMP3.Q1_DISCOMFORT,
                #TEMP3.Q1_ANXIETY,
                #TEMP3.Q1_EQ5D_PROFILE,
                #TEMP3.Q1_EQ5D_INDEX,
                #TEMP3.Q2_ASSISTED,
                #TEMP3.Q2_ASSISTED_BY,
                #TEMP3.Q2_LIVING_ARRANGEMENTS,
                #TEMP3.Q2_DISABILITY,
                #TEMP3.Q2_MOBILITY,
                #TEMP3.Q2_SELF_CARE,
                #TEMP3.Q2_ACTIVITY,
                #TEMP3.Q2_DISCOMFORT,
                #TEMP3.Q2_ANXIETY,
                #TEMP3.Q2_SATISFACTION,
                #TEMP3.Q2_SUCCESS,
                #TEMP3.Q2_ALLERGY,
                #TEMP3.Q2_BLEEDING,
                #TEMP3.Q2_WOUND,
                #TEMP3.Q2_URINE,
                #TEMP3.Q2_FURTHER_SURGERY,
                #TEMP3.Q2_READMITTED,
                #TEMP3.Q2_EQ5D_PROFILE,
                #TEMP3.Q2_EQ5D_INDEX,
                #TEMP3.HR_EQ_5D_Q2_PREDICTED,
                #TEMP3.Q1_EQ5D_HEALTH_SCALE,
                #TEMP3.Q2_EQ5D_HEALTH_SCALE,
                #TEMP3.HR_EQ_VAS_Q2_PREDICTED,
                #TEMP3.HR_Q1_PAIN,
                #TEMP3.HR_Q1_SUDDEN_PAIN,
                #TEMP3.HR_Q1_NIGHT_PAIN,
                #TEMP3.HR_Q1_WASHING,
                #TEMP3.HR_Q1_TRANSPORT,
                #TEMP3.HR_Q1_DRESSING,
                #TEMP3.HR_Q1_SHOPPING,
                #TEMP3.HR_Q1_WALKING,
                #TEMP3.HR_Q1_LIMPING,
                #TEMP3.HR_Q1_STAIRS,
                #TEMP3.HR_Q1_STANDING,
                #TEMP3.HR_Q1_WORK,
                #TEMP3.HR_Q1_SCORE,
                #TEMP3.HR_Q2_PAIN,
                #TEMP3.HR_Q2_SUDDEN_PAIN,
                #TEMP3.HR_Q2_NIGHT_PAIN,
                #TEMP3.HR_Q2_WASHING,
                #TEMP3.HR_Q2_TRANSPORT,
                #TEMP3.HR_Q2_DRESSING,
                #TEMP3.HR_Q2_SHOPPING,
                #TEMP3.HR_Q2_WALKING,
                #TEMP3.HR_Q2_LIMPING,
                #TEMP3.HR_Q2_STAIRS,
                #TEMP3.HR_Q2_STANDING,
                #TEMP3.HR_Q2_WORK,
                #TEMP3.HR_Q2_SCORE,
                #TEMP3.HR_OHS_Q2_PREDICTED
        FROM
        (
        SELECT
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex,
                Count = COUNT(*)
        FROM #TEMP3
        GROUP BY
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex
        )HC2
        JOIN #TEMP3
        ON HC2.ProviderCode = #TEMP3.ProviderCode
        AND HC2.PromsProcGroup = #TEMP3.PromsProcGroup
        AND HC2.AgeBand = #TEMP3.AgeBand
        AND HC2.Sex = #TEMP3.Sex
        )_	

        SELECT * INTO #TEMPREC
        FROM
        (
        SELECT
                DISTINCT ProviderCode
        FROM #TEMP4
        WHERE #TEMP4.SupFlag = 1
        )_
        SELECT * INTO #TEMPREC2
        FROM
        (
        SELECT
                SupFlag = 2,
                NS.ProviderCode,
                NS.PromsProcGroup,
                NS.[Year],
                NS.AgeBand,
                NS.Sex
        FROM
        (				
        SELECT 
                N.ProviderCode,
                N.PromsProcGroup,
                N.[Year],
                N.AgeBand,
                N.Sex,
                SupNext = ROW_NUMBER()OVER(PARTITION BY N.ProviderCode
                                        ORDER BY N.Scount,N.AgeBand,N.Sex)
        FROM 
        (
        SELECT
                Scount = COUNT(*),
                #TEMP4.DGcount,
                #TEMP4.ProviderCode,
                #TEMP4.PromsProcGroup,
                #TEMP4.[Year],
                #TEMP4.AgeBand,
                #TEMP4.Sex
        FROM #TEMP4
        WHERE #TEMP4.SupFlag = 0
        GROUP BY
                #TEMP4.DGcount,
                #TEMP4.ProviderCode,
                #TEMP4.PromsProcGroup,
                #TEMP4.[Year],
                #TEMP4.AgeBand,
                #TEMP4.Sex
        ) N
        )NS

        JOIN #TEMPREC TR
        ON TR.ProviderCode = NS.ProviderCode
        WHERE NS.SupNext = 1
        AND NS.AgeBand <> '*'
        )_

        SELECT *
        FROM
        (
        SELECT 
                T4.ProviderCode AS 'Provider Code',
                T4.PromsProcGroup AS 'Procedure',
                T4.PROC_REVISION_FLAG AS 'Revision Flag',
                T4.[Year] As 'Year',
                CASE WHEN TREC.SupFlag = 2 THEN '*' ELSE T4.AgeBand END AS 'Age Band',
                CASE WHEN TREC.SupFlag = 2 THEN '*' ELSE T4.Sex END AS 'Gender',
                T4.Q1_ASSISTED AS 'Pre-Op Q Assisted',
                T4.Q1_ASSISTED_BY AS 'Pre-Op Q Assisted By',
                T4.Q1_SYMPTOM_PERIOD AS 'Pre-Op Q Symptom Period',
                T4.Q1_PREVIOUS_SURGERY AS 'Pre-Op Q Previous Surgery',
                T4.Q1_LIVING_ARRANGEMENTS AS 'Pre-Op Q Living Arrangements',
                T4.Q1_DISABILITY AS 'Pre-Op Q Disability',
                T4.HEART_DISEASE AS 'Heart Disease',
                T4.HIGH_BP AS 'High Bp',
                T4.STROKE AS 'Stroke',
                T4.CIRCULATION AS 'Circulation',
                T4.LUNG_DISEASE AS 'Lung Disease',
                T4.DIABETES AS 'Diabetes',
                T4.KIDNEY_DISEASE AS 'Kidney Disease',
                T4.NERVOUS_SYSTEM AS 'Nervous System',
                T4.LIVER_DISEASE AS 'Liver Disease',
                T4.CANCER AS 'Cancer',
                T4.DEPRESSION AS 'Depression',
                T4.ARTHRITIS AS 'Arthritis',
                Q1_MOBILITY AS 'Pre-Op Q Mobility',
                Q1_SELF_CARE AS 'Pre-Op Q Self-Care',
                Q1_ACTIVITY AS 'Pre-Op Q Activity',
                Q1_DISCOMFORT AS 'Pre-Op Q Discomfort',
                Q1_ANXIETY AS 'Pre-Op Q Anxiety',
                Q1_EQ5D_PROFILE AS 'Pre-Op Q EQ5D Index Profile',
                Q1_EQ5D_INDEX AS 'Pre-Op Q EQ5D Index',
                T4.Q2_ASSISTED AS 'Post-Op Q Assisted',
                T4.Q2_ASSISTED_BY AS 'Post-Op Q Assisted By',
                T4.Q2_LIVING_ARRANGEMENTS AS 'Post-Op Q Living Arrangements',
                T4.Q2_DISABILITY AS 'Post-Op Q Disability',
                Q2_MOBILITY AS 'Post-Op Q Mobility',
                Q2_SELF_CARE AS 'Post-Op Q Self-Care',
                Q2_ACTIVITY AS 'Post-Op Q Activity',
                Q2_DISCOMFORT AS 'Post-Op Q Discomfort',
                Q2_ANXIETY AS 'Post-Op Q Anxiety',
                Q2_SATISFACTION AS 'Post-Op Q Satisfaction',
                Q2_SUCCESS AS 'Post-Op Q Sucess',
                Q2_ALLERGY AS 'Post-Op Q Allergy',
                Q2_BLEEDING AS 'Post-Op Q Bleeding',
                Q2_WOUND AS 'Post-Op Q Wound',
                Q2_URINE AS 'Post-Op Q Urine',
                Q2_FURTHER_SURGERY AS 'Post-Op Q Further Surgery',
                Q2_READMITTED AS 'Post-Op Q Readmitted',
                Q2_EQ5D_PROFILE AS 'Post-Op Q EQ5D Index Profile',
                Q2_EQ5D_INDEX AS 'Post-Op Q EQ5D Index',
                HR_EQ_5D_Q2_PREDICTED AS 'Hip Replacement EQ5D Index Post-Op Q Predicted',
                Q1_EQ5D_HEALTH_SCALE AS 'Pre-Op Q EQ VAS',
                Q2_EQ5D_HEALTH_SCALE AS 'Post-Op Q EQ VAS',
                HR_EQ_VAS_Q2_PREDICTED AS 'Hip Replacement EQ VAS Post-Op Q Predicted',
                HR_Q1_PAIN AS 'Hip Replacement Pre-Op Q Pain',
                HR_Q1_SUDDEN_PAIN AS 'Hip Replacement Pre-Op Q Sudden Pain',
                HR_Q1_NIGHT_PAIN AS 'Hip Replacement Pre-Op Q Night Pain',
                HR_Q1_WASHING AS 'Hip Replacement Pre-Op Q Washing',
                HR_Q1_TRANSPORT AS 'Hip Replacement Pre-Op Q Transport',
                HR_Q1_DRESSING AS 'Hip Replacement Pre-Op Q Dressing',
                HR_Q1_SHOPPING AS 'Hip Replacement Pre-Op Q Shopping',
                HR_Q1_WALKING AS 'Hip Replacement Pre-Op Q Walking',
                HR_Q1_LIMPING AS 'Hip Replacement Pre-Op Q Limping',
                HR_Q1_STAIRS AS 'Hip Replacement Pre-Op Q Stairs',
                HR_Q1_STANDING AS 'Hip Replacement Pre-Op Q Standing',
                HR_Q1_WORK AS 'Hip Replacement Pre-Op Q Work',
                HR_Q1_SCORE AS 'Hip Replacement Pre-Op Q Score',
                HR_Q2_PAIN AS 'Hip Replacement Post-Op Q Pain',
                HR_Q2_SUDDEN_PAIN AS 'Hip Replacement Post-Op Q Sudden Pain',
                HR_Q2_NIGHT_PAIN AS 'Hip Replacement Post-Op Q Night Pain',
                HR_Q2_WASHING AS 'Hip Replacement Post-Op Q Washing',
                HR_Q2_TRANSPORT AS 'Hip Replacement Post-Op Q Transport',
                HR_Q2_DRESSING AS 'Hip Replacement Post-Op Q Dressing',
                HR_Q2_SHOPPING AS 'Hip Replacement Post-Op Q Shopping',
                HR_Q2_WALKING AS 'Hip Replacement Post-Op Q Walking',
                HR_Q2_LIMPING AS 'Hip Replacement Post-Op Q Limping',
                HR_Q2_STAIRS AS 'Hip Replacement Post-Op Q Stairs',
                HR_Q2_STANDING AS 'Hip Replacement Post-Op Q Standing',
                HR_Q2_WORK AS 'Hip Replacement Post-Op Q Work',
                HR_Q2_SCORE AS 'Hip Replacement Post-Op Q Score',
                HR_OHS_Q2_PREDICTED AS 'Hip Replacement OHS Post-Op Q Predicted'
                
        FROM #TEMP4 T4
        LEFT JOIN #TEMPREC2 TREC
        ON T4.ProviderCode = TREC.ProviderCode
        AND T4.PromsProcGroup = TREC.PromsProcGroup
        AND T4.[Year] = TREC.[Year]
        AND T4.AgeBand = TREC.AgeBand
        AND T4.Sex = TREC.Sex
        )_
        ORDER BY
                CASE WHEN [Age Band] = '*' THEN 1 ELSE 0 END DESC,
                [Provider Code],
                [Age Band],
                Gender,
                [Hip Replacement EQ5D Index Post-Op Q Predicted],
                [Hip Replacement EQ VAS Post-Op Q Predicted],
                [Pre-Op Q EQ5D Index Profile],
                [Post-Op Q EQ5D Index Profile] ,
                [Pre-Op Q EQ VAS],
                [Post-Op Q EQ VAS],
                [Hip Replacement Post-Op Q Score],
                [Hip Replacement OHS Post-Op Q Predicted]



        DROP TABLE ##proms_processing_TEMP1;
        DROP TABLE #TEMP2;
        DROP TABLE #TEMP3;
        DROP TABLE #TEMP4
        DROP TABLE #TEMPREC
        DROP TABLE #TEMPREC2

    '''
    return hr_prov_records_str

def kr_prov_records(startfyear,table):
    yearmonth=f'{int(startfyear)+1}-03'
    kr_prov_records_str = f'''
        DECLARE @FYEAR  VARCHAR (4);
        DECLARE @END  VARCHAR (10);
        DECLARE @table VARCHAR (15);
        DECLARE @sql NVARCHAR(MAX);

        ----------------------- Update these variables as required --------------------------

        SET @FYEAR = '{startfyear}'		    -- represents a financial year, the year selected is the first year of the period e.g. 2012-13 is @FYEAR 2012
        SET @END = '{yearmonth}'		-- year and month of the last month for this dateset
        SET @table = '{table}'	-- processing run with X suffix
        -------------------------------------------------------------------------------------
        SET NOCOUNT ON

        SET @sql =
        '
        SELECT * INTO ##proms_processing_TEMP1
        FROM
        (
        SELECT
                P._P_PROCODE AS ProviderCode,
                RP.Description AS PromsProcGroup,
                P.PROC_REVISION_FLAG,
                \'\'\'+@FYEAR+'/'+RIGHT(+@FYEAR+1,2)+\'\'\' AS ''Year'',
                P._AGE_GROUP_10YR AS AgeBand,
                P.SEX AS Sex,
                ISNULL(Q.Q1_MOBILITY,\'\'\'') AS Q1_MOBILITY,
                ISNULL(Q.Q1_SELF_CARE,\'\'\'') AS Q1_SELF_CARE,
                ISNULL(Q.Q1_ACTIVITY,\'\'\'') AS Q1_ACTIVITY,
                ISNULL(Q.Q1_DISCOMFORT,\'\'\'') AS Q1_DISCOMFORT,
                ISNULL(Q.Q1_ANXIETY,\'\'\'') AS Q1_ANXIETY,
                ISNULL(Q.Q1_EQ5D_PROFILE,\'\'\'') AS Q1_EQ5D_PROFILE,
                ISNULL(CAST(Q.Q1_EQ5D_INDEX AS VARCHAR),\'\'\'') AS Q1_EQ5D_INDEX,
                ISNULL(Q.Q2_MOBILITY,\'\'\'') AS Q2_MOBILITY,
                ISNULL(Q.Q2_SELF_CARE,\'\'\'') AS Q2_SELF_CARE,
                ISNULL(Q.Q2_ACTIVITY,\'\'\'') AS Q2_ACTIVITY,
                ISNULL(Q.Q2_DISCOMFORT,\'\'\'') AS Q2_DISCOMFORT,
                ISNULL(Q.Q2_ANXIETY,\'\'\'') AS Q2_ANXIETY,
                ISNULL(Q.Q2_SATISFACTION,\'\'\'') AS Q2_SATISFACTION,
                ISNULL(Q.Q2_SUCCESS,\'\'\'') AS Q2_SUCCESS,
                ISNULL(Q.Q2_ALLERGY,\'\'\'') AS Q2_ALLERGY,
                ISNULL(Q.Q2_BLEEDING,\'\'\'') AS Q2_BLEEDING,
                ISNULL(Q.Q2_WOUND,\'\'\'') AS Q2_WOUND,
                ISNULL(Q.Q2_URINE,\'\'\'') AS Q2_URINE,
                ISNULL(Q.Q2_FURTHER_SURGERY,\'\'\'') AS Q2_FURTHER_SURGERY,
                ISNULL(Q.Q2_READMITTED,\'\'\'') AS Q2_READMITTED,
                ISNULL(Q.Q2_EQ5D_PROFILE,\'\'\'') AS Q2_EQ5D_PROFILE,
                ISNULL(CAST(Q.Q2_EQ5D_INDEX AS VARCHAR),\'\'\'') AS Q2_EQ5D_INDEX,
                ISNULL(CAST(Q.EQ5D_INDEX_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS KR_EQ_5D_Q2_PREDICTED,
                ISNULL(Q.Q1_EQ5D_HEALTH_SCALE,\'\'\'') AS Q1_EQ5D_HEALTH_SCALE,
                ISNULL(Q.Q2_EQ5D_HEALTH_SCALE,\'\'\'') AS Q2_EQ5D_HEALTH_SCALE,
                ISNULL(CAST(Q.EQ5D_HEALTH_SCALE_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS KR_EQ_VAS_Q2_PREDICTED,
                ISNULL(CAST(Q.KR_Q1_PAIN AS VARCHAR),\'\'\'') AS KR_Q1_PAIN, 
                ISNULL(CAST(Q.KR_Q1_NIGHT_PAIN AS VARCHAR),\'\'\'') AS KR_Q1_NIGHT_PAIN, 
                ISNULL(CAST(Q.KR_Q1_WASHING AS VARCHAR),\'\'\'') AS KR_Q1_WASHING, 
                ISNULL(CAST(Q.KR_Q1_TRANSPORT AS VARCHAR),\'\'\'') AS KR_Q1_TRANSPORT, 
                ISNULL(CAST(Q.KR_Q1_WALKING AS VARCHAR),\'\'\'') AS KR_Q1_WALKING, 
                ISNULL(CAST(Q.KR_Q1_STANDING AS VARCHAR),\'\'\'') AS KR_Q1_STANDING, 
                ISNULL(CAST(Q.KR_Q1_LIMPING AS VARCHAR),\'\'\'') AS KR_Q1_LIMPING, 
                ISNULL(CAST(Q.KR_Q1_KNEELING AS VARCHAR),\'\'\'') AS KR_Q1_KNEELING, 
                ISNULL(CAST(Q.KR_Q1_WORK AS VARCHAR),\'\'\'') AS KR_Q1_WORK, 
                ISNULL(CAST(Q.KR_Q1_CONFIDENCE AS VARCHAR),\'\'\'') AS KR_Q1_CONFIDENCE, 
                ISNULL(CAST(Q.KR_Q1_SHOPPING AS VARCHAR),\'\'\'') AS KR_Q1_SHOPPING, 
                ISNULL(CAST(Q.KR_Q1_STAIRS AS VARCHAR),\'\'\'') AS KR_Q1_STAIRS,
                ISNULL(CAST(Q.KR_Q1_SCORE AS VARCHAR),\'\'\'') AS KR_Q1_SCORE,
                ISNULL(CAST(Q.KR_Q2_PAIN AS VARCHAR),\'\'\'') AS KR_Q2_PAIN, 
                ISNULL(CAST(Q.KR_Q2_NIGHT_PAIN AS VARCHAR),\'\'\'') AS KR_Q2_NIGHT_PAIN, 
                ISNULL(CAST(Q.KR_Q2_WASHING AS VARCHAR),\'\'\'') AS KR_Q2_WASHING, 
                ISNULL(CAST(Q.KR_Q2_TRANSPORT AS VARCHAR),\'\'\'') AS KR_Q2_TRANSPORT, 
                ISNULL(CAST(Q.KR_Q2_WALKING AS VARCHAR),\'\'\'') AS KR_Q2_WALKING, 
                ISNULL(CAST(Q.KR_Q2_STANDING AS VARCHAR),\'\'\'') AS KR_Q2_STANDING, 
                ISNULL(CAST(Q.KR_Q2_LIMPING AS VARCHAR),\'\'\'') AS KR_Q2_LIMPING, 
                ISNULL(CAST(Q.KR_Q2_KNEELING AS VARCHAR),\'\'\'') AS KR_Q2_KNEELING, 
                ISNULL(CAST(Q.KR_Q2_WORK AS VARCHAR),\'\'\'') AS KR_Q2_WORK, 
                ISNULL(CAST(Q.KR_Q2_CONFIDENCE AS VARCHAR),\'\'\'') AS KR_Q2_CONFIDENCE, 
                ISNULL(CAST(Q.KR_Q2_SHOPPING AS VARCHAR),\'\'\'') AS KR_Q2_SHOPPING, 
                ISNULL(CAST(Q.KR_Q2_STAIRS AS VARCHAR),\'\'\'') AS KR_Q2_STAIRS,
                ISNULL(CAST(Q.KR_Q2_SCORE AS VARCHAR),\'\'\'') AS KR_Q2_SCORE,
                ISNULL(CAST(Q.KR_SCORE_EXPECTED_FINAL_MODEL3 AS VARCHAR),\'\'\'') AS KR_OKS_Q2_PREDICTED,
                
                DW.Q1_ASSISTED,
                ISNULL(DW.Q1_ASSISTED_BY,\'\'\'') AS Q1_ASSISTED_BY,
                DW.Q1_SYMPTOM_PERIOD,
                DW.Q1_PREVIOUS_SURGERY,
                DW.Q1_LIVING_ARRANGEMENTS,
                Q.Q1_DISABILITY,
                ISNULL(DW.HEART_DISEASE,\'\'\'') AS HEART_DISEASE,
                DW.HIGH_BP,
                DW.STROKE,
                DW.CIRCULATION,
                DW.LUNG_DISEASE,
                DW.DIABETES,
                DW.KIDNEY_DISEASE,
                DW.NERVOUS_SYSTEM,
                DW.LIVER_DISEASE,
                DW.CANCER,
                DW.DEPRESSION,
                DW.ARTHRITIS,
                ISNULL(DW.Q2_ASSISTED, \'\'\'') AS Q2_ASSISTED,
                ISNULL(DW.Q2_ASSISTED_BY, \'\'\'') AS Q2_ASSISTED_BY,
                ISNULL(DW.Q2_LIVING_ARRANGEMENTS, \'\'\'') AS Q2_LIVING_ARRANGEMENTS,
                ISNULL(DW.Q2_DISABILITY, \'\'\'') AS Q2_DISABILITY

        FROM proms.QUESTS_'+@table+' Q
        INNER JOIN [PromsDW].dbo.QUESTIONNAIRE_'+@table+' DW
        ON Q.PROMS_SERIAL_NO = DW.PROMS_SERIAL_NO
        LEFT JOIN proms.HES_PROCEDURES_'+@table+' P
        ON Q._P_REF_PROM = P._P_REF_PROM
        LEFT JOIN proms.REF_PROCEDURES RP
        ON Q.PROMS_PROC_CODE = RP.PROMs_PROC_CODE
        WHERE Q.PROMS_PROC_CODE IN (''KR-PRIM'',''KR-REV'',''KR'')
        AND P._P_FYEAR_EPIEND = \'\'\'+@FYEAR+\'\'\'
        AND P._P_YEAR_MONTH_EPIEND <= \'\'\'+@END+\'\'\'
        AND Q._Q2_RETURNED_FLAG = 1
        AND P._P_REF_PROM IS NOT NULL
        )_
        '
        EXEC sp_executesql @sql;

        -- Removes Providers with less than 5 records -------------------------------------------------

        SELECT * INTO #TEMP2
        FROM
        (
        SELECT
                TP1.ProviderCode,
                TP1.PromsProcGroup,
                TP1.PROC_REVISION_FLAG,
                TP1.[Year],
                TP1.AgeBand,
                TP1.Sex,
                TP1.Q1_ASSISTED,
                TP1.Q1_ASSISTED_BY,
                TP1.Q1_SYMPTOM_PERIOD,
                TP1.Q1_PREVIOUS_SURGERY,
                TP1.Q1_LIVING_ARRANGEMENTS,
                TP1.Q1_DISABILITY,
                TP1.HEART_DISEASE,
                TP1.HIGH_BP,
                TP1.STROKE,
                TP1.CIRCULATION,
                TP1.LUNG_DISEASE,
                TP1.DIABETES,
                TP1.KIDNEY_DISEASE,
                TP1.NERVOUS_SYSTEM,
                TP1.LIVER_DISEASE,
                TP1.CANCER,
                TP1.DEPRESSION,
                TP1.ARTHRITIS,
                TP1.Q1_MOBILITY,
                TP1.Q1_SELF_CARE,
                TP1.Q1_ACTIVITY,
                TP1.Q1_DISCOMFORT,
                TP1.Q1_ANXIETY,
                TP1.Q1_EQ5D_PROFILE,
                TP1.Q1_EQ5D_INDEX,
                TP1.Q2_ASSISTED,
                TP1.Q2_ASSISTED_BY,
                TP1.Q2_LIVING_ARRANGEMENTS,
                TP1.Q2_DISABILITY,
                TP1.Q2_MOBILITY,
                TP1.Q2_SELF_CARE,
                TP1.Q2_ACTIVITY,
                TP1.Q2_DISCOMFORT,
                TP1.Q2_ANXIETY,
                TP1.Q2_SATISFACTION,
                TP1.Q2_SUCCESS,
                TP1.Q2_ALLERGY,
                TP1.Q2_BLEEDING,
                TP1.Q2_WOUND,
                TP1.Q2_URINE,
                TP1.Q2_FURTHER_SURGERY,
                TP1.Q2_READMITTED,
                TP1.Q2_EQ5D_PROFILE,
                TP1.Q2_EQ5D_INDEX,
                TP1.KR_EQ_5D_Q2_PREDICTED,
                TP1.Q1_EQ5D_HEALTH_SCALE,
                TP1.Q2_EQ5D_HEALTH_SCALE,
                TP1.KR_EQ_VAS_Q2_PREDICTED,
                TP1.KR_Q1_PAIN, 
                TP1.KR_Q1_NIGHT_PAIN, 
                TP1.KR_Q1_WASHING, 
                TP1.KR_Q1_TRANSPORT, 
                TP1.KR_Q1_WALKING, 
                TP1.KR_Q1_STANDING, 
                TP1.KR_Q1_LIMPING, 
                TP1.KR_Q1_KNEELING, 
                TP1.KR_Q1_WORK, 
                TP1.KR_Q1_CONFIDENCE, 
                TP1.KR_Q1_SHOPPING, 
                TP1.KR_Q1_STAIRS,
                TP1.KR_Q1_SCORE,
                TP1.KR_Q2_PAIN, 
                TP1.KR_Q2_NIGHT_PAIN, 
                TP1.KR_Q2_WASHING, 
                TP1.KR_Q2_TRANSPORT, 
                TP1.KR_Q2_WALKING, 
                TP1.KR_Q2_STANDING, 
                TP1.KR_Q2_LIMPING, 
                TP1.KR_Q2_KNEELING, 
                TP1.KR_Q2_WORK, 
                TP1.KR_Q2_CONFIDENCE, 
                TP1.KR_Q2_SHOPPING, 
                TP1.KR_Q2_STAIRS,
                TP1.KR_Q2_SCORE,
                TP1.KR_OKS_Q2_PREDICTED
        FROM
        (
            SELECT
                ProviderCode,
                count = COUNT(*)
            FROM ##proms_processing_TEMP1
            GROUP BY
                ProviderCode
        ) PC

        JOIN ##proms_processing_TEMP1 TP1
        ON PC.ProviderCode = TP1.ProviderCode
        WHERE count > 5
        )_
        -- Suppresses Provider records where count for Ageband and Sex is between 1 and 5 ----------------

        SELECT * INTO #TEMP3
        FROM
        (
        SELECT
                #TEMP2.ProviderCode,
                #TEMP2.PromsProcGroup,
                #TEMP2.PROC_REVISION_FLAG,
                #TEMP2.[Year],
                CASE WHEN HC.count BETWEEN 1 AND 5 THEN '*' ELSE #TEMP2.AgeBand END AS 'AgeBand',
                CASE WHEN HC.count BETWEEN 1 AND 5 THEN '*' ELSE #TEMP2.Sex END AS 'Sex',
                #TEMP2.Q1_ASSISTED,
                #TEMP2.Q1_ASSISTED_BY,
                #TEMP2.Q1_SYMPTOM_PERIOD,
                #TEMP2.Q1_PREVIOUS_SURGERY,
                #TEMP2.Q1_LIVING_ARRANGEMENTS,
                #TEMP2.Q1_DISABILITY,
                #TEMP2.HEART_DISEASE,
                #TEMP2.HIGH_BP,
                #TEMP2.STROKE,
                #TEMP2.CIRCULATION,
                #TEMP2.LUNG_DISEASE,
                #TEMP2.DIABETES,
                #TEMP2.KIDNEY_DISEASE,
                #TEMP2.NERVOUS_SYSTEM,
                #TEMP2.LIVER_DISEASE,
                #TEMP2.CANCER,
                #TEMP2.DEPRESSION,
                #TEMP2.ARTHRITIS,
                #TEMP2.Q1_MOBILITY,
                #TEMP2.Q1_SELF_CARE,
                #TEMP2.Q1_ACTIVITY,
                #TEMP2.Q1_DISCOMFORT,
                #TEMP2.Q1_ANXIETY,
                #TEMP2.Q1_EQ5D_PROFILE,
                #TEMP2.Q1_EQ5D_INDEX,
                #TEMP2.Q2_ASSISTED,
                #TEMP2.Q2_ASSISTED_BY,
                #TEMP2.Q2_LIVING_ARRANGEMENTS,
                #TEMP2.Q2_DISABILITY,
                #TEMP2.Q2_MOBILITY,
                #TEMP2.Q2_SELF_CARE,
                #TEMP2.Q2_ACTIVITY,
                #TEMP2.Q2_DISCOMFORT,
                #TEMP2.Q2_ANXIETY,
                #TEMP2.Q2_SATISFACTION,
                #TEMP2.Q2_SUCCESS,
                #TEMP2.Q2_ALLERGY,
                #TEMP2.Q2_BLEEDING,
                #TEMP2.Q2_WOUND,
                #TEMP2.Q2_URINE,
                #TEMP2.Q2_FURTHER_SURGERY,
                #TEMP2.Q2_READMITTED,
                #TEMP2.Q2_EQ5D_PROFILE,
                #TEMP2.Q2_EQ5D_INDEX,
                #TEMP2.KR_EQ_5D_Q2_PREDICTED,
                #TEMP2.Q1_EQ5D_HEALTH_SCALE,
                #TEMP2.Q2_EQ5D_HEALTH_SCALE,
                #TEMP2.KR_EQ_VAS_Q2_PREDICTED,
                #TEMP2.KR_Q1_PAIN, 
                #TEMP2.KR_Q1_NIGHT_PAIN, 
                #TEMP2.KR_Q1_WASHING, 
                #TEMP2.KR_Q1_TRANSPORT, 
                #TEMP2.KR_Q1_WALKING, 
                #TEMP2.KR_Q1_STANDING, 
                #TEMP2.KR_Q1_LIMPING, 
                #TEMP2.KR_Q1_KNEELING, 
                #TEMP2.KR_Q1_WORK, 
                #TEMP2.KR_Q1_CONFIDENCE, 
                #TEMP2.KR_Q1_SHOPPING, 
                #TEMP2.KR_Q1_STAIRS,
                #TEMP2.KR_Q1_SCORE,
                #TEMP2.KR_Q2_PAIN, 
                #TEMP2.KR_Q2_NIGHT_PAIN, 
                #TEMP2.KR_Q2_WASHING, 
                #TEMP2.KR_Q2_TRANSPORT, 
                #TEMP2.KR_Q2_WALKING, 
                #TEMP2.KR_Q2_STANDING, 
                #TEMP2.KR_Q2_LIMPING, 
                #TEMP2.KR_Q2_KNEELING, 
                #TEMP2.KR_Q2_WORK, 
                #TEMP2.KR_Q2_CONFIDENCE, 
                #TEMP2.KR_Q2_SHOPPING, 
                #TEMP2.KR_Q2_STAIRS,
                #TEMP2.KR_Q2_SCORE,
                #TEMP2.KR_OKS_Q2_PREDICTED
        FROM
        (
            SELECT
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex,
                count = COUNT(*)
            FROM #TEMP2
            GROUP BY
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex
        ) HC

        JOIN #TEMP2
        ON HC.ProviderCode = #TEMP2.ProviderCode
        AND HC.PromsProcGroup = #TEMP2.PromsProcGroup
        AND HC.AgeBand = #TEMP2.AgeBand
        AND HC.Sex = #TEMP2.Sex
        )_
        -------------------------------------------------------------------------------------------------------------------------
        SELECT * INTO #TEMP4
        FROM
        (
        SELECT
                nextsup_pref_order = ROW_NUMBER() OVER (PARTITION BY #TEMP3.ProviderCode ORDER BY KC2.Count,#TEMP3.AgeBand, #TEMP3.Sex),
                CASE WHEN KC2.Count BETWEEN 1 AND 5 THEN 1 ELSE 0 END AS SupFlag,
                KC2.Count AS DGcount,
                #TEMP3.ProviderCode,
                #TEMP3.PromsProcGroup,
                #TEMP3.PROC_REVISION_FLAG,
                #TEMP3.[Year],
                #TEMP3.AgeBand,
                #TEMP3.Sex,
                #TEMP3.Q1_ASSISTED,
                #TEMP3.Q1_ASSISTED_BY,
                #TEMP3.Q1_SYMPTOM_PERIOD,
                #TEMP3.Q1_PREVIOUS_SURGERY,
                #TEMP3.Q1_LIVING_ARRANGEMENTS,
                #TEMP3.Q1_DISABILITY,
                #TEMP3.HEART_DISEASE,
                #TEMP3.HIGH_BP,
                #TEMP3.STROKE,
                #TEMP3.CIRCULATION,
                #TEMP3.LUNG_DISEASE,
                #TEMP3.DIABETES,
                #TEMP3.KIDNEY_DISEASE,
                #TEMP3.NERVOUS_SYSTEM,
                #TEMP3.LIVER_DISEASE,
                #TEMP3.CANCER,
                #TEMP3.DEPRESSION,
                #TEMP3.ARTHRITIS,
                #TEMP3.Q1_MOBILITY,
                #TEMP3.Q1_SELF_CARE,
                #TEMP3.Q1_ACTIVITY,
                #TEMP3.Q1_DISCOMFORT,
                #TEMP3.Q1_ANXIETY,
                #TEMP3.Q1_EQ5D_PROFILE,
                #TEMP3.Q1_EQ5D_INDEX,
                #TEMP3.Q2_ASSISTED,
                #TEMP3.Q2_ASSISTED_BY,
                #TEMP3.Q2_LIVING_ARRANGEMENTS,
                #TEMP3.Q2_DISABILITY,
                #TEMP3.Q2_MOBILITY,
                #TEMP3.Q2_SELF_CARE,
                #TEMP3.Q2_ACTIVITY,
                #TEMP3.Q2_DISCOMFORT,
                #TEMP3.Q2_ANXIETY,
                #TEMP3.Q2_SATISFACTION,
                #TEMP3.Q2_SUCCESS,
                #TEMP3.Q2_ALLERGY,
                #TEMP3.Q2_BLEEDING,
                #TEMP3.Q2_WOUND,
                #TEMP3.Q2_URINE,
                #TEMP3.Q2_FURTHER_SURGERY,
                #TEMP3.Q2_READMITTED,
                #TEMP3.Q2_EQ5D_PROFILE,
                #TEMP3.Q2_EQ5D_INDEX,
                #TEMP3.KR_EQ_5D_Q2_PREDICTED,
                #TEMP3.Q1_EQ5D_HEALTH_SCALE,
                #TEMP3.Q2_EQ5D_HEALTH_SCALE,
                #TEMP3.KR_EQ_VAS_Q2_PREDICTED,
                #TEMP3.KR_Q1_PAIN, 
                #TEMP3.KR_Q1_NIGHT_PAIN, 
                #TEMP3.KR_Q1_WASHING, 
                #TEMP3.KR_Q1_TRANSPORT, 
                #TEMP3.KR_Q1_WALKING, 
                #TEMP3.KR_Q1_STANDING, 
                #TEMP3.KR_Q1_LIMPING, 
                #TEMP3.KR_Q1_KNEELING, 
                #TEMP3.KR_Q1_WORK, 
                #TEMP3.KR_Q1_CONFIDENCE, 
                #TEMP3.KR_Q1_SHOPPING, 
                #TEMP3.KR_Q1_STAIRS,
                #TEMP3.KR_Q1_SCORE,
                #TEMP3.KR_Q2_PAIN, 
                #TEMP3.KR_Q2_NIGHT_PAIN, 
                #TEMP3.KR_Q2_WASHING, 
                #TEMP3.KR_Q2_TRANSPORT, 
                #TEMP3.KR_Q2_WALKING, 
                #TEMP3.KR_Q2_STANDING, 
                #TEMP3.KR_Q2_LIMPING, 
                #TEMP3.KR_Q2_KNEELING, 
                #TEMP3.KR_Q2_WORK, 
                #TEMP3.KR_Q2_CONFIDENCE, 
                #TEMP3.KR_Q2_SHOPPING, 
                #TEMP3.KR_Q2_STAIRS,
                #TEMP3.KR_Q2_SCORE,
                #TEMP3.KR_OKS_Q2_PREDICTED
        FROM
        (
            SELECT
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex,
                count = COUNT(*)
            FROM #TEMP3
            GROUP BY
                ProviderCode,
                PromsProcGroup,
                AgeBand,
                Sex
        ) KC2

        JOIN #TEMP3
        ON KC2.ProviderCode = #TEMP3.ProviderCode
        AND KC2.PromsProcGroup = #TEMP3.PromsProcGroup
        AND KC2.AgeBand = #TEMP3.AgeBand
        AND KC2.Sex = #TEMP3.Sex
        )_

        SELECT * INTO #TEMPREC
        FROM
        (
        SELECT
                DISTINCT ProviderCode
        FROM #TEMP4
        WHERE #TEMP4.SupFlag = 1
        )_

        SELECT * INTO #TEMPREC2
        FROM
        (
        SELECT
                SupFlag = 2,
                NS.ProviderCode,
                NS.PromsProcGroup,
                NS.[Year],
                NS.AgeBand,
                NS.Sex
        FROM
        (				
        SELECT 
                N.ProviderCode,
                N.PromsProcGroup,
                N.[Year],
                N.AgeBand,
                N.Sex,
                SupNext = ROW_NUMBER()OVER(PARTITION BY N.ProviderCode
                                        ORDER BY N.Scount,N.AgeBand,N.Sex)
        FROM 
        (
        SELECT
                Scount = COUNT(*),
                #TEMP4.DGcount,
                #TEMP4.ProviderCode,
                #TEMP4.PromsProcGroup,
                #TEMP4.[Year],
                #TEMP4.AgeBand,
                #TEMP4.Sex

        FROM #TEMP4
        WHERE #TEMP4.SupFlag = 0
        GROUP BY
                #TEMP4.DGcount,
                #TEMP4.ProviderCode,
                #TEMP4.PromsProcGroup,
                #TEMP4.[Year],
                #TEMP4.AgeBand,
                #TEMP4.Sex
        ) N
        )NS

        JOIN #TEMPREC TR
        ON TR.ProviderCode = NS.ProviderCode

        WHERE NS.SupNext = 1
        AND NS.AgeBand <> '*'
        )_

        SELECT *
        FROM
        (
        SELECT 
                T4.ProviderCode AS 'Provider Code',
                T4.PromsProcGroup AS 'Procedure',
                T4.PROC_REVISION_FLAG AS 'Revision Flag',
                T4.[Year] As 'Year',
                CASE WHEN TREC.SupFlag = 2 THEN '*' ELSE T4.AgeBand END AS 'Age Band',
                CASE WHEN TREC.SupFlag = 2 THEN '*' ELSE T4.Sex END AS 'Gender',
                T4.Q1_ASSISTED AS 'Pre-Op Q Assisted',
                T4.Q1_ASSISTED_BY AS 'Pre-Op Q Assisted By',
                T4.Q1_SYMPTOM_PERIOD AS 'Pre-Op Q Symptom Period',
                T4.Q1_PREVIOUS_SURGERY AS 'Pre-Op Q Previous Surgery',
                T4.Q1_LIVING_ARRANGEMENTS AS 'Pre-Op Q Living Arrangements',
                T4.Q1_DISABILITY AS 'Pre-Op Q Disability',
                T4.HEART_DISEASE AS 'Heart Disease',
                T4.HIGH_BP AS 'High Bp',
                T4.STROKE AS 'Stroke',
                T4.CIRCULATION AS 'Circulation',
                T4.LUNG_DISEASE AS 'Lung Disease',
                T4.DIABETES AS 'Diabetes',
                T4.KIDNEY_DISEASE AS 'Kidney Disease',
                T4.NERVOUS_SYSTEM AS 'Nervous System',
                T4.LIVER_DISEASE AS 'Liver Disease',
                T4.CANCER AS 'Cancer',
                T4.DEPRESSION AS 'Depression',
                T4.ARTHRITIS AS 'Arthritis',
                Q1_MOBILITY AS 'Pre-Op Q Mobility',
                Q1_SELF_CARE AS 'Pre-Op Q Self-Care',
                Q1_ACTIVITY AS 'Pre-Op Q Activity',
                Q1_DISCOMFORT AS 'Pre-Op Q Discomfort',
                Q1_ANXIETY AS 'Pre-Op Q Anxiety',
                Q1_EQ5D_PROFILE AS 'Pre-Op Q EQ5D Index Profile',
                Q1_EQ5D_INDEX AS 'Pre-Op Q EQ5D Index',
                T4.Q2_ASSISTED AS 'Post-Op Q Assisted',
                T4.Q2_ASSISTED_BY AS 'Post-Op Q Assisted By',
                T4.Q2_LIVING_ARRANGEMENTS AS 'Post-Op Q Living Arrangements',
                T4.Q2_DISABILITY AS 'Post-Op Q Disability',
                Q2_MOBILITY AS 'Post-Op Q Mobility',
                Q2_SELF_CARE AS 'Post-Op Q Self-Care',
                Q2_ACTIVITY AS 'Post-Op Q Activity',
                Q2_DISCOMFORT AS 'Post-Op Q Discomfort',
                Q2_ANXIETY AS 'Post-Op Q Anxiety',
                Q2_SATISFACTION AS 'Post-Op Q Satisfaction',
                Q2_SUCCESS AS 'Post-Op Q Sucess',
                Q2_ALLERGY AS 'Post-Op Q Allergy',
                Q2_BLEEDING AS 'Post-Op Q Bleeding',
                Q2_WOUND AS 'Post-Op Q Wound',
                Q2_URINE AS 'Post-Op Q Urine',
                Q2_FURTHER_SURGERY AS 'Post-Op Q Further Surgery',
                Q2_READMITTED AS 'Post-Op Q Readmitted',
                Q2_EQ5D_PROFILE AS 'Post-Op Q EQ5D Index Profile',
                Q2_EQ5D_INDEX AS 'Post-Op Q EQ5D Index',
                KR_EQ_5D_Q2_PREDICTED AS 'Knee Replacement EQ 5D Index Post-Op Q Predicted',
                Q1_EQ5D_HEALTH_SCALE AS 'Pre-Op Q EQ VAS',
                Q2_EQ5D_HEALTH_SCALE AS 'Post-Op Q EQ VAS',
                KR_EQ_VAS_Q2_PREDICTED AS 'Knee Replacement EQ VAS_Post-Op Q Predicted',
                KR_Q1_PAIN AS 'Knee Replacement Pre-Op Q Pain', 
                KR_Q1_NIGHT_PAIN AS 'Knee Replacement Pre-Op Q Night Pain', 
                KR_Q1_WASHING AS 'Knee Replacement Pre-Op Q Washing', 
                KR_Q1_TRANSPORT AS 'Knee Replacement Pre-Op Q Transport', 
                KR_Q1_WALKING AS 'Knee Replacement Pre-Op Q Walking', 
                KR_Q1_STANDING AS 'Knee Replacement Pre-Op Q Standing', 
                KR_Q1_LIMPING AS 'Knee Replacement Pre-Op Q Limping', 
                KR_Q1_KNEELING AS 'Knee Replacement Pre-Op Q Kneeling', 
                KR_Q1_WORK AS 'Knee Replacement Pre-Op Q Work', 
                KR_Q1_CONFIDENCE AS 'Knee Replacement Pre-Op Q Confidence', 
                KR_Q1_SHOPPING AS 'Knee Replacement Pre-Op Q Shopping', 
                KR_Q1_STAIRS AS 'Knee Replacement Pre-Op Q Stairs',
                KR_Q1_SCORE AS 'Knee Replacement Pre-Op Q Score',
                KR_Q2_PAIN AS 'Knee Replacement Post-Op Q Pain', 
                KR_Q2_NIGHT_PAIN AS 'Knee Replacement Post-Op Q Night Pain', 
                KR_Q2_WASHING AS 'Knee Replacement Post-Op Q Washing', 
                KR_Q2_TRANSPORT AS 'Knee Replacement Post-Op Q Transport', 
                KR_Q2_WALKING AS 'Knee Replacement Post-Op Q Walking', 
                KR_Q2_STANDING AS 'Knee Replacement Post-Op Q Standing', 
                KR_Q2_LIMPING AS 'Knee Replacement Post-Op Q Limping', 
                KR_Q2_KNEELING AS 'Knee Replacement Post-Op Q Kneeling', 
                KR_Q2_WORK AS 'Knee Replacement Post-Op Q Work', 
                KR_Q2_CONFIDENCE AS 'Knee Replacement Post-Op Q Confidence', 
                KR_Q2_SHOPPING AS 'Knee Replacement Post-Op Q Shopping', 
                KR_Q2_STAIRS AS 'Knee Replacement Post-Op Q Stairs',
                KR_Q2_SCORE AS 'Knee Replacement Post-Op Q Score',
                KR_OKS_Q2_PREDICTED AS 'Knee Replacement OKS Post-Op Q Predicted'
            
        FROM #TEMP4 T4
        LEFT JOIN #TEMPREC2 TREC
        ON T4.ProviderCode = TREC.ProviderCode
        AND T4.PromsProcGroup = TREC.PromsProcGroup
        AND T4.[Year] = TREC.[Year]
        AND T4.AgeBand = TREC.AgeBand
        AND T4.Sex = TREC.Sex
        )T

        ORDER BY
                CASE WHEN [Age Band] = '*' THEN 1 ELSE 0 END DESC,
                [Provider Code],
                [Age Band],
                Gender,
                [Knee Replacement EQ 5D Index Post-Op Q Predicted] ,
                [Knee Replacement EQ VAS_Post-Op Q Predicted],
                [Pre-Op Q EQ5D Index Profile],
                [Post-Op Q EQ5D Index Profile],
                [Pre-Op Q EQ VAS],
                [Post-Op Q EQ VAS],
                [Knee Replacement Post-Op Q Score],
                [Knee Replacement OKS Post-Op Q Predicted]


            
        DROP TABLE ##proms_processing_TEMP1;
        DROP TABLE #TEMP2;
        DROP TABLE #TEMP3;
        DROP TABLE #TEMP4
        DROP TABLE #TEMPREC
        DROP TABLE #TEMPREC2
    '''
    return kr_prov_records_str