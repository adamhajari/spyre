from spyre import server
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

cities = [
    {'label': 'New York', 'value': '1', 'checked': True},
    {'label': 'San Francisco', 'value': '13', 'checked': True},
    {'label': 'Portland, OR', 'value': '26', 'checked': True},
    {'label': 'Miami', 'value': '42', 'checked': True},
    {'label': 'New Orleans', 'value': '49', 'checked': True},
    {'label': 'Washington D.C.', 'value': '21'},
    {'label': 'Raleigh, NC', 'value': '41'},
    {'label': 'St. Louis', 'value': '61'},
    {'label': 'Chicago', 'value': '3'},
    {'label': 'Boise', 'value': '99'},
    {'label': 'Boulder', 'value': '276'},
    {'label': 'Austin', 'value': '11'},
    {'label': 'Philidelphia', 'value': '6'},
    {'label': 'Phoenix', 'value': '5'},
    {'label': 'Nashville', 'value': '24'},
    {'label': 'Los Angeles', 'value': '2'},
    {'label': 'Huntsville', 'value': '124'},
]

DB_PATH = 'city_weather.db'

con = sqlite3.connect(DB_PATH)
query = """select c.* from cities c"""
all_cities_df = pd.read_sql(query, con)

query = """select * from qol"""
qol_df = pd.read_sql(query, con)
con.close()


def sort_months(df):
    df = df.drop('Anu')
    df['month_num'] = pd.to_datetime(df.index, format='%b').month
    df.sort_values(by='month_num', inplace=True)
    df.drop('month_num', axis=1, inplace=True)
    return df


class WeatherCompareApp(server.App):
    title = 'City Comparisons'

    inputs = [{
        'type': 'searchbox',
        'label': 'city',
        'options': all_cities_df['city'].tolist(),
        'key': 'city',
        'action_id': 'update_all',
        'value': 'Search for city'
    }, {
        'type': 'checkboxgroup',
        'label': 'cities',
        'options': cities,
        'key': 'city_ids',
        'action_id': 'update_all'


    }]

    outputs = [{
        'type': 'plot',
        'id': 'weather',
        'control_id': 'update_all',
        'tab': 'weather'
    }, {
        'type': 'plot',
        'id': 'size',
        'control_id': 'update_all',
        'tab': 'size'
    }, {
        'type': 'plot',
        'id': 'qol',
        'control_id': 'update_all',
        'tab': 'quality-of-life'
    }]

    controls = [{
        'type': 'button',
        'label': 'update',
        'id': 'update_all'
    }]

    tabs = ['quality-of-life', 'weather', 'size']

    def weather(self, params):
        city_ids = params['city_ids']
        city = params['city']
        if len(all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()) > 0:
            extra_id = all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()[0]
            city_ids.append(extra_id)

        con = sqlite3.connect(DB_PATH)
        query = """
            select c.city, w.* from weather w
            inner join cities c
            on w.id=c.id
            where c.id IN (%s)
        """ % ','.join(city_ids)
        df = pd.read_sql(query, con)
        con.close()

        f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(7, 18))

        df_avghigh = df[['city', 'month', 'average_high']]\
            .pivot_table(index='month', columns='city', values='average_high')
        df_avghigh = sort_months(df_avghigh)
        ax1.set_ylabel('avg high (F)')
        df_avghigh.plot(ax=ax1)
        ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fancybox=True)

        df_avglow = df[['city', 'month', 'average_low']]\
            .pivot_table(index='month', columns='city', values='average_low')
        df_avglow = sort_months(df_avglow)
        ax2.set_ylabel('avg low (F)')
        df_avglow.plot(ax=ax2)
        ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fancybox=True)

        df_sun = df[['city', 'month', 'mean_monthly_sun']]\
            .pivot_table(index='month', columns='city', values='mean_monthly_sun')
        df_sun = sort_months(df_sun)
        ax3.set_ylabel('mean sunshine (hours)')
        df_sun.plot(ax=ax3)
        ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fancybox=True)

        df_sun = df[['city', 'month', 'avg_precip_in']]\
            .pivot_table(index='month', columns='city', values='avg_precip_in')
        df_sun = sort_months(df_sun)
        ax4.set_ylabel('avg precipitation (in)')
        df_sun.plot(ax=ax4)
        ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fancybox=True)

        df_sun = df[['city', 'month', 'avg_snowfall_in']]\
            .pivot_table(index='month', columns='city', values='avg_snowfall_in')
        df_sun = sort_months(df_sun)
        ax5.set_ylabel('avg snowfall (in)')
        df_sun.plot(ax=ax5)
        ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fancybox=True)
        return f

    def size(self, params):
        city_ids = params['city_ids']
        city = params['city']
        if len(all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()) > 0:
            extra_id = all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()[0]
            city_ids.append(extra_id)
        f, (ax1, ax2) = plt.subplots(2, figsize=(7, 10))
        df = all_cities_df.loc[all_cities_df['id'].isin(city_ids), :]

        df['density'] = df['density'] / 1000
        ax1.set_xlabel('density (x1k people/sq mi)')
        df[['city', 'density']].set_index('city').plot(ax=ax1, kind='barh', legend=False)

        ax2.set_xlabel('population (x 100k)')
        df['population'] = df['population'] / 100000
        df[['city', 'population']].set_index('city').plot(ax=ax2, kind='barh', legend=False)
        return f

    def qol(self, params):
        city_ids = params['city_ids']
        city = params['city']
        if len(all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()) > 0:
            extra_id = all_cities_df.loc[all_cities_df['city'] == city, 'id'].tolist()[0]
            city_ids.append(extra_id)
        f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = plt.subplots(9, figsize=(7, 26))
        df = qol_df.loc[qol_df['id'].isin(city_ids), :]

        ax1.set_title('Quality of Life Index', fontsize=10)
        df[['city', 'Quality of Life Index']].set_index('city')\
            .plot(ax=ax1, kind='barh', legend=False)

        ax2.set_title('Property Price to Income Ratio', fontsize=10)
        df[['city', 'Property Price to Income Ratio']].set_index('city')\
            .plot(ax=ax2, kind='barh', legend=False)

        ax3.set_title('Traffic Commute Time Index', fontsize=10)
        df[['city', 'Traffic Commute Time Index']].set_index('city')\
            .plot(ax=ax3, kind='barh', legend=False)

        ax4.set_title('Cost of Living Index', fontsize=10)
        df[['city', 'Cost of Living Index']].set_index('city')\
            .plot(ax=ax4, kind='barh', legend=False)

        ax5.set_title('Climate Index', fontsize=10)
        df[['city', 'Climate Index']].set_index('city')\
            .plot(ax=ax5, kind='barh', legend=False)

        ax6.set_title('Safety Index', fontsize=10)
        df[['city', 'Safety Index']].set_index('city')\
            .plot(ax=ax6, kind='barh', legend=False)

        ax7.set_title('Pollution Index', fontsize=10)
        df[['city', 'Pollution Index']].set_index('city')\
            .plot(ax=ax7, kind='barh', legend=False)

        ax8.set_title('Purchasing Power Index', fontsize=10)
        df[['city', 'Purchasing Power Index']].set_index('city')\
            .plot(ax=ax8, kind='barh', legend=False)

        ax9.set_title('Health Care Index', fontsize=10)
        df[['city', 'Health Care Index']].set_index('city')\
            .plot(ax=ax9, kind='barh', legend=False)
        f.tight_layout()
        return f


app = WeatherCompareApp()
app.launch()
