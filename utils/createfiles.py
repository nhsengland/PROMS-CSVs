from connection import connection
import pandas as pd
from queries.partlink import partlink
from queries.provcomm import provcomm
from queries.keyfacts import key_facts
from queries.providerrecords import hr_prov_records,kr_prov_records
from queries.ccg import hr_ccg,kr_ccg
from queries.equality import equality
from queries.timeseries import new_timeseries_table,compile_timeseries

def createfiles(fromdate,todate,table,fyear,startfyear):
    cnxn = connection('PROMS_PUBLICATION')
    partlinkdata = pd.read_sql(partlink(fromdate,todate,table),cnxn)
    provcommdata = pd.read_sql(provcomm(fromdate,todate,startfyear,table),cnxn)
    keyfactsdata = pd.read_sql(key_facts(startfyear,todate,table),cnxn)

    hrprovrec = pd.read_sql(hr_prov_records(startfyear,table),cnxn)
    hrprovrec['Revision Flag'] = (hrprovrec['Revision Flag']).astype(int)

    krprovrec = pd.read_sql(kr_prov_records(startfyear,table),cnxn)
    krprovrec['Revision Flag'] = (krprovrec['Revision Flag']).astype(int)
    cnxn.close()

    cnxn2 = connection('PROMS_PUBLICATION')
    hrccgs = pd.read_sql(hr_ccg(startfyear,table),cnxn2)
    hrccgs['Revision Flag'] = (hrccgs['Revision Flag']).astype(int)
    krccgs = pd.read_sql(kr_ccg(startfyear,table),cnxn2)
    krccgs['Revision Flag'] = (krccgs['Revision Flag']).astype(int)
    equalities = pd.read_sql(equality(startfyear,table),cnxn2)
    cnxn2.close()

    cnxn3 = connection('PROMS_DEVELOPMENT')
    cursor = cnxn3.cursor()
    cursor.execute(new_timeseries_table(fromdate,todate,startfyear,table))
    cnxn3.commit()
    timeseries = pd.read_sql(compile_timeseries(startfyear),cnxn3)
    cnxn3.close()
    
    partlinkdata.to_csv(f'Final-CSV-Files/PartLink Hip and Knee Replacements {fyear}.csv',index=False,mode='w')
    provcommdata.to_csv(f'Final-CSV-Files/ProvComm Hip and Knee Replacements {fyear}.csv',index=False,mode='w')
    keyfactsdata.to_csv(f'Final-CSV-Files/Key Facts Hip and Knee Replacements {fyear}.csv',index=False,mode='w')
    hrprovrec.to_csv(f'Final-CSV-Files/Hip Replacement Provider {fyear}.csv',index=False,mode='w')
    hrccgs.to_csv(f'Final-CSV-Files/Hip Replacement CCG {fyear}.csv',index=False,mode='w')
    krprovrec.to_csv(f'Final-CSV-Files/Knee Replacement Provider {fyear}.csv',index=False,mode='w')
    krccgs.to_csv(f'Final-CSV-Files/Knee Replacement CCG {fyear}.csv',index=False,mode='w')
    equalities.to_csv(f'Final-CSV-Files/Equality {fyear}.csv',index=False,mode='w')
    timeseries.to_csv(f'Final-CSV-Files/Time Series Hip and Knee Replacements {fyear}.csv',index=False,mode='w')
