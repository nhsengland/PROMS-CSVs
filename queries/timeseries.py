def new_timeseries_table(fromdate,todate,startfyear,table):
    timeseries_str = f'''
        DECLARE @latest_from DATE ='{fromdate}' 
        DECLARE @latest_to   DATE ='{todate}'
        DECLARE @latest_year VARCHAR(4) = '{startfyear}'

        SET ANSI_NULLS ON
        SET ANSI_WARNINGS ON



        --episodes from latest year, must amend processing run to latest--

        SELECT * INTO #HES_epsL FROM
        (select 
        CASE WHEN GROUPING(_P_PROCODE) = 0 THEN _P_PROCODE ELSE 'England' END AS 'H1_Org',
        case when PROMS_PROC_CODE ='HR' and PROC_REVISION_FLAG = 0 then 'HR-PRIM'
            when PROMS_PROC_CODE ='HR' and PROC_REVISION_FLAG = 1 then 'HR-REV'
            when PROMS_PROC_CODE ='KR' and PROC_REVISION_FLAG = 0 then 'KR-PRIM'
            when PROMS_PROC_CODE ='KR' and PROC_REVISION_FLAG = 1 then 'KR-REV'
            else null
        end as 'H2_Proc',
        COUNT (EPIKEY) as 'H3_Episodes'
        from PROMS_PUBLICATION.proms.HES_PROCEDURES_{table} --UPDATE THIS
        where EPISTART between @latest_from and @latest_to and PROMS_PROC_CODE in ('hr','kr')
        group by rollup(_P_PROCODE), PROMS_PROC_CODE, PROC_REVISION_FLAG

        union

        select 
        CASE WHEN GROUPING(CCG_CODE) = 0 THEN CCG_CODE ELSE 'England_CCG' END AS 'H1_Org',
        case when PROMS_PROC_CODE ='HR' and PROC_REVISION_FLAG = 0 then 'HR-PRIM'
            when PROMS_PROC_CODE ='HR' and PROC_REVISION_FLAG = 1 then 'HR-REV'
            when PROMS_PROC_CODE ='KR' and PROC_REVISION_FLAG = 0 then 'KR-PRIM'
            when PROMS_PROC_CODE ='KR' and PROC_REVISION_FLAG = 1 then 'KR-REV'
            else null
        end as 'H2_Proc',
        COUNT (EPIKEY) as 'H3_Episodes'
        from PROMS_PUBLICATION.proms.HES_PROCEDURES_{table} --UPDATE THIS
        where EPISTART between @latest_from and @latest_to and PROMS_PROC_CODE in ('hr','kr')
        group by rollup(CCG_CODE), PROMS_PROC_CODE, PROC_REVISION_FLAG

        union

        select 
        CASE WHEN GROUPING(_P_PROCODE) = 0 THEN _P_PROCODE ELSE 'England' END AS 'H1_Org',
        PROMS_PROC_CODE as 'H2_Proc',
        COUNT (EPIKEY) as 'H3_Episodes'
        from PROMS_PUBLICATION.proms.HES_PROCEDURES_{table} --UPDATE THIS
        where EPISTART between @latest_from and @latest_to and PROMS_PROC_CODE in ('hr','kr')
        group by rollup(_P_PROCODE), PROMS_PROC_CODE

        union

        select 
        CASE WHEN GROUPING(CCG_CODE) = 0 THEN CCG_CODE ELSE 'England_CCG' END AS 'H1_Org',
        PROMS_PROC_CODE as 'H2_Proc',
        COUNT (EPIKEY) as 'H3_Episodes'
        from PROMS_PUBLICATION.proms.HES_PROCEDURES_{table} --UPDATE THIS
        where EPISTART between @latest_from and @latest_to and PROMS_PROC_CODE in ('hr','kr')
        group by rollup(CCG_CODE), PROMS_PROC_CODE, PROC_REVISION_FLAG


        )_


        --latest episodes joined to agg stats--

        select * into #Agg from (
        select 
        FYEAR,
        OrgType,
        OrgCode,
        H1_Org,
        case 
        when ProcGroup='HR' THEN 'Total Hip Replacement'
        when ProcGroup='HR-PRIM' THEN 'Hip Replacement Primary'
        when ProcGroup='HR-REV' THEN 'Hip Replacement Revision'
        when ProcGroup='KR' THEN 'Total Knee Replacement'
        when ProcGroup='KR-PRIM' THEN 'Knee Replacement Primary'
        when ProcGroup='KR-REV' THEN 'Knee Replacement Revision'
        else null end as ProcGroup,
        H2_Proc,
        case 
        when Measure='OHS' then 'Oxford Hip Score'
        when Measure='OKS' then 'Oxford Knee Score'
        when Measure='Index' then 'EQ-5D Index'
        when Measure='Vas' then 'EQ VAS'
        else null end as Measure,
        H3_Episodes,
        InputCount,
        cast(AdjHG as decimal(5,3)) as AdjHG,
        [Outlier 95%],
        [Outlier 99.8%]

        from PROMS_PUBLICATION.proms.PROMS_AGGREGATED_STATS_{table} a -- UPDATE THIS
        join #hes_epsL b on a.orgcode = b.H1_Org and a.ProcGroup = b.H2_Proc
        where FYear=@latest_year)_


        -- UPDATE THIS SECTION FOR A NEW YEAR
        if object_id('PROMS_DEVELOPMENT.proms.TIME_SERIES_{startfyear}') is not null
        drop table PROMS_DEVELOPMENT.proms.TIME_SERIES_{startfyear}

        select *,
        convert(varchar, (case when H3_Episodes in (1,2,3,4,5) then -1 else InputCount end)) as 'Modelled_Records_{startfyear}',
        convert(varchar, (case when InputCount between 1 and 29 then -30 when InputCount=0 then -999 else AdjHG end)) as 'Adjusted_Health_Gain_{startfyear}',
        case 
        when InputCount between 1 and 29 then 'Insufficient records'
        when InputCount >=30 and [Outlier 95%] not in ('+ve', '-ve') then 'Not an outlier'
        when InputCount >=30 and [Outlier 95%] = '+ve' and [Outlier 99.8%] not in ('+ve', '-ve') then 'Positive outlier (95%)'
        when InputCount >=30 and [Outlier 95%] = '-ve' and [Outlier 99.8%] not in ('+ve', '-ve') then 'Negative outlier (95%)'
        when InputCount >=30 and [Outlier 99.8%] = '+ve' then 'Positive outlier (99.8%)'
        when InputCount >=30 and [Outlier 99.8%] = '-ve' then 'Negative outlier (99.8%)'
        else 'No procedures'
        end as 'Outlier_{startfyear}'
        into [PROMS_DEVELOPMENT].[proms].[TIME_SERIES_{startfyear}]
        from #Agg
    '''
    return timeseries_str

def compile_timeseries(startfyear):
    timeseries_str = f'''
        SET ANSI_NULLS ON
        SET ANSI_WARNINGS ON
        SET NOCOUNT ON

        -- Outputs
        -- MR = -1 then number to be supressed
        -- AHG = -30 then number to be supressed; -999 then MR = 0


        select * into #TS from 

        (select

        -- update here for the latest year
        ts_{startfyear}.OrgCode,
        case when ts_{startfyear}.orgcode='England' then 'England' else orgs.OrgName end as OrgName,
        ts_{startfyear}.ProcGroup as 'Procedure',
        ts_{startfyear}.Measure,

        ts_{str(int(startfyear)-9)}.Modelled_Records_{str(int(startfyear)-9)},
        ts_{str(int(startfyear)-8)}.Modelled_Records_{str(int(startfyear)-8)},
        ts_{str(int(startfyear)-7)}.Modelled_Records_{str(int(startfyear)-7)},
        ts_{str(int(startfyear)-6)}.Modelled_Records_{str(int(startfyear)-6)},
        ts_{str(int(startfyear)-5)}.Modelled_Records_{str(int(startfyear)-5)},
        ts_{str(int(startfyear)-4)}.Modelled_Records_{str(int(startfyear)-4)},
        ts_{str(int(startfyear)-3)}.Modelled_Records_{str(int(startfyear)-3)},
        ts_{str(int(startfyear)-2)}.Modelled_Records_{str(int(startfyear)-2)},
        ts_{str(int(startfyear)-1)}.Modelled_Records_{str(int(startfyear)-1)},
        ts_{startfyear}.Modelled_Records_{startfyear},
        -- add a new year on if needed


        ts_{str(int(startfyear)-9)}.Adjusted_Health_Gain_{str(int(startfyear)-9)},
        ts_{str(int(startfyear)-8)}.Adjusted_Health_Gain_{str(int(startfyear)-8)},
        ts_{str(int(startfyear)-7)}.Adjusted_Health_Gain_{str(int(startfyear)-7)},
        ts_{str(int(startfyear)-6)}.Adjusted_Health_Gain_{str(int(startfyear)-6)},
        ts_{str(int(startfyear)-5)}.Adjusted_Health_Gain_{str(int(startfyear)-5)},
        ts_{str(int(startfyear)-4)}.Adjusted_Health_Gain_{str(int(startfyear)-4)},
        ts_{str(int(startfyear)-3)}.Adjusted_Health_Gain_{str(int(startfyear)-3)},
        ts_{str(int(startfyear)-2)}.Adjusted_Health_Gain_{str(int(startfyear)-2)},
        ts_{str(int(startfyear)-1)}.Adjusted_Health_Gain_{str(int(startfyear)-1)},
        ts_{startfyear}.Adjusted_Health_Gain_{startfyear},
        -- add a new year on if needed


        ts_{str(int(startfyear)-9)}.Outlier_{str(int(startfyear)-9)},
        ts_{str(int(startfyear)-8)}.Outlier_{str(int(startfyear)-8)},
        ts_{str(int(startfyear)-7)}.Outlier_{str(int(startfyear)-7)},
        ts_{str(int(startfyear)-6)}.Outlier_{str(int(startfyear)-6)},
        ts_{str(int(startfyear)-5)}.Outlier_{str(int(startfyear)-5)},
        ts_{str(int(startfyear)-4)}.Outlier_{str(int(startfyear)-4)},
        ts_{str(int(startfyear)-3)}.Outlier_{str(int(startfyear)-3)},
        ts_{str(int(startfyear)-2)}.Outlier_{str(int(startfyear)-2)},
        ts_{str(int(startfyear)-1)}.Outlier_{str(int(startfyear)-1)},
        ts_{startfyear}.Outlier_{startfyear}
        -- add a new year on if needed - prior to {str(int(startfyear)-4)} these fields were held in a different table


        from 
        -- add a new year if needed - new year needs to be first

        [proms].[TIME_SERIES_{startfyear}] ts_{startfyear} left join proms.REF_ORGS_202112_V1_ar as orgs on ts_{startfyear}.OrgCode = orgs.OrgCode  -- UPDATE THIS TABLE
        left join [proms].[TIME_SERIES_{str(int(startfyear)-1)}] ts_{str(int(startfyear)-1)} on ts_{startfyear}.OrgCode=ts_{str(int(startfyear)-1)}.OrgCode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-1)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-1)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-2)}] ts_{str(int(startfyear)-2)} on ts_{startfyear}.OrgCode=ts_{str(int(startfyear)-2)}.OrgCode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-2)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-2)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-3)}] ts_{str(int(startfyear)-3)} on ts_{startfyear}.OrgCode=ts_{str(int(startfyear)-3)}.OrgCode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-3)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-3)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-4)}] ts_{str(int(startfyear)-4)} on ts_{startfyear}.OrgCode=ts_{str(int(startfyear)-4)}.OrgCode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-4)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-4)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-5)}] ts_{str(int(startfyear)-5)} on ts_{startfyear}.orgcode=ts_{str(int(startfyear)-5)}.orgcode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-5)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-5)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-6)}] ts_{str(int(startfyear)-6)} on ts_{startfyear}.orgcode=ts_{str(int(startfyear)-6)}.orgcode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-6)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-6)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-7)}] ts_{str(int(startfyear)-7)} on ts_{startfyear}.orgcode=ts_{str(int(startfyear)-7)}.orgcode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-7)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-7)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-8)}] ts_{str(int(startfyear)-8)} on ts_{startfyear}.orgcode=ts_{str(int(startfyear)-8)}.orgcode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-8)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-8)}.Measure
        left join [proms].[TIME_SERIES_{str(int(startfyear)-9)}] ts_{str(int(startfyear)-9)} on ts_{startfyear}.orgcode=ts_{str(int(startfyear)-9)}.orgcode and ts_{startfyear}.ProcGroup=ts_{str(int(startfyear)-9)}.ProcGroup and ts_{startfyear}.Measure=ts_{str(int(startfyear)-9)}.Measure

        where ts_{startfyear}.OrgType in ('provider','england')
        )_


        select * into #Supp from (select

        OrgCode,
        OrgName,
        [Procedure],
        Measure,
        case when Modelled_Records_{str(int(startfyear)-9)} is null then '0' else Modelled_Records_{str(int(startfyear)-9)} end as Modelled_Records_{str(int(startfyear)-9)},
        case when Modelled_Records_{str(int(startfyear)-8)} is null then '0' else Modelled_Records_{str(int(startfyear)-8)} end as Modelled_Records_{str(int(startfyear)-8)},
        case when Modelled_Records_{str(int(startfyear)-7)} is null then '0' else Modelled_Records_{str(int(startfyear)-7)} end as Modelled_Records_{str(int(startfyear)-7)},
        case when Modelled_Records_{str(int(startfyear)-6)} is null then '0' else Modelled_Records_{str(int(startfyear)-6)} end as Modelled_Records_{str(int(startfyear)-6)},
        case when Modelled_Records_{str(int(startfyear)-5)} is null then '0' else Modelled_Records_{str(int(startfyear)-5)} end as Modelled_Records_{str(int(startfyear)-5)},
        case when Modelled_Records_{str(int(startfyear)-4)} = '-1' then '*' when Modelled_Records_{str(int(startfyear)-4)} is null then '-' else Modelled_Records_{str(int(startfyear)-4)} end as Modelled_Records_{str(int(startfyear)-4)},
        case when Modelled_Records_{str(int(startfyear)-3)} = '-1' then '*' else Modelled_Records_{str(int(startfyear)-3)} end as Modelled_Records_{str(int(startfyear)-3)},
        case when Modelled_Records_{str(int(startfyear)-2)} = '-1' then '*' else Modelled_Records_{str(int(startfyear)-2)} end as Modelled_Records_{str(int(startfyear)-2)},
        case when Modelled_Records_{str(int(startfyear)-1)} = '-1' then '*' else Modelled_Records_{str(int(startfyear)-1)} end as Modelled_Records_{str(int(startfyear)-1)},
        case when Modelled_Records_{startfyear} = '-1' then '*' else Modelled_Records_{startfyear} end as Modelled_Records_{startfyear},
        -- add a new year on if needed
        case when Modelled_Records_{str(int(startfyear)-9)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-9)} end as Adjusted_Health_Gain_{str(int(startfyear)-9)},
        case when Modelled_Records_{str(int(startfyear)-8)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-8)} end as Adjusted_Health_Gain_{str(int(startfyear)-8)},
        case when Modelled_Records_{str(int(startfyear)-7)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-7)} end as Adjusted_Health_Gain_{str(int(startfyear)-7)},
        case when Modelled_Records_{str(int(startfyear)-6)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-6)} end as Adjusted_Health_Gain_{str(int(startfyear)-6)},
        case when Modelled_Records_{str(int(startfyear)-5)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-5)} end as Adjusted_Health_Gain_{str(int(startfyear)-5)},
        case when Adjusted_Health_Gain_{str(int(startfyear)-4)} = '-30.000' then '-' when Adjusted_Health_Gain_{str(int(startfyear)-4)} = '-999.000' then '-' when Adjusted_Health_Gain_{str(int(startfyear)-4)} is null then '-' else Adjusted_Health_Gain_{str(int(startfyear)-4)} end as Adjusted_Health_Gain_{str(int(startfyear)-4)},
        case when Adjusted_Health_Gain_{str(int(startfyear)-3)} = '-30.000' then '-' when Adjusted_Health_Gain_{str(int(startfyear)-3)} = '-999.000' then '-' else Adjusted_Health_Gain_{str(int(startfyear)-3)} end as Adjusted_Health_Gain_{str(int(startfyear)-3)},
        case when Adjusted_Health_Gain_{str(int(startfyear)-2)} = '-30.000' then '-' when Adjusted_Health_Gain_{str(int(startfyear)-2)} = '-999.000' then '-' else Adjusted_Health_Gain_{str(int(startfyear)-2)} end as Adjusted_Health_Gain_{str(int(startfyear)-2)},
        case when Adjusted_Health_Gain_{str(int(startfyear)-1)} = '-30.000' then '-' when Adjusted_Health_Gain_{str(int(startfyear)-1)} = '-999.000' then '-' else Adjusted_Health_Gain_{str(int(startfyear)-1)} end as Adjusted_Health_Gain_{str(int(startfyear)-1)},
        case when Adjusted_Health_Gain_{startfyear} = '-30.000' then '-' when Adjusted_Health_Gain_{startfyear} = '-999.000' then '-' else Adjusted_Health_Gain_{startfyear} end as Adjusted_Health_Gain_{startfyear},
        -- add a new year on if needed
        case when Modelled_Records_{str(int(startfyear)-9)} is null then 'No procedures' else Outlier_{str(int(startfyear)-9)} end as Outlier_{str(int(startfyear)-9)},
        case when Modelled_Records_{str(int(startfyear)-8)} is null then 'No procedures' else Outlier_{str(int(startfyear)-8)} end as Outlier_{str(int(startfyear)-8)},
        case when Modelled_Records_{str(int(startfyear)-7)} is null then 'No procedures' else Outlier_{str(int(startfyear)-7)} end as Outlier_{str(int(startfyear)-7)},
        case when Modelled_Records_{str(int(startfyear)-6)} is null then 'No procedures' else Outlier_{str(int(startfyear)-6)} end as Outlier_{str(int(startfyear)-6)},
        case when Modelled_Records_{str(int(startfyear)-5)} is null then 'No procedures' else Outlier_{str(int(startfyear)-5)} end as Outlier_{str(int(startfyear)-5)},
        Outlier_{str(int(startfyear)-4)},
        Outlier_{str(int(startfyear)-3)},
        Outlier_{str(int(startfyear)-2)},
        Outlier_{str(int(startfyear)-1)},
        Outlier_{startfyear}
        -- add a new year on if needed

        from #TS)_

        --apply secondary suppression to TOTAL where REV is suppressed

        SELECT * INTO #HPRIM  FROM (SELECT * FROM #Supp where [procedure] ='Hip Replacement Primary')_
        SELECT * INTO #HREV   FROM (SELECT * FROM #Supp where [procedure] like 'Hip Replacement Revision')_
        SELECT * INTO #HTOTAL FROM (SELECT * FROM #Supp where [procedure] like 'Total Hip Replacement')_

        SELECT * INTO #KPRIM FROM (SELECT * FROM #Supp where [procedure] ='Knee Replacement Primary')_
        SELECT * INTO #KREV  FROM (SELECT * FROM #Supp where [procedure] like 'Knee Replacement Revision')_
        SELECT * INTO #KTOTAL FROM (SELECT * FROM #Supp where [procedure] like 'Total Knee Replacement')_

        SELECT a.[OrgCode]
            ,a.[OrgName]
            ,a.[Procedure]
            ,a.[Measure]
            ,case when c.[Modelled_Records_{str(int(startfyear)-9)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-9)}] else a.[Modelled_Records_{str(int(startfyear)-9)}] end as [Modelled_Records_{str(int(startfyear)-9)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-8)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-8)}] else a.[Modelled_Records_{str(int(startfyear)-8)}] end as [Modelled_Records_{str(int(startfyear)-8)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-7)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-7)}] else a.[Modelled_Records_{str(int(startfyear)-7)}] end as [Modelled_Records_{str(int(startfyear)-7)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-6)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-6)}] else a.[Modelled_Records_{str(int(startfyear)-6)}] end as [Modelled_Records_{str(int(startfyear)-6)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-5)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-5)}] else a.[Modelled_Records_{str(int(startfyear)-5)}] end as [Modelled_Records_{str(int(startfyear)-5)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-4)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-4)}] else a.[Modelled_Records_{str(int(startfyear)-4)}] end as [Modelled_Records_{str(int(startfyear)-4)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-3)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-3)}] else a.[Modelled_Records_{str(int(startfyear)-3)}] end as [Modelled_Records_{str(int(startfyear)-3)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-2)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-2)}] else a.[Modelled_Records_{str(int(startfyear)-2)}] end as [Modelled_Records_{str(int(startfyear)-2)}]
            ,case when c.[Modelled_Records_{str(int(startfyear)-1)}] = '*' then b.[Modelled_Records_{str(int(startfyear)-1)}] else a.[Modelled_Records_{str(int(startfyear)-1)}] end as [Modelled_Records_{str(int(startfyear)-1)}]
            ,case when c.[Modelled_Records_{startfyear}] = '*' then b.[Modelled_Records_{startfyear}] else a.[Modelled_Records_{startfyear}] end as [Modelled_Records_{startfyear}]
            -- add a new year on if needed
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-9)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-8)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-7)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-6)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-5)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-4)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-3)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-2)}]
            ,a.[Adjusted_Health_Gain_{str(int(startfyear)-1)}]
            ,a.[Adjusted_Health_Gain_{startfyear}]
            -- add a new year on if needed
            ,a.[Outlier_{str(int(startfyear)-9)}]
            ,a.[Outlier_{str(int(startfyear)-8)}]
            ,a.[Outlier_{str(int(startfyear)-7)}]
            ,a.[Outlier_{str(int(startfyear)-6)}]
            ,a.[Outlier_{str(int(startfyear)-5)}]
            ,a.[Outlier_{str(int(startfyear)-4)}]
            ,a.[Outlier_{str(int(startfyear)-3)}]
            ,a.[Outlier_{str(int(startfyear)-2)}]
            ,a.[Outlier_{str(int(startfyear)-1)}]
            ,a.[Outlier_{startfyear}]
            -- add a new year on if needed
        FROM #HTOTAL a
        left join #HPRIM b on a.orgcode=b.orgcode and a.measure=b.measure
        left join #HREV c on a.orgcode=c.orgcode and a.measure=c.measure

        

        union select * from #Hprim
        union select * from #Hrev
        
        UNION

        SELECT d.[OrgCode]
            ,d.[OrgName]
            ,d.[Procedure]
            ,d.[Measure]
            ,case when f.[Modelled_Records_{str(int(startfyear)-9)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-9)}] else d.[Modelled_Records_{str(int(startfyear)-9)}] end as [Modelled_Records_{str(int(startfyear)-9)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-8)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-8)}] else d.[Modelled_Records_{str(int(startfyear)-8)}] end as [Modelled_Records_{str(int(startfyear)-8)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-7)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-7)}] else d.[Modelled_Records_{str(int(startfyear)-7)}] end as [Modelled_Records_{str(int(startfyear)-7)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-6)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-6)}] else d.[Modelled_Records_{str(int(startfyear)-6)}] end as [Modelled_Records_{str(int(startfyear)-6)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-5)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-5)}] else d.[Modelled_Records_{str(int(startfyear)-5)}] end as [Modelled_Records_{str(int(startfyear)-5)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-4)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-4)}] else d.[Modelled_Records_{str(int(startfyear)-4)}] end as [Modelled_Records_{str(int(startfyear)-4)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-3)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-3)}] else d.[Modelled_Records_{str(int(startfyear)-3)}] end as [Modelled_Records_{str(int(startfyear)-3)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-2)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-2)}] else d.[Modelled_Records_{str(int(startfyear)-2)}] end as [Modelled_Records_{str(int(startfyear)-2)}]
            ,case when f.[Modelled_Records_{str(int(startfyear)-1)}] = '*' then e.[Modelled_Records_{str(int(startfyear)-1)}] else d.[Modelled_Records_{str(int(startfyear)-1)}] end as [Modelled_Records_{str(int(startfyear)-1)}]
            ,case when f.[Modelled_Records_{startfyear}] = '*' then e.[Modelled_Records_{startfyear}] else d.[Modelled_Records_{startfyear}] end as [Modelled_Records_{startfyear}]
            -- add a new year on if needed
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-9)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-8)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-7)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-6)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-5)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-4)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-3)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-2)}]
            ,d.[Adjusted_Health_Gain_{str(int(startfyear)-1)}]
            ,d.[Adjusted_Health_Gain_{startfyear}]
            -- add a new year on if needed
            ,d.[Outlier_{str(int(startfyear)-9)}]
            ,d.[Outlier_{str(int(startfyear)-8)}]
            ,d.[Outlier_{str(int(startfyear)-7)}]
            ,d.[Outlier_{str(int(startfyear)-6)}]
            ,d.[Outlier_{str(int(startfyear)-5)}]
            ,d.[Outlier_{str(int(startfyear)-4)}]
            ,d.[Outlier_{str(int(startfyear)-3)}]
            ,d.[Outlier_{str(int(startfyear)-2)}]
            ,d.[Outlier_{str(int(startfyear)-1)}]
            ,d.[Outlier_{startfyear}]
            -- add a new year on if needed
        FROM #KTOTAL d
        left join #KPRIM e on d.orgcode=e.orgcode and d.measure=e.measure
        left join #KREV f on d.orgcode=f.orgcode and d.measure=f.measure

        union select * from #Kprim
        union select * from #Krev
        order by orgcode,measure,[procedure]

        -- drop tables

        drop table #TS
        drop table #Supp

        drop table #hprim      
        drop table #hrev   
        drop table #htotal
        drop table #Kprim      
        drop table #Krev   
        drop table #Ktotal

    '''

    return timeseries_str

