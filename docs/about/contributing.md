# For Contributors

## Setup

### Requirements

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

### Installation

Create a virtual environment:

```
$ make env
```

## Development Tasks

### Care about code quality

Follow Python, OOP and other good conventions.

Follow those conventions:

* [PEP0008](https://www.python.org/dev/peps/pep-0008/)
* [PEP0257](https://www.python.org/dev/peps/pep-0257/)
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

#### Docstrings
Create meaningful dosctrings using [Google Docstring Format.](http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html)
Add types in docstrings.

### Testing

Manually run the tests:

```
$ make test
$ make tests  # includes integration tests
```

or keep them running on change:

```
$ make watch
```

> In order to have OS X notifications, `brew install terminal-notifier`.

### Documentation

Build the documentation:

```
$ make doc
```

### Static Analysis

Run linters and static analyzers:

```
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

### Commiting to master

1. Check that code pass all CI tests on your machine 
2. Create Pull request and recheck that all CI tests are green.
3. If owner of repo approve your changes then merge to master.

#### Pull Requests

1. Each commit in PR should represent one independent working functionality.
2. After merging your PR to master remove your branch.

## Continuous Integration

The CI server will report overall build status:

```
$ make ci
```

## Release Tasks

Release to PyPI:

1. Update version in file `grortir/__init__.py` to `your.version`
2. Check and update `CHANGES.md` file.
3. Commit changes in branch `release/your.version`
4. Upload package:
```
$ make upload-test  # dry run upload to a test server, if success upload to real pypi
$ make upload
```
5. Check success of upload on [Grortir PyPI](https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=Grortir) site and fix if needed.

