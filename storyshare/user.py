import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from storyshare.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<username>/stories', methods=('GET', 'POST'))
def stories(username):
	db = get_db()
	posts = db.execute(
		'SELECT p.id, title, body, created, author_id, username'
		' FROM post p JOIN user u ON p.author_id = u.id WHERE author_id = ?'
		' ORDER BY created DESC', (g.user['id'],)
	).fetchall()

	if request.method == 'POST':
		print('POST user.stories')
	return render_template('user/stories.html', posts=posts)