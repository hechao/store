import sys
sys.path.append("..")
from data_handle import data_mhandle

funda_ifile = 'funda.csv'
funda_ofile = 'funda_data.csv'

file_path = "/srv/www/idehe.com/store/stock_data/"

data_mhandle(funda_ifile, funda_ofile, file_path)