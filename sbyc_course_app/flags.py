import os
import yaml

THIS_PATH = os.path.dirname(os.path.abspath(__file__))


def path_to_image_html(src):
    return "<img src=\"{}\" height=\"30\">".format(src)


def dict_list_to_html_table(data, cols=[], html_classes=''):
    if html_classes == '':
        table_html = '<table>\n'
    else:
        table_html = f'<table class="{html_classes}">\n'
    
    # Header row
    table_html += '<thead>\n<tr>'
    for key in data[0].keys():
        if key in cols:
            table_html += f'<th>{key.capitalize()}</th>'
    table_html += '</tr>\n</thead>\n'
    
    # Body rows
    table_html += '<tbody>\n'
    for item in data:
        table_html += '<tr>'
        for key, value in item.items():
            if key == 'flag':
                table_html += f'<td><img src="{value}" height="30"></td>'
            else:
                table_html += f'<td>{value}</td>'
        table_html += '</tr>\n'
    table_html += '</tbody>\n'
    
    table_html += '</table>'
    
    return table_html


def html_flag_tables(html_classes):
    
    with open(os.path.join(THIS_PATH, 'fixtures/flags.yaml')) as f:
        flag_data = yaml.load(f, Loader=yaml.FullLoader)
    
    flag_tables = {}
    for flag_type, flags in flag_data.items():        
        # Convert to html table
        html_table = dict_list_to_html_table(
            flags,
            cols=['name', 'phonetic', 'flag'],
            html_classes=html_classes
        )
        flag_tables[flag_type + '_flag_table'] = html_table

    return flag_tables

