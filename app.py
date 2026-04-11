from flask import Flask
from config import Config
from routes import main_blueprint, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    bcrypt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=app.config['DEBUG'], port=5001)
