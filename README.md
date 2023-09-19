# Nimb-test

## Usage

To use this project, you need to have Docker installed on your machine. If you don't have Docker installed, you can download and install it from the official Docker website: [https://www.docker.com/get-started](https://www.docker.com/get-started)

To build the project, run the following command:
`make build`

To run the project, use the following command:

`make run`

To stop the project, run the following command:

`make stop`

To run tests, use the following command:

`make test`

## Configuration

The project can be configured using the following environment variables:

APP_ENV: The environment in which the application is running. Default: local.
APP_URL: The URL of the application. Default: http://localhost.
CORS_ALLOWED_ORIGINS: Allowed origins for Cross-Origin Resource Sharing (CORS) in other environments. Default: "\*".

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## WIP

- Writing more tests
