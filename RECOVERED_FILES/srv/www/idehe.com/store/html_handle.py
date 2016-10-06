# -*- coding: utf-8 -*- 
from html import HTML

def html(html_body):
    html_header ="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>This is my stock manager!</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    </head>
    <body>
    %s
    </body>
    </html>""" % (html_body)
    return html_header

def page_layout(page_desc, stock_list, col1, col2, col3, lsfilter, chg_lsfilter, ext, storepic):
    layout = """
    <div class="container">
        <div class="row clearfix">
    		<div class="col-md-12 column">
    		%s
    		</div>
    	</div>
    	
    	<div class="row clearfix">
    		<div class="col-md-4 column">
    		%s
    		</div>
    		<div class="col-md-4 column">
    		%s
    		</div>
    		<div class="col-md-4 column">
    		%s
    		</div>
	    </div>

    	<div class="row clearfix">
    		<div class="col-md-4 column">
    		%s
    		</div>
    		<div class="col-md-4 column">
    		%s
    		</div>
    		<div class="col-md-4 column">
    		%s
    		</div>
	    </div>	    
        <div class="row clearfix">
    		<div class="col-md-12 column">
    		%s
    		</div>
    	</div>	    
	    
	    <div class="row clearfix">
		<div class="col-md-4 column">
			<img alt="140x140" src=%s />
		</div>
		<div class="col-md-4 column">
		reserve...
		</div>
		<div class="col-md-4 column">
		reserve...
		</div>
		
	</div>
	</div>
    """ % (page_desc, col1, col2, col3, lsfilter, chg_lsfilter, ext, stock_list, storepic)
    
    return layout


def page_desciption():
    page_desc = HTML()
    page_desc.h2("Welcome!")
    l = page_desc.ol
    l.li('This is the store of all my stocks! thanks for visiting!')
    l.li('VER:1.0, next design: ')
    l.li('买入位对比更新位置')
    l.li('自动更新市价，52K最低')
    l.li('Post FORM 中文化-搞定， 新增证券-搞定')
    return str(page_desc)
    
def html_stock_list(stock_data):
    stock_list = HTML()
    stock_list.h2("持仓一览！")
    t = stock_list.table(border='2px', width ='70%', klass ='table table-bordered')
    t.th('ID')
    t.th('名称')
    t.th('状态')
    t.th('分组')
    t.th('52W-L')
    t.th('52W-P')
    t.th('52K区间')
    t.th('市价')
    t.th('市价/目标价比')
    t.th('目标价')
    t.th('我的价格')
    t.th('份额')
    t.th('市值')
    t.th('仓位')
    t.th('Update')
    
    ratio_list =[]
    
    for i in stock_data:
        ratio_list.append(i['lh_ratio'])
    
    ratio_list_sorted = sorted(ratio_list)
    
    #print ratio_list_sorted
    
    for j in ratio_list_sorted:
        
        for i in stock_data:
            if i['lh_ratio'] == j:
                r = t.tr
                r.td(str(i['code']))
                r.td(str(i['name']))
                r.td(str(i['status']))
                r.td(str(i['group']))
                r.td(str(i['low52week']))
                r.td(str(i['high52week']))
                if i['lh_ratio'] is not "":
                    r.td.b("%.2f %%" % (float(i['lh_ratio'])*100.0))
                else:
                    r.td("")
                r.td(str(i['current']))
                if float(i['target_ratio'])*100 <= 10 and float(i['target_ratio'])*100 !=0:
                    r.td.b("%.2f %%" % (float(i['target_ratio'])*100.0))
                else:
                    r.td("%.2f %%" % (float(i['target_ratio'])*100.0))
                r.td(str(i['target']))
                r.td(str(i['cost']))
                r.td(str(i['share']))
                r.td(str(i['value']))
                r.td("%.2f %%" % (float(i['store'])*100.0))
                r.td("%s(%s)" % (str(i['time']), str(i['update_date'])))
        
    return str(stock_list)
   
    
def html_table_setprice(dir):
    h = HTML()
    h.h3("更新目标价")
    #webform = h.form
    f = h.form(action=dir, method="post")
    
    f.p("Code: ")
    f.input(type="text", name= "code")
    f.br
    
    f.p("Target: ")
    f.input(type="text", name= "target")
    f.br
    
    f.input(type="submit", name= "submit")
    f.br
    return str(h)
    
def html_table_filter(dir):
    h = HTML()
    h.h3("过滤分组")
    #webform = h.form
    f = h.form(action=dir, method="post")
    
    f.p("Group: ")
    f.input(type="text", name= "group")
    f.br
    
    f.input(type="submit", name= "submit")
    f.br
    return str(h)
    
def html_table_chg_filter(dir):
    h = HTML()
    h.h3("修改属性")
    #webform = h.form
    f = h.form(action=dir, method="post")

    f.p("Code: ")
    f.input(type="text", name= "code")
    f.br
    
    f.p("Key: ")
    f.input(type="text", name= "key")
    f.br
    
    f.p("Value: ")
    f.input(type="text", name= "value")
    f.br
    
    f.input(type="submit", name= "submit")
    f.br
    return str(h)
    
def html_table_setshare(dir):
    h = HTML()
    h.h3("更新我的库存:  ")
    #webform = h.form
    f = h.form(action=dir, method="post")

    f.p("code: ")
    f.input(type="text", name= "code")
    f.br
    
    f.p("Share： ")
    f.input(type="text", name= "share")
    f.br
    
    f.input(type="submit", name= "submit")
    f.br
    return str(h)
    
def html_table_setcost(dir):
    h = HTML()
    h.h3("更新我的买入价:  ")
    #webform = h.form
    f = h.form(action=dir, method="post")

    f.p("Code: ")
    f.input(type="text", name= "code")
    f.br
    
    f.p("Cost： ")
    f.input(type="text", name= "cost")
    f.br
    
    f.input(type="submit", name= "submit")
    f.br
    return str(h) 
    
def html_table_addnew(dir):
    h = HTML()
    h.h3("添加新的股票： ")
    #webform = h.form
    f = h.form(action=dir, method="post")
    
    f.p("code: ")
    f.input(type="text", name= "code")
    f.br

    f.p("exchange: ")
    f.input(type="text", name= "exchange")
    f.br    

    
    f.input(type="submit", name= "submit")
    f.br

    return str(h)


def html_content_dc(user):
    html_cont = {}
    html_setprice = html_table_setprice(user)
    html_setshare = html_table_setshare(user)
    html_setcost = html_table_setcost(user)
    html_addnew = html_table_addnew(user)
    html_table_filter_str = html_table_filter(user)
    html_table_chg_filter_str = html_table_chg_filter(user)
    html_cont['setprice'] = html_setprice
    html_cont['setshare'] = html_setshare
    html_cont['setcost'] = html_setcost
    html_cont['addnew'] = html_addnew
    html_cont['filter'] = html_table_filter_str
    html_cont['chg_filter'] = html_table_chg_filter_str
    return html_cont
    
        
if __name__ == "__main__":
    k =html_table_addnew('aa')
    print k
    