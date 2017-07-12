import os
import redis
import logging
import datetime

from flask import Flask , send_from_directory, render_template, url_for, request

#Redis instance from heroku
r = redis.from_url(os.environ.get("REDIS_URL"), db =None, decode_responses = True)

app = Flask(__name__)

FAIL_MESSAGE = 'la pulenta oe'

#"Landing page"
@app.route('/')
def webprint():
    return render_template('index.html')

#Saves the string <strng> in the DB
@app.route('/db/<strng>')
def saveInDB(strng):
    r.lpush('db', '%s' % strng)
    return 'OK'

#Recalls the stored info in the DB
@app.route('/db/recall/test', methods = ['GET'])
def recallDB():
    try:
        return str(r.lrange('db', 0, -1))
    except Exception as error:
        return formatError(error)

#DevMode Handling---------------------------------------------

#Returns devMode.html [GET] #Checks login credentials [POST]
@app.route('/devMode', methods = ['POST', 'GET'])
def devMode():

    if request.method == 'GET':
        r.incr('devModeGet')
        return render_template('devMode.html')
    elif request.method == 'POST':
        pss = request.get_json() or request.form #Matching Axios request type
        if checkPassword(pss['password'], pss['info']):
            return os.environ.get('PASSWORD_MESSAGE')
        else:
            return FAIL_MESSAGE
    else: #Message for other methods (DELETE, PUT, CONNECT, ...)
        return '¿?'

#Recalls the failed log attemps of devMode
@app.route('/devMode/recall/logAttempts', methods = ['POST'])
def recallLogAttempts():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        try:
            return str(r.lrange('devModeGetList', 0, -1))[1:-2]
        except Exception as error:
            return formatError(error)
    else:
        return FAIL_MESSAGE

#Recalls the times devMode's URL was accessed
@app.route('/devMode/recall/getTimes', methods = ['POST'])
def recallGetTimes():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        try:
            return str(r.get('devModeGet'))
        except Exception as error:
            return formatError(error)
    else:
        return FAIL_MESSAGE

#Checks for password and logs failed attempts 
def checkPassword(password, info):
    date = str(datetime.datetime.utcnow())
    attempt = password == os.environ.get('REDIS_URL')
    if not attempt:
        r.lpush('devModeGetList', "Info: " + info + " --- " + "Timestamp: " + date + " // Attempt: " + password + "\n")
    return attempt

#Format function to redis errors
def formatError(error):
    msg = 'Type: ' + type(error) + '\n'
    msg += 'Exception: ' + error
    return msg