# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import query_fromYAPI, calc

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['GOOGLE_ID'] = "615677142223-hcjeucs12o40tf2jaoeqs3t4e5kd267m.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "0PPZlYAhe18vY4vqmvIlEDpu"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)



@app.route('/tes')
def tes():
        return '''
        <div>
        <h1>Hello there!</h1>
        <a href="http://127.0.0.1:5000/logout"> Logout </a >
        </div>
        '''

@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return '''
        <div>
        <h1>Hello {}!</h1>
        <h2> Here's our available API for <b> Youtube Engagement Calculator </b> </h2>
        <li> <b> SUMMARY </b> </li>
        <p> <i> /summary/channelID </i> </p>
        <p> mengeluarkan semua perhitungan engagement rate dari sebuah channel </p>
        <li> <b> LIKE PER VIEW </b> </li>
        <p> <i> /likeperview/channelID </i> </p>
        <p> mengeluarkan jumlah like per jumlah view dari sebuah channel </p>
        <li> <b> COMMENT PER VIEW </b> </li>
        <p> <i> /commentperview/channelID </i> </p>
        <p> mengeluarkan jumlah comment per jumlah view dari sebuah channel </p>
        <li> <b> SUBSCRIBER PER VIEW </b> </li>
        <p> <i> /subscriberperview/channelID </i> </p>
        <p> mengeluarkan rata-rata jumlah subscriber per jumlah view dari sebuah channel </p>

        <a href="http://127.0.0.1:5000/logout"> Logout </a >
        </div>
        '''.format(me.data["given_name"])
        return jsonify({"data": me.data})
    return '''
    <div>
    <h1>Hello There,  </h1>
    <h1>Welcome to Youtube Engagement Calculator!</h1>
    <h2>Please authenticate yourself before using our API </h2>
    <a href="/login"> Login Using Google </a >
    </div>
    '''


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return redirect(url_for('index'))

@app.route('/summary/<string:userID>', methods=['GET'])
def summary(userID):
    if 'google_token' in session:
        data = calc.calculate_all(userID)
        return jsonify({
        'Channel Name': data[0],
        'Likes Count' : data[1],
        'Views Count' : data[2],
        'Comment Count' : data[3],
        'Subscriber Count' : data[4],
        'Engagement Rate': {
            'Like Per View': "{} %".format(data[5]),
            'Comment Per View': "{} %".format(data[6]),
            'Subscriber Per View': "{} %".format(data[7]),
            }
        })
    return redirect(url_for('index'))

@app.route('/likeperview/<string:userID>', methods=['GET'])
def likeperview(userID):
    if 'google_token' in session:
        data = calc.calculate_all(userID)
        return jsonify({
        'Channel Name': data[0],
        'Likes Count' : data[1],
        'Views Count' : data[2],
        'Engagement Rate' : {
        'Like Per View' : "{} %".format(data[5])}})
    return redirect(url_for('index'))

@app.route('/commentperview/<string:userID>', methods=['GET'])
def commentperview(userID):
    if 'google_token' in session:
        data = calc.calculate_all(userID)
        return jsonify({
        'Channel Name': data[0],
        'Comment Count' : data[3],
        'Views Count' : data[2],
        'Engagement Rate' :  {
            'Comment per View': "{} %".format(data[6])}})
    return redirect(url_for('index'))

@app.route('/subscriberperview/<string:userID>', methods=['GET'])
def subscriberperview(userID):
    if 'google_token' in session:
        data = calc.calculate_all(userID)
        return jsonify({
        'Channel Name': data[0],
        'Subscribers Count' : data[4],
        'Views Count' : data[2],
        'Engagement Rate' :  {
        'Subscriber Per View': "{} %".format(data[7])}})
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
