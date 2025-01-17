from api import create_app
from api import db
from api.models import User, Organisation
from waitress import serve
from paste.translogger import TransLogger
import logging
import os
from flask import jsonify


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = create_app('production')

@app.route('/')
def home():
    return jsonify({
        "message": "HNG11 Backend Track Stage 2!"
    })


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Organisation': Organisation}

@app.cli.command("init_db")
def init_db():
    db.create_all()

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()

if __name__ == '__main__':
    port = os.getenv('PORT', 3000)
    # app.run(debug=True, port=3000)
    serve(TransLogger(app, setup_console_handler=False), host='0.0.0.0', port=port)