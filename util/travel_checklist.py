import click

JACKET_TEMP_THRESHOLD = 50
COAT_TEMP_THRESHOLD = 40
GLOVES_TEMP_THRESHOLD = 35

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

def gen_travel_checklist_csv_from_specs(specs):
    return ''
