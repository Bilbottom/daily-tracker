<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![unit-tests](https://github.com/Bilbottom/daily-tracker/actions/workflows/unit-tests.yaml/badge.svg)](https://github.com/Bilbottom/daily-tracker/actions/workflows/unit-tests.yaml)
[![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/daily-tracker)](https://shields.io/)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/daily-tracker/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/daily-tracker/main)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

</div>

# Daily Tracker

An application for keeping track of tasks throughout the day.

## About

Not sure where all your time goes? I wasn't either, so this application generates a pop-up box every 15 minutes (configurable) for me to enter what I'm working on.

## Resources

The clock icon is from [icons8.com](https://icons8.com/):

- https://icons8.com/icon/2YPST59G2xJZ/clock

## Form UI

The form UI is currently built with [tkinter](https://docs.python.org/3/library/tkinter.html) and looks like:

![tkinter-form](tracker-form-tkinter.png)

## Commits

This project uses a mix of [Conventional Commits](https://www.conventionalcommits.org/en) and [gitmojis](https://gitmoji.dev/) for its commit messages. The commit types used follow the [Angular convention](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines) and are:

- `build`: Changes that affect the build system, external dependencies, or CI
- `chore`: Updating grunt tasks etc; no production code change
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `test`: Adding missing tests or correcting existing tests

## Dependencies

On macOS, you may need to install the Tcl/Tk framework:

```bash
brew install tcl-tk
```

More details available at:

- https://tkdocs.com/tutorial/install.html#install-macos
