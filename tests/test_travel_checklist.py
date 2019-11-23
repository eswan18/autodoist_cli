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

def test_general_invocation():
    runner = CliRunner()
    result = runner.invoke(cli, ['travel-checklist'])
    assert result.exit_code == 0

@pytest.mark.parametrize('trip', trips)
def test_create_interactive(trip):
    spec = trip['spec']
    runner = CliRunner()
    # Create the user input.
    input = '\n'.join([str(spec[key]) for key in KEY_ORDER])
    # We may be prompted to overwrite a file.
    out_path = Path(spec['csv_name'])
    if out_path.exists():
        input += '\ny'
    result = runner.invoke(cli, ['travel-checklist', 'create'],
                           input=input)
    assert result.exit_code == 0
    conf_text = 'CSV written to file: {}'.format(str(out_path.absolute()))
    assert conf_text in result.output

@pytest.mark.parametrize('trip', trips)
def test_create_json_file(trip):
    runner = CliRunner()
    # Use a temp file to store the trip json for the duration of the test.
    with tempfile.NamedTemporaryFile(mode='w', suffix='json') as f:
        f.write(json.dumps(trip['spec']))
        f.seek(0)
        result = runner.invoke(cli, ['travel-checklist', 'create',
                                 '--json-file', f.name, '--overwrite'])
    assert result.exit_code == 0

