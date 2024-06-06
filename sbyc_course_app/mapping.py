import yaml
from pathlib import Path
import json
import folium
import pandas as pd
from .utils import coord_mean, get_bearing, chart_course, coord_str_to_dec


print('Loading map data...')
# load_static_data once for session
MAP_DATA = {}
for obj in ['marks', 'objects', 'order']:
    fpath = Path(__file__).parent / 'fixtures' / 'map_data' / f"course_{obj}.yaml"

    with open(fpath) as f:
        MAP_DATA[obj] = yaml.load(f, Loader=yaml.FullLoader)
        
    if obj == 'marks':
        for key in MAP_DATA[obj].keys():
            MAP_DATA[obj][key]['lat'] = coord_str_to_dec(MAP_DATA[obj][key]['lat'])
            MAP_DATA[obj][key]['lon'] = coord_str_to_dec(MAP_DATA[obj][key]['lon'])


# Pre-compute course data
COURSE_DATA = {i: chart_course(i, MAP_DATA) for i in MAP_DATA['order']}

# # TODO: eliminate this class
# class CourseCharting:
#     def __init__(self, **kwargs):               
#         # default kwargs, explicit types
#         self.course_number = kwargs.get('course_number')
#         self.is_mobile = kwargs.get('is_mobile', False)
#         self.custom_coords = kwargs.get('custom_coords', {})
#         self.rounding = kwargs.get('rounding', 'PORT')
#         self.pin = kwargs.get('pin', 'T1')
        
#         # Defaults from map data
#         self.order = MAP_DATA['order']
#         self.objects = MAP_DATA['objects']
#         self.marks = MAP_DATA['marks']
            

#     def plot_course(self):

#         #TODO map doesn't scale, need to get pixels somehow...
#         if getattr(self, 'is_mobile'):
#             height = '100%'

#         assert self.marks is not None
#         assert self.order is not None
#         assert self.objects is not None

#         # Map overall center point
#         center = coord_mean([(x['lat'], x['lon']) for x in self.marks.values()])
        
#         # TODO: Split the folium mapping and the course route generator
#         # Plot map and marks
#         m = folium.Map(location=center, zoom_start=13, height='100%', width='100%')

#         segment_points = []
#         # course_df = self.order[str(self.course_number)].copy()
#         course = self.order[self.course_number]['marks'].copy()
        
#         df_cols = ['order', 'rounding', 'bearing', 'lat', 'lon']
#         course_df = pd.DataFrame(columns=df_cols, index=[x['name'] for x in course])
#         course_df.index.name = 'name'
        
#         # for mark_name, course_event in course_df.iterrows():
#         for mark in course:
            
#             mark_rounding = 'PORT'
#             mark_name = mark['name']
#             mark_type = self.objects[mark_name]['type']
            
#             # Add the order number to df
#             course_df.loc[mark_name, 'order'] = mark['order']            

#             # if len(self.objects[course_event.name]['points']) > 1:
#             # if course_event.get('rounding', self.rounding).upper() == 'GATE':
#             # if course_object.rounding is not None and course_event.rounding.upper() == 'GATE':
#             if mark_type == 'GATE':
#                 mark_rounding = 'GATE'
#                 object_marks = self.objects[mark_name]['points']
#                 object_coords = self.marks.loc[object_marks]

#                 # If START, select which pin
#                 if mark_name == 'START':
#                     object_coords = object_coords.loc[['RC BOAT', self.pin]]
#                     # Update any custom coordinates
#                     for cc in self.custom_coords:
#                         object_coords.loc[cc, ['lat', 'lon']] = self.custom_coords[cc]

#                 # Get effective center from remaining points (if there were more than 2)
#                 object_center = coord_mean(object_coords[['lat', 'lon']])

#                 # Effective mark location (center)
#                 mark['precision_value'] = object_coords.precision_value.max()

#                 mark['latlon'] = object_center
#                 for k, v in iter(zip(['lat', 'lon'], object_center)):
#                     mark[k] = v

#                 # Plot gate segment
#                 for name, gate_point in object_coords.iterrows():
#                     folium.Circle(
#                         radius=gate_point.precision_value,
#                         location=(gate_point.lat, gate_point.lon),
#                         popup=name,
#                         color="blue",
#                         fill=False,
#                     ).add_to(m)

#                 gate_points = object_coords[['lat', 'lon']].to_numpy().tolist()
#                 folium.PolyLine(gate_points, color="blue", weight=2.5, opacity=1).add_to(m)

#             else:
#                 # If starboard rounding, swap W and R and update mark data
#                 if mark_name in ['W', 'R'] and self.rounding.upper() == 'STARBOARD':
#                     mark_rounding = 'STARBOARD'
#                     windward_mark_name = {'W': 'R', 'R': 'W'}[mark_name]
#                     mark.update(self.marks.loc[windward_mark_name].to_dict())
#                 else:
#                     mark.update(self.marks.loc[mark_name].to_dict())

#             # Add the rounding to the chart table
#             if mark_name in ['W', 'R']:
#                 course_df.loc[mark_name, 'rounding'] = self.rounding
#             else:
#                 course_df.loc[mark_name, 'rounding'] = mark_rounding

#             # mark_coords = mark[['lat', 'lon']].to_list()            
#             mark_coords = [mark['lat'], mark['lon']]
            
#             folium.Circle(
#                 radius=int(mark.get('precision_value', 0)),
#                 location=mark_coords,
#                 popup=mark_name,
#                 color="crimson",
#                 fill=False,
#             ).add_to(m)

#             # Waypoint segments
#             segment_points.append(mark_coords)
#             course_df.loc[mark_name, ['lat', 'lon']] = mark_coords

#             if len(segment_points) > 1:
#                 # Calculate the segment bearing angle
#                 course_df.loc[mark_name, 'bearing'] = get_bearing(segment_points)
#                 folium.PolyLine(segment_points,
#                                 color="red", weight=2.5, opacity=1,
#                                 # popup=course_object.order-1
#                                 ).add_to(m)
#                 segment_points.pop(0)

#         # Update map center
#         m.location = coord_mean(pd.DataFrame(segment_points, columns=['lat', 'lon']))  # type: ignore
        
#         # Fill in bearing
#         # course_df.bearing = course_df.bearing.astype('Int64')
#         course_df.bearing = course_df.bearing.fillna(0).astype(int).astype(str).replace('0', '-')        
        
#         # Cleanup and output
#         course_df.reset_index(inplace=True)
#         course_df = course_df[['order', 'name', 'rounding', 'bearing', 'lat', 'lon']]
#         course_df.columns = [s.capitalize() for s in course_df.columns]

#         # m.save('templates/test_map.html')
#         return {'chart': m, 'chart_table': course_df, 'course_number': self.course_number}
