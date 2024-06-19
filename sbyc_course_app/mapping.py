import yaml
from pathlib import Path
from .utils import chart_course, coord_str_to_dec

# load_static_data once for session
MAP_DATA = {}
for obj in ['marks', 'objects', 'order']:
    print(f'Loading {obj} data...')
    fpath = Path(__file__).parent / 'fixtures' / 'map_data' / f"course_{obj}.yaml"

    with open(fpath) as f:
        MAP_DATA[obj] = yaml.load(f, Loader=yaml.FullLoader)
        
    if obj == 'marks':
        for key in MAP_DATA[obj].keys():
            MAP_DATA[obj][key]['lat'] = coord_str_to_dec(MAP_DATA[obj][key]['lat'])
            MAP_DATA[obj][key]['lon'] = coord_str_to_dec(MAP_DATA[obj][key]['lon'])

# Pre-compute course data
print("Pre-computing course data...")
COURSE_DATA = {i: chart_course(i, MAP_DATA) for i in MAP_DATA['order']}
