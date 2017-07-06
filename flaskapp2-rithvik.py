import os
from xml.etree import ElementTree
#import xlsxwriter
import sys
#import xlrd
import random
import string
import webbrowser
import pandas
from pandas import Series
import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
import datetime
import shutil
import numpy as np

DATABASE = 'test.db'
sessionparam = [];
app = Flask(__name__)
app.config.from_object(__name__)


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['STATIC_FOLDER'] = 'static/'
app.config['REDDY_FOLDER'] = 'reddy/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['xml','csv'])

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'    

def xmltocsv(username):
        
                
        path = os.path.join(app.config['UPLOAD_FOLDER'],username)
        path = path + "/"
        df_all_new = pandas.DataFrame()
        df_all_new1 = pandas.DataFrame()
        df_y = pandas.DataFrame()
        df_z = pandas.DataFrame()
        df_select = pandas.DataFrame()
        df_all = pandas.DataFrame()
          
        for fname in os.listdir(path):
                
                #filename = 'A20170202.0800-1000-0815-1000_SubNetwork=ONRM_ROOT_MO,SubNetwork=Hawaii,MeContext=LHI11025A_statsfile.xml'
                filename = fname
                filepth = os.path.join(path, filename)
                dom = ElementTree.parse(filepth)
                root_el = dom.getroot()
                parent_map = dict((c, p) for p in root_el.iter('md') for c in p)
                #print parent_map
                mdc = {}
                moid = {}
                fmoidlist = []
                fvaluelist = []
                fparamlist = []
                fdatelist = []
                fmotypelist = []
                fmovaluelist = []
                for md in root_el.iter('md'):
                    #print '1'
                    #print md.find('mi')
                    i = 1
                    
                    for mi in md.iter('mi'):
                        #print '1'
                        ts = {}
                        #print mi.find('mts')
                        ts[mi.find('mts').text] = 1
                        for mv in mi.iter('mv'):
                            valuelist = []
                            paramlist = []
                            moidlist = []
                            datelist =  []
                            for r in mv.iter('r'):
                                moidlist.append(mv.find('moid').text)
                                mosplit = [mm.split('=') for mm in mv.find('moid').text.split(',') ]
                                fmoidlist.append(mv.find('moid').text)
                                fmotypelist.append(mosplit[-1][0])
                                fmovaluelist.append(mosplit[-1][-1])
                                datelist.append(mi.find('mts').text)
                                fdatelist.append(mi.find('mts').text)
                                if not (r.text is None):
                                    try:
                                        valuelist.append(int(r.text))
                                        fvaluelist.append(int(r.text))
                                    except ValueError:
                                        strlist = r.text.split(',')
                                        intlist = []
                                        for ms in strlist:
                                           try:
                                               intlist.append(int(ms))
                                           except ValueError:
                                               pass
                                        valuelist.append(list(intlist))
                                        fvaluelist.append(list(intlist))
                                else:
                                    valuelist.append("")
                                    fvaluelist.append("")
                                    
                                    
                                      
                                
                                
                            for mt in mi.iter('mt'):
                                paramlist.append(mt.text)
                                fparamlist.append(mt.text)
                            par_val_list = zip(paramlist,valuelist)
                            par_val_dict = dict(par_val_list)
                            moid[mv.find('moid').text] = par_val_dict
                    
                    
                    
                    
                ts = mi.find('mts').text
                        #ts[mi.find('mts').text] = moid
                mdc[ts] = moid
                i = i + 1
                #with io.open('C:\PYTEST\data2.json', 'w', encoding='utf-8') as f:
                   # f.write(unicode(json.dumps(mdc, ensure_ascii=False)))
                #print fmoidlist
                df = pandas.DataFrame({'date':Series(fdatelist),
                                       'moid':Series(fmoidlist),
                                       'motype':Series(fmotypelist),
                                       'movalue':Series(fmovaluelist),             
                                       'parameters':Series(fparamlist),
                                       'values':Series(fvaluelist)                   
                                       })   
                
                
                    
                
                #dfmotype = df.groupby('motype').groups.keys()
                #df_grouped = df.groupby(['date','moid','motype','movalue','parameters','values']).size().reset_index(name='count')
                #df_nodate = df_grouped[['moid','parameters','values']]
                #dfpivoted = df_nodate.pivot(index='moid',columns='parameters',values='values')
                #==============================================================================
                # dfpivoted.reset_index(level=0,inplace=True)
                # pivdtelst = []
                # pivmtypelst = []
                # pivmvallst = []
                # for mos in dfpivoted['moid']:
                #     pivdtelst.append(fdatelist[0])
                #     mosplit = [mm.split('=') for mm in mos.split(',') ]
                #     pivmtypelst.append(mosplit[-1][0])
                #     pivmvallst.append(mosplit[-1][-1])
                # 
                # dfpivoted['date'] = Series(pivdtelst)
                # dfpivoted['motype'] = Series(pivmtypelst)
                # dfpivoted['movalue'] = Series(pivmvallst)
                # 
                # df_pmswitchingressdiscards = dfpivoted[dfpivoted['motype']=='RiLink'][['moid','pmLinkRestart','pmLinkDelayHigh']]
                #==============================================================================
                #print(type(df_pmswitchingressdiscards['pmSwitchIngressDiscards'].values))
                
                df_all = df_all.append(df)


        #dfsql = df
        #dfsql.columns = map(str.lower,dfsql.columns)
        #aaa = dfpivoted['motype']=='EutranCellFDD'
        #q = """Select moid from df_grouped where moid ='ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=LHI11025A11';"""
        #pmUeThpTimeDl = dfpivoted[dfpivoted['motype']=='EUtranCellFDD'][['date','movalue','pmUeThpTimeDl','pmPdcpVolDlDrb','pmPdcpVolDlDrblasttti','pmPdcpVolDlDrbtransum']]

        #print valuelist
        #print paramlist
        #print par_val_list
        #print par_val_dict
        #print ts
        #print ne
        #print mdc

        df_all_cluster = df_all[df_all['motype']=='EUtranCellFDD'][['date','parameters','motype','values']]
        df_all_cluster.loc[:,'moid'] = 'CLUSTER'
        df_all_cluster.loc[:,'movalue'] = 'CLUSTER'
        df_all_eutrancell = df_all[df_all['motype']=='EUtranCellFDD']
        df_all_aws = df_all_eutrancell.loc[df_all_eutrancell['movalue'].str[0]=='L']
        df_all_pcs = df_all_eutrancell.loc[df_all_eutrancell['movalue'].str[0]=='B']
        df_all_b12 = df_all_eutrancell.loc[df_all_eutrancell['movalue'].str[0]=='D']
        df_all_aws.loc[:,'movalue'] = 'AWS'
        df_all_aws.loc[:,'moid'] = 'AWS'
        df_all_pcs.loc[:,'movalue'] = 'PCS'
        df_all_pcs.loc[:,'moid'] = 'PCS'
        df_all_b12.loc[:,'movalue'] = 'B12'
        df_all_b12.loc[:,'moid'] = 'B12'
        df_all_cluster = df_all_cluster.append(df_all_aws)
        df_all_cluster = df_all_cluster.append(df_all_pcs)             
        df_all_cluster = df_all_cluster.append(df_all_b12)              
        df_all_cluster = df_all_cluster.append(df_all) 

                 
        cl_avgrrc_sum = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        #cluster_avgrrc_sum.columns = ['date','movalue','parameters','values']
        cluster_avgrrc_samp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSamp'].groupby(['date','movalue','parameters']).agg({'values':[np.sum]})
        cl_avgrrc = cl_avgrrc_sum['values'].values/180
        cluster_avgrrc_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_avgrrc = cluster_avgrrc_temp[['date','moid','motype','movalue']]
        df_cluster_avgrrc.loc[:,'values'] = cl_avgrrc
        df_cluster_avgrrc.loc[:,'parameters'] = 'AVG_RRC'


        #Event Level AVG_RRC
        df_event_avgrrc = df_cluster_avgrrc[df_cluster_avgrrc['parameters']=='AVG_RRC'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.mean]})
        df_event_avgrrc.columns = df_event_avgrrc.columns.get_level_values(0)

                     
        cl_dlvoldrb = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolDlDrb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        #cluster_avgrrc_sum.columns = ['date','movalue','parameters','values']
        cl_dlvolsrb = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolDlSrb'].groupby(['date','movalue','parameters']).agg({'values':[np.sum]})
        cluster_dlvol_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_dlvol = cluster_dlvol_temp[['date','moid','motype','movalue']]
        df_cluster_dlvol.loc[:,'values'] = (cl_dlvoldrb['values'].values + cl_dlvolsrb['values'].values)/(8*1024)
        df_cluster_dlvol.loc[:,'parameters'] = 'DL_TRAFFIC_VOL(MB)' 

        #Event level DL_TRAFFIC_VOL
        df_event_dlvol = df_cluster_dlvol[df_cluster_dlvol['parameters']=='DL_TRAFFIC_VOL(MB)'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        df_event_dlvol.columns = df_event_dlvol.columns.get_level_values(0)		

        cl_ulvoldrb = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolUlDrb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        #cluster_avgrrc_sum.columns = ['date','movalue','parameters','values']
        cl_ulvolsrb = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolUlSrb'].groupby(['date','movalue','parameters']).agg({'values':[np.sum]})
        cluster_ulvol_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_ulvol = cluster_ulvol_temp[['date','moid','motype','movalue']]
        df_cluster_ulvol.loc[:,'values'] = (cl_ulvoldrb['values'].values + cl_ulvolsrb['values'].values)/(8*1024)
        df_cluster_ulvol.loc[:,'parameters'] = 'UL_TRAFFIC_VOL(MB)'

        #Event Level UL_TRAFFIC_VOL
        df_event_ulvol = df_cluster_ulvol[df_cluster_ulvol['parameters']=='UL_TRAFFIC_VOL(MB)'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        df_event_ulvol.columns = df_event_ulvol.columns.get_level_values(0)		

        #print(df_cluster_ulvol)



        #df_avgrrc = df_all[df_all['parameters']=='pmRrcConnLevSum'][['date','moid','motype','movalue']]
        #df_avgrrc.loc[:,'values'] = df_all[df_all['parameters']=='pmRrcConnLevSum']['values'].values/df_all[df_all['parameters']=='pmRrcConnLevSamp']['values'].values
        #df_avgrrc.loc[:,'parameters'] = 'AVG_RRC'
        #
        #
        #
        #df_dlvol = df_all[df_all['parameters']=='pmRrcConnLevSum'][['date','moid','motype','movalue']]
        #df_dlvol.loc[:,'values'] = (df_all[df_all['parameters']=='pmPdcpVolDlDrb']['values'].values + df_all[df_all['parameters']=='pmPdcpVolDlSrb']['values'].values)/(8*1024)
        #df_dlvol.loc[:,'parameters'] = 'DL_TRAFFIC_VOL(MB)'
        #
        #df_ulvol = df_all[df_all['parameters']=='pmRrcConnLevSum'][['date','moid','motype','movalue']]
        #df_ulvol.loc[:,'values'] = (df_all[df_all['parameters']=='pmPdcpVolUlDrb']['values'].values + df_all[df_all['parameters']=='pmPdcpVolUlSrb']['values'].values)/(8*1024)
        #df_ulvol.loc[:,'parameters'] = 'UL_TRAFFIC_VOL(MB)'

        cl_prbavaildl = df_all_cluster[df_all_cluster['parameters']=='pmPrbAvailDl'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedDlBcch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlBcch'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedDlDtch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlDtch'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedDlFirstTrans = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlFirstTrans'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedDlPcch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlPcch'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_prbutildl = 100*(cl_pmPrbUsedDlBcch['values'].values + cl_pmPrbUsedDlDtch['values'].values + cl_pmPrbUsedDlFirstTrans['values'].values + cl_pmPrbUsedDlPcch['values'].values)/(cl_prbavaildl['values'].values)
        cluster_prbutildl_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_prbutildl = cluster_prbutildl_temp[['date','moid','motype','movalue']]
        df_cluster_prbutildl.loc[:,'values'] = cl_prbutildl
        df_cluster_prbutildl.loc[:,'parameters'] = 'PERC_PRB_UTIL_DL' 
                
                #Event level PERC_PRB_UTIL_DL
        event_prbavaildl = df_all_cluster[df_all_cluster['parameters']=='pmPrbAvailDl'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedDlBcch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlBcch'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedDlDtch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlDtch'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedDlFirstTrans = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlFirstTrans'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedDlPcch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedDlPcch'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_prbutildl = 100*(event_pmPrbUsedDlBcch['values'].values + event_pmPrbUsedDlDtch['values'].values + event_pmPrbUsedDlFirstTrans['values'].values + event_pmPrbUsedDlPcch['values'].values)/(event_prbavaildl['values'].values)
        event_prbutildl_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_prbutildl = event_prbutildl_temp[['movalue','motype','moid']]
        df_event_prbutildl.loc[:,'values'] = event_prbutildl
        df_event_prbutildl.loc[:,'parameters'] = 'PERC_PRB_UTIL_DL'
        print(df_event_prbutildl)


        cl_prbavailul = df_all_cluster[df_all_cluster['parameters']=='pmPrbAvailUl'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedUlDtch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedUlDtch'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPrbUsedUlSrb = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedUlSrb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_prbutilul = 100*(cl_pmPrbUsedUlDtch['values'].values + cl_pmPrbUsedUlSrb['values'].values)/(cl_prbavailul['values'].values)
        cluster_prbutilul_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_prbutilul = cluster_prbutilul_temp[['date','moid','motype','movalue']]
        df_cluster_prbutilul.loc[:,'values'] = cl_prbutilul
        df_cluster_prbutilul.loc[:,'parameters'] = 'PERC_PRB_UTIL_UL' 
                
                #Event level PERC_PRB_UTIL_UL
        event_prbavailul = df_all_cluster[df_all_cluster['parameters']=='pmPrbAvailUl'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedUlDtch = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedUlDtch'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmPrbUsedUlSrb = df_all_cluster[df_all_cluster['parameters']=='pmPrbUsedUlSrb'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_prbutilul = 100*(event_pmPrbUsedUlDtch['values'].values + event_pmPrbUsedUlSrb['values'].values)/(event_prbavailul['values'].values)
        event_prbutilul_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnLevSum'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_prbutilul = event_prbutilul_temp[['movalue','motype','moid']]
        df_event_prbutilul.loc[:,'values'] = event_prbutilul
        df_event_prbutilul.loc[:,'parameters'] = 'PERC_PRB_UTIL_UL'


        cl_pmPdcpVolDlDrb = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolDlDrb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmPdcpVolDlDrbLastTTI = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolDlDrbLastTTI'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmUeThpTimeDl = df_all_cluster[df_all_cluster['parameters']=='pmUeThpTimeDl'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_avg_ue_dlthr = 1000*(cl_pmPdcpVolDlDrb['values'].values - cl_pmPdcpVolDlDrbLastTTI['values'].values)/(cl_pmUeThpTimeDl['values'].values)
        cluster_avguedlthr_temp = df_all_cluster[df_all_cluster['parameters']=='pmPdcpVolDlDrb'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_avguedlthr = cluster_avguedlthr_temp[['date','moid','motype','movalue']]
        df_cluster_avguedlthr.loc[:,'values'] = cl_avg_ue_dlthr
        df_cluster_avguedlthr.loc[:,'parameters'] = 'AVG_UE_DL_THR(Kbps)' 
                
                #Event level AVG_UE_DL_THR(Kbps)
        df_event_avguedlthr = df_cluster_avguedlthr[df_cluster_avguedlthr['parameters']=='AVG_UE_DL_THR(Kbps)'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.mean]})
        df_event_avguedlthr.columns = df_event_avguedlthr.columns.get_level_values(0)

        cl_pmUeThpVolUl = df_all_cluster[df_all_cluster['parameters']=='pmUeThpVolUl'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmUeThpTimeUl = df_all_cluster[df_all_cluster['parameters']=='pmUeThpTimeUl'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_avg_ue_ulthr = 1000*(cl_pmUeThpVolUl['values'].values)/(cl_pmUeThpTimeUl['values'].values)
        cluster_avgueulthr_temp = df_all_cluster[df_all_cluster['parameters']=='pmUeThpVolUl'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_avgueulthr = cluster_avgueulthr_temp[['date','moid','motype','movalue']]
        df_cluster_avgueulthr.loc[:,'values'] = cl_avg_ue_ulthr
        df_cluster_avgueulthr.loc[:,'parameters'] = 'AVG_UE_UL_THR(Kbps)' 
                
                #Event level AVG_UE_UL_THR(Kbps)
        df_event_avgueulthr = df_cluster_avgueulthr[df_cluster_avgueulthr['parameters']=='AVG_UE_UL_THR(Kbps)'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.mean]})
        df_event_avgueulthr.columns = df_event_avgueulthr.columns.get_level_values(0)

        cl_pmRrcConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmRrcConnEstabAttReatt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAttReatt'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmRrcConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabSucc'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_rrc_fail = 100*(1 - (cl_pmRrcConnEstabSucc['values'].values)/(cl_pmRrcConnEstabAtt['values'].values -cl_pmRrcConnEstabAttReatt['values'].values ))
        cluster_rrcfail_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_rrcfail = cluster_rrcfail_temp[['date','moid','motype','movalue']]
        df_cluster_rrcfail.loc[:,'values'] = cl_rrc_fail
        df_cluster_rrcfail.loc[:,'parameters'] = 'RRC_FAILURE_RATE(%)' 
                
                #Event level RRC_FAILURE_RATE
        event_pmRrcConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmRrcConnEstabAttReatt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAttReatt'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmRrcConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabSucc'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_rrc_fail = 100*(1 - (event_pmRrcConnEstabSucc['values'].values)/(event_pmRrcConnEstabAtt['values'].values -event_pmRrcConnEstabAttReatt['values'].values ))
        event_rrcfail_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_rrcfail = event_rrcfail_temp[['movalue','motype','moid']]
        df_event_rrcfail.loc[:,'values'] = event_rrc_fail
        df_event_rrcfail.loc[:,'parameters'] = 'RRC_FAILURE_RATE(%)'

        cl_pmErabRelNormalEnb = df_all_cluster[df_all_cluster['parameters']=='pmErabRelNormalEnb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelMme = df_all_cluster[df_all_cluster['parameters']=='pmErabRelMme'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalEnb = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnb'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalEnbAct = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnbAct'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalMmeAct = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalMmeAct'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_erab_drop = 100*(cl_pmErabRelAbnormalEnbAct['values'].values + cl_pmErabRelAbnormalMmeAct['values'].values )/(cl_pmErabRelNormalEnb['values'].values + cl_pmErabRelMme['values'].values + cl_pmErabRelAbnormalEnb['values'].values )
        cluster_erabdrop_temp = df_all_cluster[df_all_cluster['parameters']=='pmErabRelNormalEnb'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_erabdrop = cluster_erabdrop_temp[['date','moid','motype','movalue']]
        df_cluster_erabdrop.loc[:,'values'] = cl_erab_drop
        df_cluster_erabdrop.loc[:,'parameters'] = 'ERAB_DROP_RATE(%)' 
                
                #Event level ERAB_DROP_RATE
        event_pmErabRelNormalEnb = df_all_cluster[df_all_cluster['parameters']=='pmErabRelNormalEnb'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelMme = df_all_cluster[df_all_cluster['parameters']=='pmErabRelMme'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalEnb = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnb'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalEnbAct = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnbAct'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalMmeAct = df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalMmeAct'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_erab_drop = 100*(event_pmErabRelAbnormalEnbAct['values'].values + event_pmErabRelAbnormalMmeAct['values'].values )/(event_pmErabRelNormalEnb['values'].values + event_pmErabRelMme['values'].values + event_pmErabRelAbnormalEnb['values'].values )
        event_erabdrop_temp = df_all_cluster[df_all_cluster['parameters']=='pmErabRelNormalEnb'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_erabdrop = event_erabdrop_temp[['movalue','motype','moid']]
        df_event_erabdrop.loc[:,'values'] = event_erab_drop
        df_event_erabdrop.loc[:,'parameters'] = 'ERAB_DROP_RATE(%)'


        qci1df_parameters = df_all_cluster[df_all_cluster['parameters']=='pmErabEstabSuccAddedQci']
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabRelNormalEnbQci'])
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabRelMmeQci'])
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnbQci'])
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalEnbActQci'])
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabRelAbnormalMmeActQci'])
        qci1df_parameters = qci1df_parameters.append(df_all_cluster[df_all_cluster['parameters']=='pmErabEstabAttAddedQci'])

        qci1zerodf = qci1df_parameters[qci1df_parameters['values']==0]
        qci1nonzerodf = qci1df_parameters[qci1df_parameters['values']!=0]
        vltecalls = []
        for qcis in qci1nonzerodf['values'].values:
                if qcis[1] == 1:
                        vltecalls.append(qcis[2])
                else: vltecalls.append(0)

        qci1nonzerodf.loc[:,'values'] = vltecalls
        qci1df = pandas.DataFrame()
        qci1df = qci1df.append(qci1zerodf)
        qci1df = qci1df.append(qci1nonzerodf)


        cl_vltecalls_sum = qci1df[qci1df['parameters']=='pmErabEstabSuccAddedQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_vltecalls = cl_vltecalls_sum['values'].values
        cluster_vltecalls_temp = qci1df[qci1df['parameters']=='pmErabEstabSuccAddedQci'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_vltecalls = cluster_vltecalls_temp[['date','moid','motype','movalue']]
        df_cluster_vltecalls.loc[:,'values'] = cl_vltecalls
        df_cluster_vltecalls.loc[:,'parameters'] = 'VOLTE_CALLS' 
                
                #Event level VOLTE_CALLS
        df_event_vltecalls = df_cluster_vltecalls[df_cluster_vltecalls['parameters']=='VOLTE_CALLS'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        df_event_vltecalls.columns = df_event_vltecalls.columns.get_level_values(0)
                
                
                

        cl_pmErabRelNormalEnbQci = qci1df[qci1df['parameters']=='pmErabRelNormalEnbQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelMmeQci = qci1df[qci1df['parameters']=='pmErabRelMmeQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalEnbQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalEnbQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalEnbActQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalEnbActQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmErabRelAbnormalMmeActQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalMmeActQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_vlte_drop = 100*(cl_pmErabRelAbnormalEnbActQci['values'].values + cl_pmErabRelAbnormalMmeActQci['values'].values )/(cl_pmErabRelNormalEnbQci['values'].values + cl_pmErabRelMmeQci['values'].values + cl_pmErabRelAbnormalEnbQci['values'].values )
        cluster_vltedrop_temp = qci1df[qci1df['parameters']=='pmErabRelNormalEnbQci'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_vltedrop = cluster_vltedrop_temp[['date','moid','motype','movalue']]
        df_cluster_vltedrop.loc[:,'values'] = cl_vlte_drop
        df_cluster_vltedrop.loc[:,'parameters'] = 'VOLTE_DROP_RATE(%)' 
                
                #Event level VOLTE_DROP_RATE
        event_pmErabRelNormalEnbQci = qci1df[qci1df['parameters']=='pmErabRelNormalEnbQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelMmeQci = qci1df[qci1df['parameters']=='pmErabRelMmeQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalEnbQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalEnbQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalEnbActQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalEnbActQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmErabRelAbnormalMmeActQci = qci1df[qci1df['parameters']=='pmErabRelAbnormalMmeActQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_vlte_drop = 100*(event_pmErabRelAbnormalEnbActQci['values'].values + event_pmErabRelAbnormalMmeActQci['values'].values )/(event_pmErabRelNormalEnbQci['values'].values + event_pmErabRelMmeQci['values'].values + event_pmErabRelAbnormalEnbQci['values'].values )
        event_vltedrop_temp = qci1df[qci1df['parameters']=='pmErabRelNormalEnbQci'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_vltedrop = event_vltedrop_temp[['movalue','motype','moid']]
        df_event_vltedrop.loc[:,'values'] = event_vlte_drop
        df_event_vltedrop.loc[:,'parameters'] = 'VOLTE_DROP_RATE(%)' 
                
                


        cl_pmRrcConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmRrcConnEstabAttReatt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAttReatt'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmRrcConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabSucc'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_rrc_succ_ratio = (cl_pmRrcConnEstabSucc['values'].values)/(cl_pmRrcConnEstabAtt['values'].values -cl_pmRrcConnEstabAttReatt['values'].values )
        cl_pmS1SigConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmS1SigConnEstabAtt'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_pmS1SigConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmS1SigConnEstabSucc'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_s1_succ_ratio = (cl_pmS1SigConnEstabSucc['values'].values)/(cl_pmS1SigConnEstabAtt['values'].values)
        cl_vlte_succ_sum = qci1df[qci1df['parameters']=='pmErabEstabSuccAddedQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_vlte_succ = cl_vlte_succ_sum['values'].values
        cl_vlte_att_sum = qci1df[qci1df['parameters']=='pmErabEstabAttAddedQci'].groupby(['date','movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        cl_vlte_att = cl_vlte_att_sum['values'].values
        cl_vlte_succ_ratio = (cl_vlte_succ)/(cl_vlte_att)
        cl_vlte_afr = 100*(1-(cl_vlte_succ_ratio*cl_s1_succ_ratio*cl_rrc_succ_ratio))
        cluster_vlteafr_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['date','movalue','motype','moid'],as_index=False).count()
        df_cluster_vlteafr = cluster_vlteafr_temp[['date','moid','motype','movalue']]
        df_cluster_vlteafr.loc[:,'values'] = cl_vlte_afr
        df_cluster_vlteafr.loc[:,'parameters'] = 'VOLTE_AFR(%)' 
        #print(cl_rrc_succ_ratio)
                
        #Event level VOLTE_AFR
        event_pmRrcConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmRrcConnEstabAttReatt = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAttReatt'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmRrcConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabSucc'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_rrc_succ_ratio = (event_pmRrcConnEstabSucc['values'].values)/(event_pmRrcConnEstabAtt['values'].values -event_pmRrcConnEstabAttReatt['values'].values )
        event_pmS1SigConnEstabAtt = df_all_cluster[df_all_cluster['parameters']=='pmS1SigConnEstabAtt'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_pmS1SigConnEstabSucc = df_all_cluster[df_all_cluster['parameters']=='pmS1SigConnEstabSucc'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_s1_succ_ratio = (event_pmS1SigConnEstabSucc['values'].values)/(event_pmS1SigConnEstabAtt['values'].values)
        event_vlte_succ_sum = qci1df[qci1df['parameters']=='pmErabEstabSuccAddedQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_vlte_succ = event_vlte_succ_sum['values'].values
        event_vlte_att_sum = qci1df[qci1df['parameters']=='pmErabEstabAttAddedQci'].groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        event_vlte_att = event_vlte_att_sum['values'].values
        event_vlte_succ_ratio = (event_vlte_succ)/(event_vlte_att)
        event_vlte_afr = 100*(1-(event_vlte_succ_ratio*event_s1_succ_ratio*event_rrc_succ_ratio))
        event_vlteafr_temp = df_all_cluster[df_all_cluster['parameters']=='pmRrcConnEstabAtt'].groupby(['movalue','motype','moid'],as_index=False).count()
        df_event_vlteafr = event_vlteafr_temp[['movalue','motype','moid']]
        df_event_vlteafr.loc[:,'values'] = event_vlte_afr
        df_event_vlteafr.loc[:,'parameters'] = 'VOLTE_AFR(%)'
                
                

           
        df_graph = pandas.DataFrame()
        #df_graph = df_graph.append(df_avgrrc)
        df_graph = df_graph.append(df_cluster_avgrrc)
        #df_graph = df_graph.append(df_dlvol)
        df_graph = df_graph.append(df_cluster_dlvol)
        #df_graph = df_graph.append(df_ulvol)
        df_graph = df_graph.append(df_cluster_ulvol)
        df_graph = df_graph.append(df_cluster_prbutildl)
        df_graph = df_graph.append(df_cluster_prbutilul)
        df_graph = df_graph.append(df_cluster_avguedlthr)
        df_graph = df_graph.append(df_cluster_avgueulthr)
        df_graph = df_graph.append(df_cluster_rrcfail)
        df_graph = df_graph.append(df_cluster_erabdrop)
        df_graph = df_graph.append(df_cluster_vltecalls)
        df_graph = df_graph.append(df_cluster_vltedrop)
        df_graph = df_graph.append(df_cluster_vlteafr)
        #print(df_dlvol)
        #dfmovalue = 
        #dfparameters =
        #dfvalues =          
        #df_graph.to_csv('test16.csv', sep=',', encoding='utf-8') 
        df_all_cluster.to_csv('test17.csv', sep=',', encoding='utf-8') 
        #writer = pandas.ExcelWriter('uploads/test2.xlsx', engine='xlsxwriter')
        #df_graph.to_excel(writer, sheet_name='Sheet1')
        #writer.save()
        #insertdb()
        
        spath = os.path.join(app.config['STATIC_FOLDER'],username)
        avgrrcpath = spath + "/cluster_avgrrc.csv"
        dlvol  = spath + "/cluster_dlvol.csv"
        ulvol  = spath + "/cluster_ulvol.csv"
        prbutildl  = spath + "/cluster_prbutildl.csv"
        prbutilul  = spath + "/cluster_prbutilul.csv"
        avguedlthr  = spath + "/cluster_avguedlthr.csv"
        avgueulthr  = spath + "/cluster_avgueulthr.csv"
        rrcfail  = spath + "/cluster_rrcfail.csv"
        erabdrop  = spath + "/cluster_erabdrop.csv"
        vltecalls  = spath + "/cluster_vltecalls.csv"
        vltedrop  = spath + "/cluster_vltedrop.csv"
        vlteafr  = spath + "/cluster_vlteafr.csv"
            
        df_cluster_avgrrc.to_csv(avgrrcpath, sep=',', encoding='utf-8')
        df_cluster_dlvol.to_csv(dlvol, sep=',', encoding='utf-8')
        df_cluster_ulvol.to_csv(ulvol, sep=',', encoding='utf-8')
        df_cluster_prbutildl.to_csv(prbutildl, sep=',', encoding='utf-8')
        df_cluster_prbutilul.to_csv(prbutilul, sep=',', encoding='utf-8')
        df_cluster_avguedlthr.to_csv(avguedlthr, sep=',', encoding='utf-8')
        df_cluster_avgueulthr.to_csv(avgueulthr, sep=',', encoding='utf-8')
        df_cluster_rrcfail.to_csv(rrcfail, sep=',', encoding='utf-8')
        df_cluster_erabdrop.to_csv(erabdrop, sep=',', encoding='utf-8')
        df_cluster_vltecalls.to_csv(vltecalls, sep=',', encoding='utf-8')
        df_cluster_vltedrop.to_csv(vltedrop, sep=',', encoding='utf-8')
        df_cluster_vlteafr.to_csv(vlteafr, sep=',', encoding='utf-8')


        #Create the CSV to download for the user as, here taking the date of max value  for avgRRC
        df_all_new = df_all_new.append(df_cluster_avgrrc)
        df_all_new = df_all_new.append(df_cluster_dlvol)
        df_all_new = df_all_new.append(df_cluster_ulvol)
        df_all_new = df_all_new.append(df_cluster_prbutildl)
        df_all_new = df_all_new.append(df_cluster_prbutilul)
        df_all_new = df_all_new.append(df_cluster_avguedlthr)
        df_all_new = df_all_new.append(df_cluster_avgueulthr)
        df_all_new = df_all_new.append(df_cluster_rrcfail)
        df_all_new = df_all_new.append(df_cluster_erabdrop)
        df_all_new = df_all_new.append(df_cluster_vltecalls)
        df_all.new = df_all_new.append(df_cluster_vlteafr)
        df_all_new['values'].astype(float);
        #Select the maxval from the AVGRRC
        maxval = df_cluster_avgrrc['values'].max()
        df_select_row = df_cluster_avgrrc.loc[df_cluster_avgrrc['values']==maxval]
        maxvaldate = df_select_row['date'].values

        df_y = df_all_new[df_all_new['date'].values==df_select_row['date'].values][['movalue','parameters','values']]
        df_y = df_y.rename(columns = {'values':'ROP_LEVEL'})
        df_y = np.around(df_y, 2)
        #print(df_y)
        #df_y.round(2)
        #print(df_select)
        #df_all_agg = df_all_new.groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        #df_all_avg = df_all_agg['values'].values;
        #df_select['aggregate']=df_all_avg

        #df_all_agg = df_all_new.groupby(['movalue','parameters'],as_index=False).agg({'values':[np.sum]})
        df_all_new1 = df_all_new1.append(df_event_avgrrc)
        df_all_new1 = df_all_new1.append(df_event_dlvol)
        df_all_new1 = df_all_new1.append(df_event_ulvol)
        df_all_new1 = df_all_new1.append(df_event_prbutildl)
        df_all_new1 = df_all_new1.append(df_event_prbutilul)
        df_all_new1 = df_all_new1.append(df_event_avguedlthr)
        df_all_new1 = df_all_new1.append(df_event_avgueulthr)
        df_all_new1 = df_all_new1.append(df_event_rrcfail)
        df_all_new1 = df_all_new1.append(df_event_erabdrop)
        df_all_new1 = df_all_new1.append(df_event_vltecalls)
        df_all_new1 = df_all_new1.append(df_event_vlteafr)
        df_all_new1 = df_all_new1.append(df_event_vltedrop)
        #df_all_avg1 = df_all_new1['values'].values;
        #df_z['aggregate']= df_all_new1['values'].values;
        #np.around(df_all_new1['values'], 0)
        df_z = df_all_new1[['movalue','parameters','values']]
        df_z = df_z.rename(columns = {'values':'EVENT_LEVEL'})
        df_z = np.around(df_z, 2)
        
        #df_z.aggregate = df_z.aggregate.round(2)

        #result = pandas.merge(df_z, df_y)
        #df_y.values = df_y.values.round(2)
        #df_z.aggregate = df_z.aggregate.round(2)
        #df_z.round(2)
        #result = pandas.concat([df_z, df_y])
        #result = pandas.concat([df_z, df_y],join='outer')
        result = pandas.merge(df_z, df_y)
        #result = pandas.concat([df_y, df_z], axis=1)
        #result['aggregate']=df_all_avg1
        #df_all_avg1 = df_all_new1.groupby(["movalue", "parameter"]).values
        #df_all_avg = df_all_new1.groupby(["movalue", "parameters"] , as_index = False).select("values")
        print(result)
        #print()
        #rpath = os.path.join(app.config['REDDY_FOLDER'],username)
        dfile = spath + "/download.csv"
        result.to_csv(dfile, sep=',', encoding='utf-8')


        return 1


def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])


    

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def insertdb():
    cur = get_db().cursor()
    workbook = xlrd.open_workbook('uploads/test2.xlsx')
    #open first sheet of the workbook which we find at index 0
    worksheet = workbook.sheet_by_index(0)
    # use to track the rows
    number_of_rows = worksheet.nrows
    #use to track the columns
    number_of_columns = worksheet.ncols
    rows = []
    #declare dictionary
    mydata = {}
    #We need to track the rows count till what it should run the loop
    for row in range(1, number_of_rows):
        #date  = (worksheet.cell(row,1).value)
        date  = datetime.datetime.strptime((worksheet.cell(row,1).value)[0:4]+ (worksheet.cell(row,1).value)[4:6] + (worksheet.cell(row,1).value)[6:8] + (worksheet.cell(row,1).value)[8:10]+ (worksheet.cell(row,1).value)[10:12] + (worksheet.cell(row,1).value)[12:14], '%Y%m%d%H%M%S')
        moid = (worksheet.cell(row,2).value)
        motype = (worksheet.cell(row,3).value)
        movalue = (worksheet.cell(row,4).value)
        value = (worksheet.cell(row,5).value)
        parameter = (worksheet.cell(row,6).value)
        val = str(value).split(",")
        for v in val:
            #print(v)
            result = execute_query("""SELECT id,value FROM testdf  WHERE date = ? AND movalue = ? """,(date,movalue))
            if result:
                print (result)
            else:
                cur.execute("""INSERT INTO testdf (date,moid,motype,movalue,parameters,value) VALUES (?, ?, ?, ?, ?, ?);""",(date, moid, motype, movalue, parameters, v))
                get_db().commit()

    cur.close
            
    


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM testdf""")
    return '<br>'.join(str(row) for row in rows)


@app.route("/schema")
def view_schema():
    return '<br>'.join(str(row) for row in execute_query("""pragma table_info('testdf')"""))

                       
@app.route("/print_data", methods = ['POST', 'GET'])
def print_data():
    cur = get_db().cursor();
    if request.args.get('parameters') or request.args.get('date') or request.args.get('movalue'):
        date =   request.args.get('date')
        movalue = request.args.get('movalue')
        parameters=request.args.get('parameters')
        if parameters == 'ALL' and date != 'ALL' and movalue != 'ALL': #011
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE date =? and movalue = ?""",(date,movalue))
        elif parameters != 'ALL' and date == 'ALL' and movalue != 'ALL': #101
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters =? and movalue = ?""",(parameters,movalue))
        elif parameters != 'ALL' and date != 'ALL' and movalue == 'ALL': #110
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters = ? and date = ?""",(parameters,date))
            print (result)
        elif parameters != 'ALL' and date == 'ALL' and movalue == 'ALL': #100
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters = ?""",(parameters,))
        elif parameters == 'ALL' and date != 'ALL' and movalue == 'ALL': #010
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE date = ?""",(date,))
        elif parameters == 'ALL' and date == 'ALL' and movalue != 'ALL': #001
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE movalue = ?""",(movalue,))
        elif parameters != 'ALL' and date != 'ALL' and movalue != 'ALL': #111
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters= ? and date = ? and movalue = ?""",(parameters, date, movalue))
        else:
            result = execute_query("""SELECT date, movalue, value, parameters FROM testdf""")
        
            
   # elif request.args.get('parameters') and request.args.get('date'):
    #    date =   request.args.get('date')
     #   parameters=request.args.get('parameters')
      #  result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters = ? and date =?""",(parameters,date))
   # elif request.args.get('parameters') and request.args.get('movalue'):
    #    movalue =   request.args.get('movalue')
     #   parameters=request.args.get('parameters')
      #  result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE parameters = ? and movalue =?""",(parameters,movalue))
    #elif request.args.get('date') and request.args.get('movalue'):
     #   movalue =   request.args.get('movalue')
      #  date =request.args.get('date')
      #  result = execute_query("""SELECT date, movalue, value, parameters FROM testdf WHERE date = ? and movalue =?""",(date,movalue))
    #elif  request.args.get('parameters'):
        
    #else:
        #result = execute_query("""SELECT date, movalue, value, parameters FROM testdf""")
    #and request.args.get('date'):
     #   movalue = request.args.get('movalue')
      #  date = request.args.get('date')
    #else:
     #   movalue = ""
      #  date = ""
    
    
    #result = execute_query("""SELECT value FROM testdf""")
    #print(result)
    str_rows = [','.join(map(str,row)) for row in result]
    
    header = 'date,movalue,value,parameters\n'
  
    return header + '\n'.join(str_rows)


@app.route("/upload", methods = ['POST'])
def upload():
    uploaded_files=request.files.getlist("file[]")
    #username = request.form['username']
    username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    session['username'] = username
    #path = os.path.dirname(os.path.abspath(__file__)) + "/uploads/" + username
    path = app.config['UPLOAD_FOLDER'] + username;
    spath = app.config['STATIC_FOLDER'] + username;
    
    print(path)
    if not os.path.isdir(path):
        os.mkdir(path)
        os.mkdir(spath)
    if os.path.isdir(path):
        path = path + "/"
        print("directory created\n\n")
    
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        print(file)
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(path, filename))
            if os.path.isfile(os.path.join(path,filename)):
                print("File Saved \n")
            # Save the filename into a list, we'll use it later
            filenames.append(filename)

    flag = xmltocsv(session['username'])
    
    session['flag'] = flag
    return render_template('index.html', session=session);
        

@app.route("/graph", methods = ['GET'])
def graph():
    path = os.path.join(app.config['STATIC_FOLDER'],session['username'])
    for fname in os.listdir(path):
        if fname and allowed_file(fname)and fname != 'download.csv':
            sessionparam.append(fname)
    return render_template('graph-rithvik.html',parameters=sessionparam, session=session)

@app.route("/test2", methods = ['GET'])
def test2():
    path = os.path.join(app.config['STATIC_FOLDER'],session['username'])
    session['filename']="download.csv"
    for fname in os.listdir(path):
        if  fname == 'download.csv':
            session['filename']=fname;
            
    return render_template('test2.html',session=session)

@app.route("/home")
def home():
    if session['username']:
        spath = os.path.join(app.config['STATIC_FOLDER'],session['username'])
        path = os.path.join(app.config['UPLOAD_FOLDER'],session['username'])
        if os.path.isdir(path):
            shutil.rmtree(path)
            shutil.rmtree(spath)
        session.pop('username')
        session.pop('flag')
        return redirect(url_for('index'))

@app.route("/", methods = ['GET'])
def index():
    flag=0;
    #if session['username']:
        #spath = os.path.join(app.config['STATIC_FOLDER'],session['username'])
        #path = os.path.join(app.config['UPLOAD_FOLDER'],session['username'])
        #if os.path.isdir(path):
            #shutil.rmtree(path)
            #shutil.rmtree(spath)
        #session.pop('username')
        #session.pop('flag')
        
        
   # rows = execute_query("""SELECT distinct parameters FROM testdf""")
    #print(rows)
   # for fname in os.listdir(app.config['STATIC_FOLDER']):
    #    if fname and allowed_file(fname):
     #       sessionparam.append(fname)
       
   # return render_template('index5.html', parameters=sessionparam)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
