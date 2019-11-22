from autodoist import cli
from pathlib import Path
from click.testing import CliRunner

def test_general_invocation():
    runner = CliRunner()
    result = runner.invoke(cli, ['travel-checklist'])
    assert result.exit_code == 0

def test_create_invocation():
    OUT_FILE = 'test-trip.csv'
    runner = CliRunner()
    result = runner.invoke(cli, ['travel-checklist', 'create'],
                           input='''test-trip\n{}
                                    7\nn\ny\n1
                                    78\n45\ny\ny'''.format(OUT_FILE))
    assert result.exit_code == 0
    assert Path(OUT_FILE).exists()
