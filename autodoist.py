#!/usr/bin/env python
import click
import json
import os
import pathlib
import travel_checklist_util as tc_util

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
        specs = tc_util.get_specs_from_user()
    # Extended outdoor time may not be included in the spec; assume it's false.
    specs['extended_outdoor_time'] = specs.get('extended_outdoor_time', False)

    # Create the CSV.
    csv_path = pathlib.Path(specs['csv_name'])
    if csv_path.exists():
        click.confirm('{} already exists. Do you want to overwrite it?',
                      abort=True)
    with open(csv_path, 'w') as f:
        csv_content = tc_util.gen_travel_checklist_csv_from_specs(specs)
        f.write(csv_content)
    abs_path = str(csv_path.absolute())
    click.echo('CSV written to file: {}'.format(abs_path))


if __name__ == '__main__':
    cli()
