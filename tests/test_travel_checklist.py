from autodoist import cli
from click.testing import CliRunner

def test_general_invocation():
    runner = CliRunner()
    runner.invoke(cli, ['travel-checklist'])
