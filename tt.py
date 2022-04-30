from os.path import exists
from xlrd.book import open_workbook_xls
import xlwt
city='上海'
file='D:/my.xls'
if not exists(file):
    wb=xlwt.Workbook()
    ws = wb.add_sheet(city)
    wb.save('D:/my.xls')
    
