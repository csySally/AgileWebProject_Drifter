from app import app, db
from app.models import User, Send, Reply, Labels

@app.shell_context_processor
def make_shell_context():
 return {'db': db, 'User': User, 'Send': Send, 'Reply': Reply, 'Labels': Labels}