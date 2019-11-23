import json
import math

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
                
def make_task_line(task_name, priority=4, indent=1):
    return 'task,{},{},{},,,,,'.format(task_name, priority, indent) + '\n'

def make_note_line(note_name):
    return 'note,{},,,,,,,'.format(note_name) + '\n'

def gen_items_and_quantities_by_category(specs):
    # Some meta-parameters.
    n_days = specs['n_days']
    if specs['can_wash']:
        n_days_wash = math.ceil(n_days / 2) + 1)
    else:
        n_days_wash = n_days
    max_temp, min_temp = specs['max_temp'], specs['min_temp']
    avg_temp = (max_temp + min_temp) / 2
    dress_days = specs['dress_days']
    is_flying = specs['is_flying']
    # This feels hacky but it's going to be cumbersome no matter how we do it.

    daily_wear = []
    # --- Underwear
    daily_wear += ('Underwear', n_days_wash + 2)
    # --- Undershirts
    daily_wear += ('Undershirts', n_days_wash)
    # --- Jeans/chinos
    if min_temp >= 70:
        n_jeans = 0 if n_days_wash < 2 else 1
    # A lot has to happen to bring 3 pairs of jeans.
    elif max_temp <= 75 and n_days_wash >= 7 and not specs['is_flying']:
        n_jeans = 3
    else:
        n_jeans = 2
    daily_wear += ('Jeans/chinos', n_jeans, 'Consider customizing based on weather')
    # --- Dress pants
    if dress_days > 2:
        daily_wear += ('Dress pants', 2,
                       "Reduce if you'll have a chance to do laundry")
    elif dress_days > 0:
        daily_wear += ('Dress pants', 1)
    # --- Dress shirts
    n_dress_shirts = dress_days
    if can_wash and is_flying:
        n_dress_shirts = math.ceil(n_dress_shirts / 2)
    daily_wear += ('Dress shirts', n_dress_shirts)
    # --- Dress socks
    n_nice_socks = max(n_jeans + n_dress_pants, n_days_wash)
    daily_wear += ('Nice socks', n_nice_socks)
    # --- Tshirts
    daily_wear += ('T-shirts', n_days_wash - 1)
    # --- Belts
    if dress_days > 0:
        daily_wear += ('Belts', 1)
    # --- Decent shoes
    if dress_days > 0:
        daily_wear += ('Decent shoes', 1)
    elif n_days_wash > 2 and n_jeans > 0:
        daily_wear += ('Decent shoes', 'Optional')
    # --- Polos/buttondowns
    n_polos = min(n_days_wash - 2, 2) if n_days_was > 2 else 1
    daily_wear += ('Casual polos/buttondowns', n_polos)

    workout = []
    return {
        'daily_wear': daily_wear,
        [
            ('shoes', 2, 'remember these'),
            ('socks', 2)
        ],
        'headwear': [
            ('hat', 1)
        ]
    }

