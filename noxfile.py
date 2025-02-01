import nox
import os

nox.options.reuse_venv = "yes"
nox.options.error_on_external_run = True

# TODO: nox.needs_version
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def precommit(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session
def test(session):
    session.install(".")
    session.install("-r", "test-requirements.txt")
    session.run(
        "coverage",
        "run",
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

    if os.environ.get("CI") != "true":
        session.notify("coverage")


@nox.session(default=False)
def coverage(session):
    session.install("-r", "test-requirements.txt")
    session.run("coverage", "combine")
    session.run("coverage", "report")

    os.remove(".coverage")
