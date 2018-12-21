from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import coba, calc

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
        <img src="{}" alt="Red dot" />
        <a href="http://127.0.0.1:5000/logout"> Logout </a >
        </div>
        '''.format(me.data["given_name"],me.data["picture"])
        return jsonify({"data": me.data})
    return '''
    <div>
    <h1>Hello There, Welcome to Youtube Engagement Calculator!</h1>
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
