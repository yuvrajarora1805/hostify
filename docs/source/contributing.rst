Contributing
============

We welcome contributions to Hostify! This guide will help you get started.

How to Contribute
-----------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** and test them
5. **Submit a pull request**

Development Setup
-----------------

Clone the repository:

.. code-block:: bash

   git clone https://github.com/yuvrajarora1805/hostify.git
   cd hostify

Install in development mode:

.. code-block:: bash

   pip install -e .

Install development dependencies:

.. code-block:: bash

   pip install pytest black flake8 mypy

Running Tests
-------------

Run the test suite:

.. code-block:: bash

   python tests/test_suite.py

Expected output:

.. code-block:: text

   Results: 9/9 tests passed (100%)
   All tests passed! Library is ready for publication.

Code Style
----------

We follow PEP 8 style guidelines. Format your code with Black:

.. code-block:: bash

   black hostify/

Check with flake8:

.. code-block:: bash

   flake8 hostify/

Type Checking
-------------

We use type hints throughout the codebase. Check types with mypy:

.. code-block:: bash

   mypy hostify/

Submitting Changes
------------------

1. **Create a descriptive branch name:**

   .. code-block:: bash

      git checkout -b feature/add-new-feature

2. **Make your changes** with clear commit messages

3. **Test your changes** thoroughly

4. **Push to your fork:**

   .. code-block:: bash

      git push origin feature/add-new-feature

5. **Open a pull request** on GitHub

Pull Request Guidelines
------------------------

- **Describe your changes** clearly in the PR description
- **Reference any related issues** (e.g., "Fixes #123")
- **Include tests** for new features
- **Update documentation** if needed
- **Follow the existing code style**
- **Keep PRs focused** - one feature/fix per PR

Reporting Bugs
--------------

Found a bug? Please open an issue on GitHub with:

- **Python version** (``python --version``)
- **Hostify version** (``pip show hostify``)
- **Operating system**
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Error messages** (full traceback if available)

Feature Requests
----------------

Have an idea for a new feature? Open an issue with:

- **Clear description** of the feature
- **Use case** - why is this useful?
- **Proposed implementation** (if you have ideas)

Code of Conduct
---------------

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

License
-------

By contributing, you agree that your contributions will be licensed under the MIT License.

Questions?
----------

Feel free to open an issue for any questions about contributing!
