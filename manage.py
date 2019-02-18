from main import app
from models import db, Player, Team, City


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Player=Player, Team=Team, City=City)
