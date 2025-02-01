import nox
import os

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
        "coverage",
        "run",
        "--rcfile=.coveragerc",
        "-m",
        "pytest",
        "-W",
        "error",
        "-ra",
        "-v",
        "--pyargs",
        "trio_monitor",
        "--verbose",
        *session.posargs,
    )
    session.notify("coverage")


@nox.session(default=False)
def coverage(session):
    session.install("-r", "test-requirements.txt")
    session.run("coverage", "combine")
    session.run("coverage", "report")

    os.remove(".coverage")
