from flask import Blueprint
from app.models import Send
from app import db
from app.api import bp
import sqlalchemy as sa
from flask import request
from flask import url_for
from app.api.errors import bad_request


send_bp = Blueprint('send', __name__)

@bp.route('/sned/<int:id>', methods=['GET'])
def get_user(id):
    return db.get_or_404(Send, id).to_dict()