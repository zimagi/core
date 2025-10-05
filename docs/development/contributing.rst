Contributing and Development
============================

We welcome community contributions! Please review these guidelines before submitting pull requests.

Contribution Workflow
---------------------

1.  **Fork the Repository**: Start by forking the main Zimagi repository to your GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local development machine.
3.  **Create a New Branch**: For each new feature or bug fix, create a new branch from the `main` branch. Use descriptive names (e.g., `feature/my-new-feature`, `bugfix/fix-login-issue`).
4.  **Make Your Changes**: Implement your feature or fix the bug. Ensure your code adheres to Zimagi's coding standards (see below).
5.  **Write Tests**: Add or update unit and integration tests to cover your changes.
6.  **Run Tests**: Before submitting, run the full test suite to ensure no regressions are introduced.
7.  **Commit Your Changes**: Write clear and concise commit messages.
8.  **Push to Your Fork**: Push your branch to your forked repository on GitHub.
9.  **Create a Pull Request (PR)**: Open a pull request against the `main` branch of the original Zimagi repository. Provide a detailed description of your changes, including why they are needed and how they were tested.

Coding Standards
----------------
*   **Python**: Adhere to PEP 8. Use type hints where appropriate.
*   **JavaScript/TypeScript**: Follow ESLint and Prettier configurations provided in `sdk/javascript/.eslintrc.cjs` and `sdk/javascript/.prettierrc`.
*   **Documentation**: Update relevant documentation (including `README.rst` files and Sphinx documentation) for any new features or changes.

Running Tests
-------------
The `app/tests/` directory serves as the central hub for all automated tests. To run the test suite, ensure a Docker daemon is running and Zimagi services are up. The tests interact with the Zimagi Command API and Data API, typically exposed via HTTP endpoints.

To execute the tests:

.. code-block:: bash

    python manage.py test

For more details on testing, refer to :doc:`testing`.

License
-------
This project is licensed under the **Apache 2 License**.
