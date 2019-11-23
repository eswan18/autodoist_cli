import os
from pathlib import Path

import click

import util.travel_checklist as tc_util

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
@click.option('--json-file', 
              help='json file with specification of checklist')
@click.option('--yaml-file', 
              help='yaml file with specification of checklist')
def create(json_file, yaml_file):
    '''Create a new travel checklist.'''
    if json_file is not None and yaml_file is not None:
        msg = 'At most one of --json-file and --yaml-file may be specififed'
        raise ValueError(msg)
    elif json_file is not None:
        specs = tc_util.load_specs_from_file(json_file, format='json')
    elif yaml_file is not None:
        specs = tc_util.load_specs_from_file(yaml_file, format='yaml')
    else:
        # Interactively prompt the user for specs.
        specs = tc_util.get_specs_from_user()
    # Extended outdoor time may not be included in the spec; assume it's false.
    specs['extended_outdoor_time'] = specs.get('extended_outdoor_time', False)

    # Create the CSV.
    csv_path = Path(specs['csv_name'])
    if csv_path.exists():
        msg = '{} already exists. Do you want to overwrite it?'
        click.confirm(msg.format(csv_path), abort=True)
    with open(csv_path, 'w') as f:
        csv_content = tc_util.gen_travel_checklist_csv_from_specs(specs)
        f.write(csv_content)
    abs_path = str(csv_path.absolute())
    click.echo('CSV written to file: {}'.format(abs_path))


if __name__ == '__main__':
    cli()
