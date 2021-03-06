#! /usr/bin/python
#-*- encoding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from csv_handle import csv_readlist, csv_writelist
from xq_handle import data_get, select_data, data_get_index, select_data_index

from google_data import data_filter, gfile_check

def grab_data(ifile, file_path):
    is_lis_dic = csv_readlist(ifile, file_path)
    for i in is_lis_dic:
        sdict = data_get(i['SID'])
        fine_data = select_data(sdict)
        i.update(fine_data)
    return is_lis_dic

def grab_data_index(ifile, file_path):
    is_lis_dic = csv_readlist(ifile, file_path)
    for i in is_lis_dic:
        sdict = data_get_index(i['SID'])
        fine_data = select_data_index(sdict)
        i.update(fine_data)
    return is_lis_dic

def data_range(is_lis_dic):
    for i in is_lis_dic:
        #print type(i['jk'])
        cur_price = float(i['current_price'][1:])
        KL = float(i['52KL'])
        KH = float(i['52KH'])
        cal_tmp = (cur_price-KL)/(KH-KL)
        print cal_tmp
        i['range'] = round(cal_tmp*100,2)
    basedata = csv_readlist('basedata.csv', "/srv/www/idehe.com/store/stock_data/")
    for u in is_lis_dic:
        for j in basedata:
            if u['SID'] == j['SID']:
                u.update(j)
    #print is_lis_dic
    return is_lis_dic

def data_range_index(is_lis_dic, g_path, avg_range):
    
    for e in is_lis_dic:
        #print type(i['jk'])
        cur_price = float(e['current_price'])
        KL = float(e['52KL'])
        KH = float(e['52KH'])
        cal_tmp = (cur_price-KL)/(KH-KL)
        #print cal_tmp
        e['range'] = round(cal_tmp*100,2)
        
    basedata = csv_readlist('basedata.csv', "/srv/www/idehe.com/store/stock_data/")
    
    for u in is_lis_dic:
        for j in basedata:
            if u['SID'] == j['SID']:
                u.update(j)
                
    for i in is_lis_dic:
        SID = i['SID']
        check = gfile_check(SID, g_path)
        data_f = data_filter(SID, g_path, avg_range)
        if check == True:
            i['hist_H'] = data_f[0]
            i['hist_L'] = data_f[1]
            i['90_avg'] = data_f[2]
            avg_compare = round((float(i['current_price'])-i['90_avg'])/float(i['current_price'])*100,2)
            i['avg_compr'] = '%s%%' % avg_compare
    for i in is_lis_dic:
        cal_tmp = (float(i['current_price'])-float(i['hist_L']))/(float(i['hist_H'])-float(i['hist_L']))
        i['hist_range'] = round(cal_tmp*100,2)
    return is_lis_dic    

def data_mhandle(infile, outfile, file_path):
    grabed_data = grab_data(infile, file_path)
    data_ranged = data_range(grabed_data)
    csv_writelist(outfile, file_path, data_ranged)
    
def data_mhandle_index(infile, outfile, file_path, g_path, avg_range):
    grabed_data = grab_data_index(infile, file_path)
    #data_ranged = data_range(grabed_data)
    data_ranged_index = data_range_index(grabed_data, g_path, avg_range)    
    csv_writelist(outfile, file_path, data_ranged_index)

    
if __name__ == "__main__":
    ifile = "index.csv"
    ofile = "index_data.csv"
    g_path = '/srv/www/idehe.com/store/stock/'
    
    ifile2 = "ETF.csv"
    ofile2 = "ETF_data.csv"
    
    file_path = "/srv/www/idehe.com/store/stock_data/"
    
    data_mhandle_index(ifile, ofile, file_path, g_path)
    #data_mhandle(ifile2, ofile2, file_path)
    #data_mhandle(etf_ifile, etf_ofile, file_path)   #etf
    #data_mhandle(funda_ifile, funda_ofile, file_path)   #funda
    
    