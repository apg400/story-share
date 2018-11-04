#contains main instance of Flask app

import os

from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'story_share.sqlite'),
	)

	if (test_config is None):
		# load the instancee config when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import feed
	app.register_blueprint(feed.bp)
	app.add_url_rule('/', endpoint='index')

	from . import user
	app.register_blueprint(user.bp)

	return app