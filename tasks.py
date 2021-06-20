import os
from pathlib import Path
from shutil import which

from invoke import task

PKG_NAME = "seo"
PKG_PATH = Path(f"pelican/plugins/{PKG_NAME}")
BIN_DIR = "bin" if os.name != "nt" else "Scripts"
ACTIVE_VENV = os.environ.get("VIRTUAL_ENV", None)
VENV_HOME = Path(os.environ.get("WORKON_HOME", "~/.local/share/virtualenvs"))
VENV_PATH = Path(ACTIVE_VENV) if ACTIVE_VENV else (VENV_HOME / PKG_NAME)
VENV = str(VENV_PATH.expanduser())
VENV_BIN = Path(VENV) / Path(BIN_DIR)
TOOLS = ["black", "flake8", "isort", "poetry", "pre-commit", "pytest"]


def find_tool(tool):
    """Locate a tool and return its path, preferring the local virtual environment"""
    t = VENV_BIN / tool
    t = t if t.is_file() else which(tool)

    return t


@task
def tests(c):
    """Run the test suite"""
    pytest = find_tool("pytest")
    c.run(f"{pytest}", pty=True)


@task
def black(c, check=False, diff=False):
    """Run Black auto-formatter, optionally with --check and/or --diff"""
    check_flag, diff_flag = "", ""
    if check:
        check_flag = "--check"
    if diff:
        diff_flag = "--diff"
    black = find_tool("black")
    c.run(f"{black} {check_flag} {diff_flag} {PKG_PATH} tasks.py")


@task
def isort(c, check=False, diff=False):
    """Run isort import sorter, optionally with -c and/or --diff"""
    check_flag, diff_flag = "", ""
    if check:
        check_flag = "-c"
    if diff:
        diff_flag = "--diff"
    isort = find_tool("isort")
    c.run(f"{isort} {check_flag} {diff_flag} .")


@task
def flake8(c):
    flake8 = find_tool("flake8")
    c.run(f"{flake8} {PKG_PATH} tasks.py")


@task
def lint(c, diff=False):
    """Check code style via linting tools."""
    isort(c, check=True, diff=diff)
    black(c, check=True, diff=diff)
    flake8(c)


@task
def tools(c):
    """Install tools in the virtual environment if not already on PATH"""
    for tool in TOOLS:
        if not which(tool):
            c.run(f"{VENV_BIN}/pip install {tool}")


@task
def precommit(c):
    """Install pre-commit hooks to .git/hooks/pre-commit"""
    precommit = find_tool("pre-commit")
    c.run(f"{precommit} install")


@task
def setup(c):
    c.run(f"{VENV_BIN}/pip install -U pip")
    tools(c)
    poetry = find_tool("poetry")
    c.run(f"{poetry} install")
    precommit(c)
