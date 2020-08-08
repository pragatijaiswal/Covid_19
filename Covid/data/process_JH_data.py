import pandas as pd
import numpy as np

from datetime import datetime


def store_relational_JH_data():
    ''' Transformes the COVID data in a relational data set

    '''

    data_path='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    pd_raw=pd.read_csv(data_path)

    pd_data_base=pd_raw.rename(columns={'Country/Region':'country',
                      'Province/State':'state'})

    pd_data_base['state']=pd_data_base['state'].fillna('no')

    pd_data_base=pd_data_base.drop(['Lat','Long'],axis=1)


    pd_relational_model=pd_data_base.set_index(['state','country']) \
                                .T                              \
                                .stack(level=[0,1])             \
                                .reset_index()                  \
                                .rename(columns={'level_0':'date',
                                                   0:'confirmed'},
                                                  )

    pd_relational_model['date']=pd_relational_model.date.astype('datetime64[ns]')

    pd_relational_model.to_csv('data/processed/COVID_relational_confirmed.csv',sep=';',index=False)
    print(' Number of rows stored: '+str(pd_relational_model.shape[0]))
    print('tail of relational data: ')
    print(pd_relational_model.tail(5))

    
def store_flat_table():
    data_path='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    pd_raw=pd.read_csv(data_path)
    country_list = pd_raw['Country/Region'].unique()
    time_idx=pd_raw.columns[4:]
    df_plot = pd.DataFrame({'date':time_idx})
    for each in country_list:
        df_plot[each]=np.array(pd_raw[pd_raw['Country/Region']==each].iloc[:,4::].sum(axis=0))
    time_idx=[datetime.strptime( each,"%m/%d/%y") for each in df_plot.date] # convert to datetime
    df_plot['date']=time_idx
    df_plot.to_csv('data/processed/COVID_small_flat_table_conf.csv',sep=';',index=False)
    
    data_path='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    pd_raw=pd.read_csv(data_path)
    country_list = pd_raw['Country/Region'].unique()
    time_idx=pd_raw.columns[4:]
    df_plot = pd.DataFrame({'date':time_idx})
    for each in country_list:
        df_plot[each]=np.array(pd_raw[pd_raw['Country/Region']==each].iloc[:,4::].sum(axis=0))
    time_idx=[datetime.strptime( each,"%m/%d/%y") for each in df_plot.date] # convert to datetime
    df_plot['date']=time_idx
    df_plot.to_csv('data/processed/COVID_small_flat_table_recov.csv',sep=';',index=False)
    
if __name__ == '__main__':

    store_relational_JH_data()
    store_flat_table()
