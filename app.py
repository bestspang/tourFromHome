#!/usr/bin/env python
# import gevent.monkey
# gevent.monkey.patch_all()
# from gevent.pywsgi import WSGIServer
from settings import ConfigClass
from flask import Flask, render_template, request, jsonify, Blueprint, redirect
from flask import redirect, url_for
from flask_babelex import Babel
from flask_restful import Api
from flask_jwt import JWT
from flask_socketio import SocketIO, send
from flask_user import current_user, login_required, roles_required, UserManager

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.node import Node, NodeList, Activate
from resources.data import Data, DataList

from threading import Thread, Event
from db import db
from models.user import UserModel, UserProfileForm, Role

from dash import Dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt
from tools import get_wind_data
import os

app = Flask(__name__)
app.config.from_object(ConfigClass)

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 10000)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#url_base_pathname
#routes_pathname_prefix
app1 = Dash(__name__,
    server=app,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    routes_pathname_prefix='/app1/',
    external_stylesheets=external_stylesheets
)

app1.config.update({
    # remove the default of '/'
    'routes_pathname_prefix': '',

    # remove the default of '/'
    'requests_pathname_prefix': ''
})
app_color = {"graph_bg": "#FFF", "graph_line": "#007ACE"}
app1.layout = html.Div(
                    [
                        html.Div(
                            [html.H6("TEMPERATURE (℃) SAMPLE TEST", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="wind-speed",
                            figure=go.Figure(
                                layout=go.Layout(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="wind-speed-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="container"
                )

# WIND
@app1.callback(
    Output("wind-speed", "figure"), [Input("wind-speed-update", "n_intervals")]
)
def gen_wind_speed(interval):
    """
    Generate the wind speed graph.

    :params interval: update the graph based on an interval
    """

    total_time = get_current_time()
    df = get_wind_data(total_time - 200, total_time)

    trace = go.Scatter(
        y=df["Speed"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": df["SpeedError"],
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = go.Layout(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#000000"},
        height=500,
        xaxis={
            "range": [0, 60],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 10, 20, 30, 40, 50, 60],
            "ticktext": ["0", "10", "20", "30", "40", "50", "60"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [
                min(0, min(df["Speed"])),
                max(45, max(df["Speed"]) + max(df["SpeedError"])),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df["Speed"].iloc[-1] / 10)),
        },
    )

    return go.Figure(data=[trace], layout=layout)


def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_time


api = Api(app)
babel = Babel(app)

#main_blueprint = Blueprint('main', __name__, template_folder='templates')
def create_users():
    admin_role = Role.find_or_create_role('admin', u'Admin')
    member_role = Role.find_or_create_role('member', u'Member')
    #Create 'member@example.com' user with no roles
    user = UserModel.find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    user = UserModel.find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1', member_role)
    db.session.commit()

@app.before_first_request
def create_tables():
    db.create_all()
    #create_users()

jwt = JWT(app, authenticate, identity)  # /auth

thread = Thread()
thread_stop_event = Event()
socketio = SocketIO(app)

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, UserModel)

@app.route("/")
def home_page():
    return render_template('main/home_page.html')

# The Members page is only accessible to authenticated users
@app.route('/members')
@login_required    # Use of @login_required decorator
def member_page():
    return render_template('main/user_page.html')

# The Admin page requires an 'Admin' role.
@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    return render_template('main/admin_page.html')

@app.route("/dashboard")
def dashboard():
    return render_template('main/dashboard_page.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/chat")
def chat():
    return render_template('main/chat_test.html')

@app.route('/chat', methods=['GET', 'POST'])
def messageReceived():
    print('message was received!!!')

@app.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)

@app.route('/registers', methods=['POST'])
def handle_data():
    register = request.form.to_dict()
    #print(register)
    return "WELCOME {}! YOU ARE LOGED IN! <br /> <br /> <br /> <br /> <br />  I'm Joking :)".format(register['username'])

from models.node import NodeModel
import datetime
t = 0
@app.route('/api', methods=['GET', 'POST'])
def add_message():
    global t
    content = request.get_json()
    time = datetime.datetime.today()
    if content:
        if content['api'] == "kndOFSoiVnSvOEfef7sEFV78s65":
            try:
                print("temp: ", content['temp'])
                print("humid: ", content['humid'])
                # timestamp, name, model, humid, temp, api
                t += 1
                if t == 5:
                    node = NodeModel(time, **content)
                    node.save_to_db()
                    print(t, "save to database!!!")
                    t = 0
                socketio.emit('TempHu', {'temp': content['temp'],'humid': content['humid']}, namespace='/test', broadcast=True)
            except:
                print("error!")
            return jsonify({"Temp": content['temp'], "Humid": content['humid'], "Time": time})
    return jsonify({'message': 'API key is not valid!'})

@socketio.on('message', namespace='/test')
def handleMeassage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on('my event', namespace='/chat')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
# api.add_resource(UserRegister, '/register')
api.add_resource(Node, '/node/<string:uuid>')
api.add_resource(NodeList, '/nodes')
api.add_resource(DataList, '/node/<string:name>/datas')
api.add_resource(Data, '/data/<string:uuid>')
api.add_resource(UserList, '/users')
api.add_resource(Activate, '/activate/<string:name>')


if __name__ == '__main__':
    from db import db
    try:
        db.init_app(app)
    except:
        print("****Expect working on server!****")
    #create_tables()
    #create_users()
    socketio.run(app, debug=False)#port=80
    #app.run(port=5000, debug=True)
