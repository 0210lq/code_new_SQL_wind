import os
import pandas as pd
import global_setting.global_dic as glv
import sys
path = os.getenv('GLOBAL_TOOLSFUNC_new')
sys.path.append(path)
import global_tools as gt
import yaml
import pymysql
from setup_logger.logger_setup import setup_logger
class indexdata_prepare:
    def __init__(self,available_date):
        self.available_date=available_date
    def raw_wind_index_data_withdraw(self):  # available_date这里是YYYYMMDD格式
        inputpath_wind = glv.get('input_wind_indexdata')
        inputpath_wind = gt.file_withdraw(inputpath_wind, self.available_date)
        df_wind = gt.readcsv(inputpath_wind)
        return df_wind

class indexComponent_prepare:
    def __init__(self,available_date):
        self.available_date=available_date
    def file_name_withdraw(self,index_type,source_name):
        if index_type == '上证50':
            if source_name=='jy':
                return 'sz50Monthly'
            else:
                return'sz50'
        elif index_type == '沪深300':
            if source_name == 'jy':
                 return 'csi300Monthly'
            else:
                return 'hs300'
        elif index_type == '中证500':
            if source_name == 'jy':
                 return 'zz500Monthly'
            else:
                return'zz500'
        elif index_type == '中证1000':
            if source_name=='jy':
                 return 'zz1000Monthly'
            else:
                return 'zz1000'
        elif index_type == '中证2000':
            if source_name == 'jy':
                return 'zz2000Monthly'
            else:
                return 'zz2000'
        elif index_type=='国证2000':
            if source_name=='jy':
                return 'gz2000Monthly'
            else:
                return 'gz2000'
        else:
            if source_name == 'jy':
                return 'zzA500Monthly'
            else:
                return 'zzA500'


    def raw_wind_index_component_preparing(self,index_type):
        inputpath_component = glv.get('input_wind_indexcomponent')
        file_name = self.file_name_withdraw(index_type,'wind')
        inputpath_component_update = os.path.join(inputpath_component, file_name)
        inputpath_component_update = gt.file_withdraw(inputpath_component_update, self.available_date)
        df_daily = gt.readcsv(inputpath_component_update)
        if len(df_daily) != 0:
            df_daily.columns = ['date','code','weight']
            df_daily['status']=1
            df_daily=df_daily[['code', 'weight', 'status']]
            df_daily = df_daily[df_daily['status'] == 1]
            df_daily['weight'] = df_daily['weight'] / 100
        return df_daily
class stockData_preparing:
    def __init__(self,available_date):
        self.available_date =available_date

    def raw_wind_stockdata_withdraw(self):
        inputpath_stock = glv.get('input_wind_stock')
        inputpath_stock = gt.file_withdraw(inputpath_stock, self.available_date)
        df_stock = gt.readcsv(inputpath_stock)
        available_date2 = pd.to_datetime(self.available_date)
        available_date2 = available_date2.strftime('%Y-%m-%d')
        df_stock['valuation_date'] = available_date2
        def trade_status(x):
            if x=='交易':
                return 1
            else:
                return 0
        try:
            df_stock['tarde_status']= df_stock['tarde_status'].apply(lambda x:trade_status(x))
        except:
            try:
                df_stock['trade_status'] = df_stock['trade_status'].apply(lambda x: trade_status(x))
            except:
                pass
        return df_stock









if __name__ == '__main__':
    # cbp=BankMomentum_prepare('2025-05-06')
    # cbp.raw_BankMomentum_prepare()
    pass