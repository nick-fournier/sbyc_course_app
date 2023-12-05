
import math
import numpy as np
import pandas as pd
import haversine as hs
from geographiclib.geodesic import Geodesic


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


def get_bearing(point_list):
    lat1, long1, lat2, long2 = [x for point in point_list for x in point]
    bearing = getattr(Geodesic, 'WGS84').Inverse(lat1, long1, lat2, long2)['azi1']
    compass_bearing = (bearing + 360) % 360
    
    return compass_bearing


def get_bearing_man(point_list):
    lat1, long1, lat2, long2 = [x for point in point_list for x in point]
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    bearing = np.arctan2(x, y)
    bearing = np.degrees(bearing)
    compass_bearing = (bearing + 360) % 360
    
    return compass_bearing


def chart_course(course_number, map_data, **kwargs):
    
    # Parse kwargs
    custom_coords = kwargs.get('custom_coords', {})
    rounding = kwargs.get('rounding', 'PORT')
    pin = kwargs.get('pin', 'T1')
    
    # Map data
    order = map_data.get('order')
    objects = map_data.get('objects')
    marks = map_data.get('marks')

    assert marks is not None
    assert order is not None
    assert objects is not None
    
    segment_points = []
    course = order[course_number]['marks'].copy()
    gates = {}
    
    # Loop through the course and populate the attributes
    for mark in course:
        
        mark_name = mark['name']

        # If GATE, select which marks
        if objects[mark_name]['type']  == 'GATE':
            mark['rounding'] = 'GATE'
            object_marks = objects[mark_name]['points']
            object_coords = marks.loc[object_marks]

            # If START, select which pin
            if mark_name == 'START':
                object_coords = object_coords.loc[['RC BOAT', pin]]
                # Update any custom coordinates
                for cc in custom_coords:
                    object_coords.loc[cc, ['lat', 'lon']] = custom_coords[cc]

            # Get effective center from remaining points (if there were more than 2)
            object_center = coord_mean(object_coords[['lat', 'lon']])

            # Effective mark location (center)
            mark['precision_value'] = float(object_coords.precision_value.max())
            mark['lat'], mark['lon'] = object_center

            # Add gate points to gates dict
            gates[mark_name] = object_coords[['lat', 'lon']].to_numpy().tolist()

        else:
            # If starboard rounding, swap W and R and update mark data
            if mark_name in ['W', 'R'] and rounding.upper() == 'STARBOARD':
                mark['rounding'] = 'STARBOARD'
                windward_mark_name = {'W': 'R', 'R': 'W'}[mark_name]
            else:
                windward_mark_name = mark_name
                mark['rounding'] = 'PORT'
                
            mark_data = marks.loc[windward_mark_name, ['precision_value', 'lat', 'lon']]
            mark_data.precision_value = mark_data.precision_value.astype(float)
            mark.update(mark_data.to_dict())

        # Waypoint segments
        segment_points.append([mark['lat'], mark['lon']])

        if len(segment_points) > 1:
            # Calculate the segment bearing angle
            mark['bearing'] = get_bearing(segment_points)
            segment_points.pop(0)
        else:
            mark['bearing'] = '-'

    return course
    
