from spyre import server

import sys
import pandas as pd

PROJECT_ID = 'spyre-example'

stations = {
    'Paris': '071490',
    'New York': '725033',
    'Seattle': '727930',
    'LA': '722950',
    'Hanoi': '488193',
    'Delhi': '421810',
    'Moscow': '276120',
    'Tehran': '407540',
    'Shanghai': '583620',
}

station_options = [
    {'label': k, 'value': v}
    for k, v in stations.iteritems()
]
station_options[0]['checked'] = True
station_options[1]['checked'] = True


class WeatherHistoryApp(server.App):
    title = "Historical Weather"

    inputs = [
        {
            'type': 'checkboxgroup',
            'label': 'Cities',
            'options': station_options,
            'key': 'stations',
            'action_id': 'weatherplot'
        }, {
            'type': 'radiobuttons',
            'label': 'type',
            'options': [
                {'label': 'Temperature', 'value': 'mean_temp', 'checked': True},
                {'label': 'Precipitation', 'value': 'total_precipitation'}
            ],
            'key': 'type',
            'action_id': 'weatherplot'
        }, {
            'type': 'slider',
            'label': 'Number of Years to Include',
            'min': 1,
            'max': 10,
            'value': 2,
            'key': 'nyears',
            'action_id': 'weatherplot'
        }, {
            'type': 'radiobuttons',
            'label': 'Group by',
            'options': [
                {'label': 'day', 'value': 'day', 'checked': True},
                # {'label': 'month', 'value': 'month'},
                {'label': 'year', 'value': 'year'}
            ],
            'key': 'groupby',
            'action_id': 'weatherplot'
        },
    ]

    outputs = [{
        "type": "plot",
        "id": "weatherplot"
    }]

    def get_data(self, type, station_ids, n_years):
        query = """
            SELECT station_number, year, month, day, {type} as value, rain, snow
            FROM `publicdata.samples.gsod`
            WHERE station_number IN ({stns})
            AND year < 2010
            AND year >= {minyr}
        """.format(
            type=type,
            stns=','.join(station_ids),
            minyr=2010 - n_years
        )

        df = pd.read_gbq(query, project_id=PROJECT_ID, dialect='standard')
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

        stations_df = pd.DataFrame({
            'location': stations.keys(),
            'station_number': [int(v) for v in stations.values()]
        })
        df = pd.merge(df, stations_df, on='station_number')
        return df

    def weatherplot(self, params):
        station_ids = params['stations']
        n_years = params['nyears']
        ttype = params['type']
        groupby = params['groupby']
        if ttype == 'total_precipitation':
            title = 'Rain Fall'
            ylab = 'rain (inches)'
        elif ttype == 'mean_temp':
            title = 'Temperature'
            ylab = 'temp (F)'

        df = self.get_data(ttype, station_ids, n_years)
        if groupby == 'day':
            df = df.pivot_table(values='value', index='date', columns='location')
        elif groupby == 'year':
            df_by_year = df.groupby(['year', 'location']).mean()[['value']].reset_index()
            df = df_by_year.pivot_table(values='value', index='year', columns='location')
            title = 'Average ' + title
        ax = df.plot(title=title)
        ax.set_ylabel(ylab)
        return ax


if __name__ == "__main__":
    app = WeatherHistoryApp()
    args = sys.argv[1:]
    if len(args) == 1:
        app.launch(host=args[0])
    elif len(args) == 2:
        app.launch(host=args[0], port=int(args[1]))
    else:
        app.launch()
