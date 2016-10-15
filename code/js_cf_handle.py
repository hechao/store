#! /usr/bin/python
#-*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
from csv_handle import csv_readlist, csv_writelist

def raw_data(funda_url):
    funda_lst = []
    page = urlopen(funda_url)
    soup = BeautifulSoup(page, "lxml")
    
    soup = soup.p.string # element tag, remove html
    null = ''
    soup = eval(soup)
    rows_str = json.dumps(soup['rows'],indent=1, encoding="UTF-8", ensure_ascii=False)
    #rows_str =unicode.encode(rows_str,'utf-8')
    funda_list=json.loads(rows_str)
    #print type(funda_list[0])
    #print funda_list[0]
    for i in funda_list:
        funda_lst.append(i[u'cell'])
    #for j in funda_lst:
        #print j[u'funda_profit_rt_next']
    #print funda_lst
    return funda_lst

def filter_d(funda_lst):
    nlst = []
    for i in funda_lst:
        temp_dic = {}
        tSID = i[u'fund_id']
        temp_dic['disct'] =  i[u'annualize_dscnt_rt']
        if tSID[0] == '1':
            temp_dic['tSID'] = 'SZ'+tSID
        elif tSID[0] == '5':
            temp_dic['tSID'] = 'SH'+tSID
        nlst.append(temp_dic)
    return nlst
    
def dict_update(file, file_path, nlst):
    old_d = csv_readlist(file, file_path)
    for i in nlst:
        for j in old_d:
            if i['tSID'] == j['SID']:
                j['disct'] = i['disct']
            #print j
    
    #print old_d            
    csv_writelist(file, file_path, old_d)  
                
        
    

def filter_data(funda_raw_data):
    filter_data_tmp = []
    for i in funda_raw_data:
        rate = float(i[u'funda_profit_rt_next'][:-1])
        volumn = float(i[u'funda_volume'])
        if rate >= 5 and volumn >= 100:
            #print i[u'funda_id']
            filter_data_tmp.append(i)
    #print funda_fdata
    return funda_fdata
    
def funda_fcode(funda_fdata):
    funda_fcode =[]
    for i in funda_fdata:
        l = {}
        volumn = float(i[u'funda_volume'])
        rate = float(i[u'funda_profit_rt_next'][:-1])
        tSID = i[u'funda_id']
        tname = i[u'funda_name']
        name = tname.decode("unicode-escape").encode("utf-8")
        
        if tSID[0] == '1':
            SID = 'SZ' + tSID
        l['SID'] =SID
        l['rate'] =rate
        l['volumn'] =volumn
        l['cname'] = name
        #print name
        #l['cname'] = i[u'funda_name']
        funda_fcode.append(l)
    return funda_fcode

    
    
def funda_raw(funda_url):
    page = urlopen(funda_url)
    soup = BeautifulSoup(page, from_encoding="utf8")
    
    soup = soup.p.string # element tag, remove html
    null = ''
    soup = eval(soup)
    rows_str = json.dumps(soup['rows'],indent=1)
    funda_list=json.loads(rows_str)
    #print rows_str
    #print type(rows_str)
    
    funda_raw ={}

    for cells in funda_list:
        funda_data = cells[u'cell']
        
        funda_name = funda_data[u'funda_name'].decode('unicode_escape')
        funda_discount = float(funda_data[u'funda_discount_rt'][:-1])
        funda_profit = float(funda_data[u'funda_profit_rt_next'][:-1])
        if funda_data[u'funda_base_est_dis_rt'] == '-':
            print "error to read funda_base_est_dis_rt as -, set it to -999.00"
            funda_base_profit = -999.00
        else:
            funda_base_profit = float(funda_data[u'funda_base_est_dis_rt'][:-1])
        funda_raw[funda_name] =[funda_discount, funda_profit, funda_base_profit]
    
    return funda_raw

def funda(funda_raw, discount, profit, base_profit):
    
    funda = {}
    
    for i in funda_raw:
        if funda_raw[i][0]>=discount and funda_raw[i][1]>=profit and funda_raw[i][2]<=base_profit:
            #print i
            funda[i] = funda_raw[i]
    return funda

    
if __name__ == "__main__":
    funda_url = 'https://www.jisilu.cn/data/cf/cf_list/'
    file = 'uncategory_data.csv'
    file_path = '/srv/www/idehe.com/store/stock_data/'
    
    funda_rawdata = raw_data(funda_url)
    nlst = filter_d(funda_rawdata)
    dict_update(file, file_path, nlst)
    
    
    
    
    
    