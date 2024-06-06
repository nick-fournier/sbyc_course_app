
import math
# import haversine as hs
# from geographiclib.geodesic import Geodesic


def coord_str_to_dec(string):
    if not isinstance(string, str):
        raise ValueError('Input must be a string')
    
    deg, minute = [float(x) for x in string.split(' ')]
    
    return deg + math.copysign(minute / 60, deg)
    
def coord_mean(coord_pairs):
    lat_sum, lon_sum = 0, 0
    for coord in coord_pairs:
        lat, lon = coord
        
        # if format is ddd mm.mmm (not ddd.ddddd)
        if isinstance(lat, str):
            lat = coord_str_to_dec(lat)
            lon = coord_str_to_dec(lon)
        
        lat_sum += lat
        lon_sum += lon
    return lat_sum / len(coord_pairs), lon_sum / len(coord_pairs)


def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Radius of the Earth in km
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in km
    distance = R * c
    
    return distance


# def coord_diff(coord_df, units=hs.Unit.METERS):
#     # Distance from center point
#     center = coord_mean(coord_df)

#     if not all(coord_df.dtypes == [float, float]):
#         coord_df = coord_df.apply(coord_str_to_dec)

#     return coord_df.apply(lambda x: hs.haversine(center, tuple(x), unit=units), axis=1).max()


def get_bearing(point_list):
    lat1, long1, lat2, long2 = [x for point in point_list for x in point]
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = (
        math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - 
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    )
    bearing = math.degrees(math.atan2(x, y))
    compass_bearing = (bearing + 360) % 360
    
    return compass_bearing


def chart_course(course_number, map_data, **kwargs):
    
    # Parse kwargs
    custom_coords = kwargs.get('custom_coords', {})
    rounding = kwargs.get('rounding', 'PORT')
    pin = kwargs.get('pin', 'T1')
    
    # Map data
    order = map_data['order']
    objects = map_data['objects']
    marks = map_data['marks']
    
    segment_points = []
    course = []
    gates = {}
    
    # Loop through the course and populate the attributes
    for order, mark_name in enumerate(order[course_number]['marks']):
        
        # Populate mark data from the objects dict
        mark = {
            'name': mark_name,
            'order': order,
            **objects[mark_name]
            }
        
        # If GATE, select which marks
        if mark['rounding'] == 'GATE':

            # If START, select which pin
            if mark_name == 'START':
                object_marks = ['RC BOAT', pin]
            else:
                object_marks = objects[mark_name]['points']

            object_coords = {k: marks[k] for k in object_marks}
            
            # Assert all custom coord keys are in the object_coords dict
            assert all([k in object_coords for k in custom_coords])
            object_coords.update(custom_coords)

            # Get effective center from remaining points (if there were more than 2)
            coord_pairs = [(x['lat'], x['lon']) for x in object_coords.values()]

            # Effective mark location (center) and precision
            mark['precision'] = float(max([x['precision'] for x in object_coords.values()]))
            mark['lat'], mark['lon'] = coord_mean(coord_pairs)

            # Add gate points to gates dict
            gates[mark_name] = coord_pairs

        else:
            # If starboard rounding, swap W and R and update mark data
            if mark_name in ['W', 'R'] and rounding.upper() == 'STARBOARD':
                mark['rounding'] = 'STARBOARD'
                windward_mark_name = {'W': 'R', 'R': 'W'}[mark_name]
            else:
                windward_mark_name = mark_name
                mark['rounding'] = 'PORT'
            
            mark.update(marks[windward_mark_name])

        # Waypoint segments
        segment_points.append([mark['lat'], mark['lon']])

        if len(segment_points) > 1:
            # Calculate the segment bearing angle
            mark['bearing'] = int(get_bearing(segment_points))
            segment_points.pop(0)
        else:
            mark['bearing'] = '-'
        
        course.append(mark)

    return course
    
