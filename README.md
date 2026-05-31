# API testing of the Restful App

This project is designed for automated API testing of the [Restful App](https://berpress.github.io/flask-restful-api/).
It includes tests to verify various aspects of the API, ensuring the stability and quality of the service.

## Technologies Used

The project contains automated tests written in Python utilizing the following technologies:

- [Pytest](https://docs.pytest.org/en/stable/) — testing framework for organizing and running tests
- [HTTPX](https://www.python-httpx.org/) — library for making HTTP requests
- [Allure](https://allurereport.org/) — generating detailed and attractive test reports
- [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/) — API data validation and modeling
- [Faker](https://faker.readthedocs.io/en/master/) - generates fake data for tests
- [Fixtures](./fixtures) — Pytest fixtures for reusable setup and teardown logic
- [Logging](./tools/logger.py) —  logging test execution details
- [pytest-xdist](https://pypi.org/project/pytest-xdist/) - plugin for running tests in parallel
- [Docker](https://docs.docker.com/get-started/docker-overview/) — containerization of the testing environment
- **CI/CD** — automated test runs via GitHub Actions and GitLab CI/CD

### Test results

[Allure Report on GitHub Pages](https://rosemqa.github.io/QA_API_HTTPX_RestfullApp/2/index.html)

---
*This project is intended for learning and practicing automated API testing.*