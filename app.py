from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS, cross_origin

from models import db_session
from schema import schema

app = Flask(__name__)
cors = CORS(app, resources={r'/graphql': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__== '__main__':
    app.run()
