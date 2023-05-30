# Create Automatic Documentation for the Peter Algorithm with Sphinx

The documentation for the Peter Algorithm can be generated automatically using Sphinx, a powerful documentation generation tool for Python. For a high quality result, proper doc-strings are essential since Sphinx uses them to generate the documentation.

## Installation

First, make sure you have Sphinx and the Karma Sphinx theme installed. You can do this by running:

`pip install sphinx==6.2.1 karma-sphinx-theme`


## Steps for Creating Documentation from Scratch

To create the documentation, follow these steps:

1. From within the root directory of the project run `sphinx-quickstart docs`. Answer "yes" to the first prompt and customize the rest according to your preferences.
2. After running the quickstart command, generate the documentation by running `sphinx-build -b html docs/source/ docs/build/html`. This will generate the necessary files for the documentation in the "build" and "source" folders.
3. Configure the `conf.py` file in the "docs/source":
    - Add the `peters_algorithm` folder to the system path
    - Apply the installed theme
    - Use relevant extensions such as 'sphinx.ext.duration', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary', and 'sphinx.ext.viewcode'
4. Run `sphinx-apidoc -M -P -e -d 5 -f -o docs/source/ peters_algorithm/` from the root folder to generate API documentation for the `peters_algorithm` module. The individual flags mean: 
    - -M: put module documentation before submodule documentation
    - -P: include “_private” modules
    - -e: put documentation for each module on its own page to correctly display .py files as submodules
    - -d: set max toc depth to 5
    - -f: force overwriting of any existing generated files
    - -o: specifies the output directory
5. Run `make html` from within the "docs" folder to generate the HTML files.
6. Open `docs/build/html/index.html` to view the generated documentation.

## Steps for Updating Documentation
0. Only after the first pull of the repository (since the build folder is ignored by git), run `sphinx-build -b html docs/source/ docs/build/html` to generate the necessary files for the documentation in the "build" folder.
1. Run `sphinx-apidoc -M -P -e -d 5 -f -o docs/source/ peters_algorithm/` from the root folder to generate API documentation for the `peters_algorithm` module.
2. Run `make html` from within the "docs" folder to generate the HTML files.
3. Open `docs/build/html/index.html` to view the generated documentation.

That's it! With Sphinx, you can easily generate high-quality documentation :)
