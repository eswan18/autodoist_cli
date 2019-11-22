#!/usr/bin/env python
import click
import json
import os
import pathlib

JACKET_TEMP_THRESHOLD = 50
COAT_TEMP_THRESHOLD = 40
GLOVES_TEMP_THRESHOLD = 35

@click.group()
def cli():
    pass

@cli.command()
def test():
    click.echo('hi!')

@cli.group(name='travel-checklist')
def travel_checklist():
    pass

@travel_checklist.command()
@click.option('--file', 
              help='json file with specification of checklist')
def create(file):
    '''Create a new travel checklist.'''
    if file is not None:
        try:
            with open(file) as f:
                specs = json.loads(f.read())
        except json.decoder.JSONDecodeError as e:
            # Raise a JSONDecodeError with a better message than the automatic
            # one.
            msg = 'File {} is not valid JSON'.format(file)
            raise json.decoder.JSONDecodeError(msg, doc=e.doc, pos=e.pos)
    else:
        specs = get_specs_from_user()
    # Extended outdoor time may not be included in the spec; assume it's false.
    specs['extended_outdoor_time'] = specs.get('extended_outdoor_time', False)

    # Create the CSV.
    csv_path = pathlib.Path(specs['csv_name'])
    if csv_path.exists():
        click.confirm('{} already exists. Do you want to overwrite it?',
                      abort=True)
    with open(csv_path, 'w') as f:
        csv_content = gen_travel_checklist_csv_from_specs(specs)
        f.write(csv_content)
    abs_path = str(csv_path.absolute())
    click.echo('CSV written to file: {}'.format(abs_path))

def get_specs_from_user():
    name = click.prompt('Name for the project')
    csv_name = click.prompt('Name of template file to be created')
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
    # If it's already cool enough that you'll need a jacket and you'll be
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

if __name__ == '__main__':
    cli()
