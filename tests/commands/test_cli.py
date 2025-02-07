import BALSAMIC


def test_cli(invoke_cli):
    # GIVEN I want to see version of the program
    # WHEN I am asking to see version
    result = invoke_cli(["--version"])

    # THEN It should show the version of the program
    assert BALSAMIC.__version__ in result.output


def test_config(invoke_cli):
    # GIVEN I want to see config command options
    # WHEN asking to show config options
    result = invoke_cli(["config"])

    # THEN It should show config options in result
    assert "case" in result.output


def test_config_case(invoke_cli):
    # GIVEN want to see config-sample params with help option
    # WHEN asking to show params for config-sample
    result = invoke_cli(["config", "case", "--help"])

    # THEN It should show all params reuired for config-sample
    assert "sample-id" in result.output
    assert result.exit_code == 0


def test_config_case_missing_opt(invoke_cli):
    # WHEN invoking command with missing options
    result = invoke_cli(["config", "case"])

    # THEN It should throw missing option error
    assert "Error: Missing option" in result.output
    assert result.exit_code == 2


def test_report_deliver(invoke_cli):
    # WHEN invoking command with missing options
    result = invoke_cli(["report", "deliver", "--help"])

    # THEN It should throw missing option error
    assert result.exit_code == 0


def test_report_status(invoke_cli):
    # WHEN invoking command with missing options
    result = invoke_cli(["report", "status", "--help"])

    # THEN It should throw missing option error
    assert result.exit_code == 0


def test_plugins(invoke_cli):
    # GIVEN want to see config-sample params with help option
    # WHEN asking to show params for config-sample
    result = invoke_cli(["plugins", "--help"])

    # THEN It should show all params reuired for config-sample
    assert result.exit_code == 0


def test_plugins_scout(invoke_cli):
    # WHEN invoking command with missing options
    result = invoke_cli(["plugins", "scout", "--help"])

    # THEN It should throw missing option error
    assert result.exit_code == 0


def test_run(invoke_cli):
    # WHEN asking to options for run command
    result = invoke_cli(["run", "--help"])

    # THEN It should show all the params without any error
    assert result.exit_code == 0
    assert "analysis" in result.output


def test_run_analysis(invoke_cli):
    # WHEN invoking run analysis command
    result = invoke_cli(["run", "analysis", "--help"])

    # THEN it should show all params without error
    assert "--snake-file" in result.output
    assert "--sample-config" in result.output
    assert "--run-mode" in result.output
    assert "--cluster-config" in result.output
    assert "--run-analysis" in result.output


def test_run_missing_opt(invoke_cli):
    # WHEN invoking run command with missing option
    result = invoke_cli(["run", "analysis"])

    # THEN It should throw missing option error
    assert "Error: Missing option" in result.output
    assert result.exit_code == 2


def test_run_analysis_invalid(invoke_cli):
    # WHEN invoking run with invalid input value
    result = invoke_cli(["run", "analysis", "--run-mode", "foo"])

    # THEN It should throw invalid value error
    assert result.exit_code == 2
    assert "Error: Invalid value" in result.output
