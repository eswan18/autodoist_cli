import json

import click

JACKET_TEMP_THRESHOLD = 50
COAT_TEMP_THRESHOLD = 40
GLOVES_TEMP_THRESHOLD = 35
CSV_COL_NAMES = ['TYPE', 'CONTENT', 'PRIORITY', 'INDENT', 'AUTHOR',
                 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE']

def get_specs_from_user():
    name = click.prompt('Name for the project')
    csv_name = click.prompt('Name of template file to be created',
                            default=name + '.csv')
    n_days = click.prompt('Including travel time, how many days will this trip be?',
                          type=int, prompt_suffix=' ')
    can_wash = click.prompt('Will you have access to a washer and dryer during the trip?',
                            type=bool, prompt_suffix=' ')
    is_flying  = click.prompt('Are you flying and taking only a carry-on?',
                              type=bool, prompt_suffix=' ')
    dress_days = click.prompt('How many days will you need to wear clothing nicer than jeans?',
                              type=int, prompt_suffix=' ')
    max_temp = click.prompt('On a typical day, what is the maximum likely temperature?',
                            type=int, prompt_suffix=' ')
    min_temp = click.prompt('On a typical day, what is the minimum likely temperature?',
                            type=int, prompt_suffix=' ')
    # If it's already cold enough that you'll need a jacket and you'll be
    # spending a lot of time outdoors, probably a good idea to bring warm
    # clothes.
    if GLOVES_TEMP_THRESHOLD < min_temp < JACKET_TEMP_THRESHOLD:
        extended_outdoor_time = click.prompt('Will you be spending an extended'
                                             ' period of time outdoors when it'
                                             ' might be somewhat cold?',
                                             type=bool, prompt_suffix=' ')
    return locals()

def load_specs_from_file(file, format):
    if format.lower() == 'json':
        try:
            with open(file) as f:
                specs = json.loads(f.read())
        except json.decoder.JSONDecodeError as e:
            # Raise a JSONDecodeError with a better message than the automatic
            # one.
            msg = 'File {} is not valid JSON'.format(file)
            raise json.decoder.JSONDecodeError(msg, doc=e.doc, pos=e.pos)
    elif format.lower() == 'yaml':
        # TODO
        msg = 'haven\'t gotten to yaml reading yet'
        raise NotImplementedError(msg)
    else:
        msg = 'Unknown format. Format should be one of [json, yaml]'
        raise ValueError(msg)
    return specs

def gen_travel_checklist_csv_from_specs(specs):
    # Outsource the hard part to another function.
    category_items = gen_items_and_quantities_by_category(specs)
    # Format properly for Todoist, starting with a header.
    csv_str = ','.join(CSV_COL_NAMES) + '\n'
    for category, items in category_items.items():
        csv_str += make_task_line(category, indent=1)
        for item in items:
            item_name, item_quant = item[0], item[1]
            item_content = '{} ({})'.format(item_name, item_quant)
            csv_str += make_task_line(item_content, indent=2)
            # If the item has a note attached, add a line appropriately.
            if len(item) > 2:
                csv_str += make_note_line(item[2])
    return csv_str

def gen_items_and_quantities_by_category(specs):
    return {
        'footwear': [
            ('shoes', 2, 'remember these'),
            ('socks', 2)
        ],
        'headwear': [
            ('hat', 1)
        ]
    }
                
def make_task_line(task_name, priority=4, indent=1):
    return 'task,{},{},{},,,,,'.format(task_name, priority, indent) + '\n'

def make_note_line(note_name):
    return 'note,{},,,,,,,'.format(note_name) + '\n'
