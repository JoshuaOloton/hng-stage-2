from api import create_app
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
    return 'HNG11 Backend Track Stage 1!'

if __name__ == '__main__':
    # app.run(debug=True, port=3000)
    # serve(app, host='127.0.0.1', port=8080)
    serve(TransLogger(app, setup_console_handler=False), host='127.0.0.1')