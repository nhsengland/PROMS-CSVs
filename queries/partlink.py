from utils.convertfunc import procedure_count_all_procedures,procedure_count_HR,procedure_counts_HR_PRIM,procedure_counts_HR_REV,procedure_counts_KR,procedure_counts_KR_PRIM,procedure_counts_KR_REV,invalid_data_all_procs,invalid_data_HR, invalid_data_HR_REV,invalid_data_KR

def partlink(fromDate, to, table):

    '''creates the string for the sql participation linkage query, inserting the variables into it'''




    partlinkStr = (f'''DECLARE @from DATE = '{fromDate}'

        DECLARE @to   DATE = '{to}' 

        SET ANSI_NULLS OFF 

        SET ANSI_WARNINGS OFF 

        SET NOCOUNT ON 

        SET ARITHABORT OFF

        EXEC('SELECT * INTO #QUESTS FROM 

        (select 

        CASE WHEN GROUPING(_Q1_PROCODE) = 0 THEN _Q1_PROCODE ELSE ''England'' END AS ''Q1_Org'',

        [_PRIM_REV_PROC_CODE] as Q2_PROC,

        COUNT (_Q1_PROXY_DATE) as ''Q4_Q1Sent'',

        COUNT (_P_REF_HES) as ''Q6_Q1Link'',

        cast(COUNT (_P_REF_HES) *1.0  / Count (_Q1_PROXY_DATE) as decimal (10,7)) as ''Q7_Linkrate'',

        sum (case when _Q2_SENT_FLAG = 1 then 1 else 0 end) as ''Q8_Q2Sent'',

        cast(count (case when _Q2_SENT_FLAG = 1 then 1 end) *1.0 / Count (_Q1_PROXY_DATE) as decimal (10,7)) as ''Q9_Q2IssRate'',

        sum  (case when _Q2_RETURNED_FLAG = 1 then 1 else 0 end) as ''Q10_Q2Returned'',

        cast(sum (case when _Q2_RETURNED_FLAG = 1 then 1 else 0 end) *1.0  / sum (case when _Q2_SENT_FLAG = 1 then 1 else 0 end) as decimal (10,7)) as ''Q11_Q2Resp'' 

        from  proms.QUESTS_{table} 

        where _Q1_PROXY_DATE between \'\'\'+@from+\'\'\' and  \'\'\'+@to+\'\'\' and [_PRIM_REV_PROC_CODE] like ''%-%'' 

        group by [_PRIM_REV_PROC_CODE], rollup(_Q1_PROCODE) 


        union 


        select 

        CASE WHEN GROUPING(_Q1_PROCODE) = 0 THEN _Q1_PROCODE ELSE ''England'' END AS ''Q1_Org'',

        [PROMS_PROC_CODE] as Q2_PROC,

        COUNT (_Q1_PROXY_DATE) as ''Q4_Q1Sent'',

        COUNT (_P_REF_HES) as ''Q6_Q1Link'',

        cast(COUNT (_P_REF_HES) *1.0  / Count (_Q1_PROXY_DATE) as decimal(10,7)) as ''Q7_Linkrate'',

        sum (case when _Q2_SENT_FLAG = 1 then 1 else 0 end) as ''Q8_Q2Sent'',

        cast(count (case when _Q2_SENT_FLAG = 1 then 1 end) *1.0 / Count (_Q1_PROXY_DATE) as decimal (10,7)) as ''Q9_Q2IssRate'',

        sum  (case when _Q2_RETURNED_FLAG = 1 then 1 else 0 end) as ''Q10_Q2Returned'',

        cast(sum (case when _Q2_RETURNED_FLAG = 1 then 1 else 0 end) *1.0  / sum (case when _Q2_SENT_FLAG = 1 then 1 else 0 end) as decimal(10,7)) as ''Q11_Q2Resp'' 

        from  proms.QUESTS_{table} 

        where _Q1_PROXY_DATE between  \'\'\'+@from+\'\'\' and  \'\'\'+@to+\'\'\' 

        and [PROMS_PROC_CODE] in (''hr'',''kr'') 

        group by [PROMS_PROC_CODE], rollup(_Q1_PROCODE))_ 



        SELECT * INTO #HESEPS FROM 

        (select 

        CASE WHEN GROUPING(_P_PROCODE) = 0 THEN _P_PROCODE ELSE ''England'' END AS ''H1_Org'',

        case when PROMS_PROC_CODE =''HR'' and PROC_REVISION_FLAG = 0 then ''HR-PRIM'' 

            when PROMS_PROC_CODE =''HR'' and PROC_REVISION_FLAG = 1 then ''HR-REV'' 

            when PROMS_PROC_CODE =''KR'' and PROC_REVISION_FLAG = 0 then ''KR-PRIM'' 

            when PROMS_PROC_CODE =''KR'' and PROC_REVISION_FLAG = 1 then ''KR-REV'' 

            else PROMS_PROC_CODE 

        end as ''H2_Proc'',

        COUNT (EPIKEY) as ''H3_Episodes'' 

        from proms.HES_PROCEDURES_{table} 

        where EPISTART between  \'\'\'+@from+\'\'\' and  \'\'\'+@to+\'\'\' 

        and PROMS_PROC_CODE in (''hr'',''kr'') 

        group by rollup(_P_PROCODE), PROMS_PROC_CODE,PROC_REVISION_FLAG 


        union 


        select 

        CASE WHEN GROUPING(_P_PROCODE) = 0 THEN _P_PROCODE ELSE ''England'' END AS ''H1_Org'',

        PROMS_PROC_CODE as ''H2_Proc'',

        COUNT (EPIKEY) as ''H3_Episodes'' 

        from proms.HES_PROCEDURES_{table} 

        where EPISTART between  \'\'\'+@from+\'\'\' and  \'\'\'+@to+\'\'\' and PROMS_PROC_CODE in(''hr'',''kr'') 

        group by rollup(_P_PROCODE), PROMS_PROC_CODE 

        )_ 


        SELECT * into #COMBI FROM ( 

        SELECT 

        case when a.H1_Org IS null then b.Q1_Org else a.H1_Org end as QH1_Org,

        case when a.H2_Proc IS null then b.Q2_Proc else a.H2_Proc end as QH2_Proc,

        a.H3_Episodes, b.Q4_Q1Sent, 

        cast (b.Q4_Q1Sent *1.0 / a.H3_Episodes as decimal (10,7)) as QH5_PartRate,

        b.Q6_Q1Link, b.Q7_Linkrate, b.Q8_Q2Sent, b.Q9_Q2IssRate, b.Q10_Q2Returned,

        b.Q11_Q2Resp 

        FROM #HESEPS AS a full outer join #QUESTS AS b 

        ON a.H1_Org = b.Q1_Org and a.H2_Proc = b.Q2_Proc)_ 


        select * into #999 from(select 


        QH1_Org, QH2_Proc,

        case when QH2_Proc<>''AllProc'' and H3_Episodes IN (1,2,3,4,5) then ''-999'' else H3_Episodes END as H3_EPISODES,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) then ''-999'' else Q4_Q1Sent END as Q4_Q1SENT,

        case when QH2_Proc<>''AllProc'' and (H3_Episodes in (1,2,3,4,5) OR Q4_Q1Sent IN (1,2,3,4,5)) then ''-999'' else QH5_PARTRATE end as QH5_PARTRATE,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) and Q6_Q1Link IN (1,2,3,4,5) then ''-999'' else Q6_Q1Link END as Q6_Q1LINK,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) THEN ''-999'' ELSE Q7_Linkrate END AS Q7_LINKRATE,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) and Q8_Q2Sent IN (1,2,3,4,5) then ''-999'' else Q8_Q2Sent END as Q8_Q2SENT,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) THEN ''-999'' ELSE Q9_Q2IssRate END AS Q9_Q2ISSRATE,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) and Q10_Q2Returned IN (1,2,3,4,5) then ''-999'' else Q10_Q2Returned END as Q10_Q2RETURNED,

        case when QH2_Proc<>''AllProc'' and Q4_Q1Sent IN (1,2,3,4,5) THEN ''-999'' ELSE Q11_Q2Resp END AS Q11_Q2RESP 


        from #combi)_ 


        SELECT * into #all from(select 

        QH1_Org,case when grouping(QH2_Proc)=0 then  QH2_Proc else ''AllProc''end as QH2_PROC,

        sum(case when H3_EPISODES<0 then 0 else H3_EPISODES end) as H3_EPISODES,

        sum(case when Q4_Q1SENT<0 then 0 else Q4_Q1SENT end) as Q4_Q1SENT,

        sum(case when QH5_PARTRATE<0 then 0 else QH5_PARTRATE end) as QH5_PARTRATE,

        sum(case when Q6_Q1LINK<0 then 0 else Q6_Q1LINK end) as Q6_Q1LINK,

        sum(case when Q7_LINKRATE<0 then 0 else Q7_LINKRATE end) as Q7_LINKRATE,

        SUM(case when Q8_Q2SENT<0 then 0 else Q8_Q2SENT end) as Q8_Q2SENT,

        sum(case when Q9_Q2ISSRATE<0 then 0 else Q9_Q2ISSRATE end) as Q9_Q2ISSRATE,

        SUM(case when Q10_Q2Returned<0 then 0 else Q10_Q2Returned end) as Q10_Q2Returned,

        sum(case when Q11_Q2RESP<0 then 0 else Q11_Q2RESP end) as Q11_Q2RESP 

        FrOM #999 where QH2_PROC in (''hr'',''kr'') 

        group by QH1_Org,rollup(QH2_Proc) 

        )_ 


        select * into #raw from( 

        SELECT QH1_Org, QH2_PROC, H3_EPISODES, Q4_Q1SENT,

        cast (Q4_Q1Sent *1.0 / H3_Episodes as decimal (10,7)) as QH5_PartRate,

        Q6_Q1LINK,

        cast (Q6_Q1LINK *1.0 / Q4_Q1SENT as decimal (10,7)) as Q7_LinkRate,

        Q8_Q2SENT,

        cast (Q8_Q2SENT *1.0  / Q4_Q1SENT as decimal (10,7)) as Q9_Q2IssRate,

        Q10_Q2Returned,

        cast (Q10_Q2Returned *1.0 / Q8_Q2SENT as decimal (10,7)) as Q11_Q2Resp 

        from #all 

        where QH2_PROC=''AllProc'' 


        union 


        select * FrOM #999)_ 



        SELECT * into #pivot from (select 

        QH1_Org as ''OrgCode'',

        CASE WHEN OrgName is not null THEN OrgName ELSE ''ENGLAND'' END AS ''OrgName'',

        '''

        +'\n\t'.join(procedure_count_all_procedures)+

        '\n\t'.join(procedure_count_HR)+

        '\n\t'.join(procedure_counts_HR_PRIM)+

        '\n\t'.join(procedure_counts_HR_REV)+

        '\n\t'.join(procedure_counts_KR)+

        '\n\t'.join(procedure_counts_KR_PRIM)+

        '\n\t'.join(procedure_counts_KR_REV)[:-2]+

        f'''

        FROM #raw left join proms.REF_ORGS_{table} on QH1_Org=OrgCode 

        group by QH1_Org, OrgName 

        )_ 

        select 

        orgcode as ''Organisation Code'', 

        case when orgname=''England'' then OrgNAme else OrgName +'' (''+OrgCode+'')'' end as ''Organisation Name - SC'','''

        +'\n\t'.join(invalid_data_all_procs)+

        '\n\t'.join(invalid_data_HR)+


        f'''

        
        case when HR_REV_1 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_1 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_1 end as ''Primary Hip Replacement - Total HES Procedures'', 

        case when HR_REV_2 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_2 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_2 end as ''Primary Hip Replacement - Total Pre-Op Qs'', 

        case when HR_REV_3 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_3 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_3 end as ''Primary Hip Replacement - Participation Rate'', 

        case when HR_REV_4 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_4 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_4 end as ''Primary Hip Replacement - Total Linked'', 

        case when HR_REV_5 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_5 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_5 end as ''Primary Hip Replacement - Linkage rate'', 

        case when HR_REV_6 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_6 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_6 end as ''Primary Hip Replacement - Total Q2s sent to date'', 

        case when HR_REV_7 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_7 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_7 end as ''Primary Hip Replacement - Issue rate'', 

        case when HR_REV_8 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_8 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_8 end as ''Primary Hip Replacement - Total Q2s returned to date'', 

        case when HR_REV_9 in (''-999'',''-999.0000000'') then ''*'' when HR_PRIM_9 in (''-999'',''-999.0000000'') then ''*'' else HR_PRIM_9 end as ''Primary Hip Replacement - Response rate'', 

        '''+

        '\n\t'.join(invalid_data_HR_REV)+

        '\n\t'.join(invalid_data_KR)

        +f'''

        case when KR_REV_1 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_1 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_1 end as ''Primary Knee Replacement - Total HES Procedures'', 

        case when KR_REV_2 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_2 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_2 end as ''Primary Knee Replacement - Total Pre-Op Qs'', 

        case when KR_REV_2 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_3 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_3 end as ''Primary Knee Replacement - Participation Rate'', 

        case when KR_REV_3 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_4 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_4 end as ''Primary Knee Replacement - Total Linked'', 

        case when KR_REV_4 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_5 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_5 end as ''Primary Knee Replacement - Linkage rate'', 

        case when KR_REV_5 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_6 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_6 end as ''Primary Knee Replacement - Total Q2s sent to date'', 

        case when KR_REV_6 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_7 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_7 end as ''Primary Knee Replacement - Issue rate'', 

        case when KR_REV_7 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_8 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_8 end as ''Primary Knee Replacement - Total Q2s returned to date'', 

        case when KR_REV_8 in (''-999'',''-999.0000000'') then ''*'' when KR_PRIM_9 in (''-999'',''-999.0000000'') then ''*'' else KR_PRIM_9 end as ''Primary Knee Replacement - Response rate'', 

        case when KR_REV_1 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_1 end as ''Revision Knee Replacement - Total HES Procedures'', 

        case when KR_REV_2 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_2 end as ''Revision Knee Replacement - Total Pre-Op Qs'', 

        case when KR_REV_3 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_3 end as ''Revision Knee Replacement - Participation Rate'', 

        case when KR_REV_4 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_4 end as ''Revision Knee Replacement - Total Linked'', 

        case when KR_REV_5 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_5 end as ''Revision Knee Replacement - Linkage rate'', 

        case when KR_REV_6 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_6 end as ''Revision Knee Replacement - Total Q2s sent to date'', 

        case when KR_REV_7 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_7 end as ''Revision Knee Replacement - Issue rate'', 

        case when KR_REV_8 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_8 end as ''Revision Knee Replacement - Total Q2s returned to date'', 

        case when KR_REV_9 in (''-999'',''-999.0000000'') then ''*'' else KR_REV_9 end as ''Revision Knee Replacement - Response rate'' 

        from #pivot order by CASE WHEN [Orgcode] = ''England'' THEN 1 ELSE 2 END ASC') 

        DROP TABLE #QUESTS

        DROP TABLE #HESEPS 

        DROP TABLE #COMBI

        DROP TABLE #RAW

        DROP TABLE #999

        drop table #all

        drop table #pivot''')

    return partlinkStr

