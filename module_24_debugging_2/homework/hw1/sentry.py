from flask import Flask, request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging


sentry_sdk.init(
    dsn="https://c04197bd8b0ba936c48d94c2929a6a74@o4505833348530176.ingest.us.sentry.io/4507838830608384",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/test_type')
def test_type():
    user_id = request.args.get('user_id')
    user_id = float(user_id)


@app.route('/test')
def ll():
    raise IndexError


@app.route('/test_logging')
def test_logging():
    logging.error("error to log")


if __name__ == '__main__':
    app.run()