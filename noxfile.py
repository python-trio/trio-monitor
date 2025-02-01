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
    run_tests(session)


@nox.session(venv_backend="uv")
def test_oldest(session):
    pyver = session.run("python", "--version", silent=True)
    pyver = ".".join(pyver.split(" ")[1].split(".")[:2])
    # based on classifiers
    possible_trio = {
        "3.13": "trio>=0.26.0",
        "3.12": "trio>=0.23.0",
        "3.11": "trio>=0.21.0",
        "3.10": "trio>=0.20.0",
        "3.9": "trio>=0.19.0",
        "3.8": "trio",
    }

    session.install(".", possible_trio[pyver], "--resolution=lowest-direct")
    session.install("pip")
    versions = session.run("pip", "freeze", silent=True)

    # make sure we don't change the trio version
    session.install(
        "-r",
        "test-requirements.txt",
        *[line for line in versions.split() if line.startswith("trio==")],
    )

    run_tests(session)


def run_tests(session):
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
