import json
import time
from datetime import date, datetime, time as ts, timedelta
from nsetools import Nse
import pandas as pd
nse=Nse()
stock_datas = []
old_stock = []

def getStockPriceWrite():
    global old_stock
    try:
        gainers = nse.get_top_gainers()
    except:
        gainers = nse.get_top_gainers()
    modified_data = []
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    times= {'modified_time': current_time, 'curent_date' : str(date.today())}
    current_stock = []
    for key,i in enumerate(gainers):
        modified_data.append({**gainers[key], **times})
        current_stock.append(gainers[key]['symbol'])
    if len(set(current_stock)-set(old_stock)):
        print(current_stock, current_time)
        with open(str(date.today())+'.json','w+') as json_file:
            try:
                existing_data = json.load(json_file)
            except:
                existing_data={'market_data':[]}
            existing_data['market_data'].append([*modified_data])
            json_file.seek(0)
            json.dump(existing_data, json_file, indent = 4)
        old_stock = current_stock

def writeXl():
     with open(str(date.today())+'.json','r+') as json_file:
        existing_data = json.load(json_file)
        write_data = []
        for key_pair in existing_data['market_data']:
            stock_list = ''
            time_change = key_pair[0]['modified_time']
            for inner_key_pair in key_pair:
                stock_list+='\n'+inner_key_pair['symbol']+'- '+str(inner_key_pair['ltp'])
            write_data.append({'Changed stock':stock_list, 'Time of Change':time_change})
        write_data = pd.DataFrame(write_data)
        writer = pd.ExcelWriter(str(date.today())+'_stock_list.xlsx', engine='xlsxwriter')
        write_data.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    
if __name__=='__main__':
     
    # writeXl()
    while True:
        time.sleep(1)
        now = datetime.now()
        target_morning = datetime.combine(date.today(), ts(hour=8, minute=16))
        target_evening = datetime.combine(date.today(), ts(hour=8, minute=17))
        if target_morning < now and target_evening > now:
            print('entered')
            getStockPriceWrite()
        elif target_evening < now:
            print('out')
            writeXl()
            break
        print(now)