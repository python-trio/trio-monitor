import nox

nox.options.reuse_venv = "yes"
nox.options.error_on_external_run = True

# TODO: nox.needs_version
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def autoformat(session):
    session.install("black")
    session.run("black", ".")


@nox.session
def test(session):
    session.install(".")
    session.install("-r", "test-requirements.txt")
    session.run(
        "pytest",
        "-W",
        "error",
        "-ra",
        "-v",
        "--pyargs",
        "trio_monitor",
        "--cov=trio_monitor",
        "--cov-config=.coveragerc",
        "--verbose",
    )
