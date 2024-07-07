from api import create_app
from api import db
from api.models import User, Organisation
from waitress import serve
from paste.translogger import TransLogger
import logging
from dotenv import load_dotenv


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

load_dotenv()
app = create_app()

@app.route('/')
def home():
    return 'HNG11 Backend Track Stage 2!'


# @app.errorhandler(404)
# def page_not_found(e):
#     return '404 Error', 404

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
    app.run(debug=True, port=3000)
    # serve(app, host='127.0.0.1', port=8080)
    # serve(TransLogger(app, setup_console_handler=False), host='127.0.0.1')