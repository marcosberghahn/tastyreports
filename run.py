from dotenv import load_dotenv
from tastyreports import app
import os

load_dotenv()
DEBUG = os.getenv('DEBUG', False)
PORT = os.getenv('PORT', 5000)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
