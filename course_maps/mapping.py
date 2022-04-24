import numpy as np
import yaml
import os
import json
import folium
import math
import pandas as pd
import numpy as np

def coord_to_latlon(string):
    if not isinstance(string, str):
        lat, lon = [np.nan] * 2
    else:
        lat, lat_min, lon, lon_min = [float(x) for x in string.split(' ')]
        lat += np.sign(lat) * (lat_min / 60)
        lon += np.sign(lon) * (lon_min / 60)

    return pd.Series([lat, lon])

class CourseData:
    def __init__(self):
        self.settings_file = "settings.yaml"
        self.load_course_data()

    def load_course_data(self):
        settings = yaml.load(open(self.settings_file), Loader=yaml.FullLoader)

        for key, file in settings['course_data'].items():
            fpath = os.path.join(settings['data_dir'], file)

            if '.csv' in file:
                data = pd.read_csv(fpath)

            with open(fpath) as f:
                if '.yaml' in file:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                if '.json' in file:
                    data = json.load(f)

            # Data formatting
            if key == 'marks' and isinstance(data, pd.DataFrame):
                data[['lat', 'lon']] = data.coord_string.apply(coord_to_latlon)
                data.index = data['name']

            if key == 'objects':
                data = {x.pop('name'): x for x in data}

            if key == 'order':
                data = {str(x.pop('course_number')): x for x in data}

            setattr(self, key, data)



    def plot_course(self, course_number):
        # Map center point
        center = list(self.marks[['lat', 'lon']].sum() / len(self.marks.dropna()))

        # Plot map and marks
        m = folium.Map(location=center)

        points = []
        for p in self.order[str(course_number)]['marks']:

            if p['rounding'] == 'gate':
                object_marks = self.objects[p['mark']]['points']

                self.marks.loc[object_marks]

            else:
                mark = self.marks.loc[object['mark']]

            coord = tuple(self.marks.loc[object['mark']][['lat', 'lon']])
            points.append(coord)

            folium.Circle(
                radius=mark.precision_value,
                location=coord,
                popup=mark.name,
                color="crimson",
                fill=False,
            ).add_to(m)

        # Plot map waypoint segments
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

        m.save('templates/map.html')


if __name__ == "__main__":
    os.chdir('course_maps')
    self = CourseData()
    self.plot_course()
