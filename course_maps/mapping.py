import copy
import yaml
import os
import json
import folium
import haversine as hs
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


def coord_mean(coord_df):
    if not all(coord_df.dtypes == [float, float]):
        coord_df = coord_df.apply(coord_to_latlon)

    return tuple(coord_df.sum() / len(coord_df.dropna()))


def coord_diff(coord_df, units=hs.Unit.METERS):
    # Distance from center point
    center = coord_mean(coord_df)

    if not all(coord_df.dtypes == [float, float]):
        coord_df = coord_df.apply(coord_to_latlon)

    return coord_df.apply(lambda x: hs.haversine(center, tuple(x), unit=units), axis=1).max()


class CourseData:
    def __init__(self, **kwargs):
        # Set default kwargs
        defaultKwargs = {'static': True,
                         'pin': 'T1',
                         'rounding': 'PORT',
                         'custom_coords': {},
                         'is_mobile': False}
        kwargs = {**defaultKwargs, **kwargs}

        # Setup class vars
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.marks = self.objects = self.order = None
        # self.course_number = course_number
        self.settings = {'data_dir': 'course_maps/map_data',
                         'course_data': {
                             'marks': 'course_marks.csv',
                             'objects': 'course_objects.yaml',
                             'order': 'course_order.yaml'}
                         }
        if self.static:
            self.load_static_data()

    def plot_course(self):

        #TODO map doesn't scale, need to get pixels somehow...
        if self.is_mobile:
            height = '100%'

        # Map overall center point
        center = coord_mean(self.marks[['lat', 'lon']])
        # Plot map and marks
        m = folium.Map(location=center, zoom_start=14, height='100%', width='100%')

        points = []
        for index, course_object in self.order[str(self.course_number)].iterrows():

            # if len(self.objects[course_object.name]['points']) > 1:
            if course_object.rounding is not None and course_object.rounding.upper() == 'GATE':
                object_marks = self.objects[course_object.name]['points']
                object_coords = self.marks.loc[object_marks]

                # If START, select which pin
                if course_object.name == 'START':
                    object_coords = object_coords.loc[['RC BOAT', self.pin]]
                    # Update any custom coordinates
                    for cc in self.custom_coords:
                        object_coords.loc[cc, ['lat', 'lon']] = self.custom_coords[cc]

                # Get effective center from remaining points (if there were more than 2)
                object_center = coord_mean(object_coords[['lat', 'lon']])

                # Effective mark location (center)
                mark = course_object
                mark['precision_value'] = 40  # coord_diff(object_coords, units=hs.Unit.METERS)

                mark['latlon'] = object_center
                for k, v in iter(zip(['lat', 'lon'], object_center)):
                    mark[k] = v

                # Plot gate segment
                for name, gate_point in object_coords.iterrows():
                    folium.Circle(
                        radius=gate_point.precision_value,
                        location=(gate_point.lat, gate_point.lon),
                        popup=name,
                        color="blue",
                        fill=False,
                    ).add_to(m)

                gate_points = object_coords[['lat', 'lon']].to_numpy().tolist()
                folium.PolyLine(gate_points, color="blue", weight=2.5, opacity=1).add_to(m)

            else:
                # If starboard rounding, swap W and R
                if course_object.name in ['W', 'R'] and self.rounding.upper() == 'STARBOARD':
                    windward = {'W': 'R', 'R': 'W'}[course_object.name]
                    mark = copy.deepcopy(self.marks.loc[windward])
                    mark.name = course_object.name
                else:
                    mark = copy.deepcopy(self.marks.loc[course_object.name])

            points.append(mark[['lat', 'lon']].to_list())

            folium.Circle(
                radius=int(mark.precision_value),
                location=mark[['lat', 'lon']].to_list(),
                popup=mark.name,
                color="crimson",
                fill=False,
            ).add_to(m)

        # Plot map waypoint segments
        # TODO place this in the loop to break into separately labeled segments?
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

        # Update map center
        m.location = coord_mean(pd.DataFrame(points, columns=['lat','lon']))

        # m.save('templates/test_map.html')
        return m

    def load_static_data(self):
        for key, file in self.settings['course_data'].items():
            fpath = os.path.join(self.settings['data_dir'], file)

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
                data = {str(x.pop('course_number')): pd.DataFrame(x['marks']) for x in data}
                for k, v in data.items():
                    v.index = v['name']

            setattr(self, key, data)


if __name__ == "__main__":

    # if os.path.basename(os.getcwd()) != 'course_maps':
    #     os.chdir('course_maps')
    self = CourseData(**{'course_number': 16})
    self.plot_course()
