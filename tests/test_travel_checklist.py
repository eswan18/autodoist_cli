from autodoist import cli
from pathlib import Path
from click.testing import CliRunner
import pytest
import json

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
def test_create_interactive_invocation(trip):
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
