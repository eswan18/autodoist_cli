from pathlib import Path
import json
import tempfile

from click.testing import CliRunner
import pytest

from autodoist import cli

KEY_ORDER = ['name', 'csv_name', 'n_days', 'can_wash', 'is_flying',
             'dress_days', 'max_temp', 'min_temp', 'extended_outdoor_time']

# Load trips to use as parameters.
with open('tests/data/trips.json') as f:
    trips = json.loads(f.read())

# Making the trips into a fixture allows us to run each test on every trip, as
# well to do some setup and teardown.
@pytest.fixture(params=trips)
def trip(request):
    # Extract bits we need.
    _trip = request.param
    trip_name = _trip['spec']['name']
    csv_name = _trip['spec'].get('csv_name', trip_name + '.csv')
    csv_file = Path(csv_name)
    # Setup ####
    yield _trip
    # Teardown ####
    # Delete the created output files.
    if csv_file.exists():
        csv_file.unlink()
    

def test_general_invocation():
    runner = CliRunner()
    result = runner.invoke(cli, ['travel-checklist'])
    assert result.exit_code == 0

def test_create_interactive(trip):
    spec = trip['spec']
    runner = CliRunner()
    # Create the user input.
    input = '\n'.join([str(spec[key]) for key in KEY_ORDER])
    result = runner.invoke(cli, ['travel-checklist', 'create'],
                           input=input)
    assert result.exit_code == 0
    out_path = Path(spec['csv_name'])
    conf_text = 'CSV written to file: {}'.format(str(out_path.absolute()))
    assert conf_text in result.output

def test_create_json_file(trip):
    runner = CliRunner()
    # Use a temp file to store the trip json for the duration of the test.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f_json:
        f_json.write(json.dumps(trip['spec']))
        f_json.seek(0)
        result = runner.invoke(cli, ['travel-checklist', 'create',
                                     '--json-file', f_json.name])
    assert result.exit_code == 0

