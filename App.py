from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import coba

app = Flask(__name__)
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
    return redirect(url_for('login'))


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


@app.route('/likeperview/<string:userID>', methods=['GET'])
def likeperview(userID):
    if 'google_token' in session:
        data = coba.channel_query(userID)
        return jsonify({
        'Channel Name': data['snippet']['title'],
        'Likes Count' : data['statistics']['videoCount'],
        'Views Count' : data['statistics']['viewCount'],
        'Engagement Rate' : '20%'})
    return redirect(url_for('login'))

@app.route('/commentperview/<string:userID>', methods=['GET'])
def commentperview(userID):
    if 'google_token' in session:
        data = coba.channel_query(userID)
        return jsonify({
        'Channel Name': data['snippet']['title'],
        'Comment Count' : data['statistics']['commentCount'],
        'Views Count' : data['statistics']['viewCount'],
        'Engagement Rate' : '20%'})
    return redirect(url_for('login'))

@app.route('/subscriberperview/<string:userID>', methods=['GET'])
def subscriberperview(userID):
    if 'google_token' in session:
        data = coba.channel_query(userID)
        cname = data['snippet']['title']
        vc = int(data['statistics']['viewCount'])
        sc = int(data['statistics']['subscriberCount'])
        er = round(float(sc/vc*100),2)
        return jsonify({
        'Channel Name': cname,
        'Subscribers Count' : sc,
        'Views Count' : vc,
        'Engagement Rate' :  "{} %".format(er)})
    return redirect(url_for('login'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
