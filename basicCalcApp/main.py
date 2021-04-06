from flask import Flask
from flask import request
from flask import session
from flask_session import Session
import time
import redis
import uuid
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

#Below is the configuration for redistogo from the heroku
#Give your own link and domain and port
#These information can be seen from the Redis To go Addon page fron your Heroku account
#app.config['SESSION_REDIS'] = redis.from_url("redis://:**********************@crestfish.redistogo.com:11693/")

#Uncomment below line if you are planning to test it on a local run 
# i.e. direct run of this code using redis image from the docker
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

#Uncomment below line if you want to test the bundled docker of web and redis
#app.config['SESSION_REDIS'] = redis.from_url('redis://redis:6379')

server_session = Session(app)

#Below is the configuration for the redistogo connection pool
# On the same way you can use your own password, host and port
#connection_pool = redis.ConnectionPool( host='crestfish.redistogo.com', port=11693, password='******************',decode_responses=True) 

#Uncomment below line if you are planning to test it on a local run 
# i.e. direct run of this code using redis image from the docker
connection_pool = redis.ConnectionPool( host='localhost', port=6379, decode_responses=True) 

#Uncomment below line if you want to test the bundled docker of web and redis
#connection_pool = redis.ConnectionPool( host='redis', port=6379, decode_responses=True) 

r = redis.StrictRedis(connection_pool=connection_pool)
@app.route("/")
def index():
    firstnumber = request.args.get("firstnumber", "")
    secondnumber = request.args.get("secondnumber", "")
    user = request.args.get("user", "")
    operator = request.args.get("operation", "")
    result = operation(firstnumber,secondnumber,operator)
    if firstnumber and operator and secondnumber and result:
        r.set(str(uuid.uuid4()),str(firstnumber)+","+str(operator)+","+str(secondnumber)+","+str(result)+","+str(time.time_ns()))
    firstnumberstr = getallvalueredis()
    return (
        """<form action="" method="get">
                Give your name: <input type="text" name="user">
                <h1></h1>        
                Give the first Number: <input type="text" name="firstnumber">
                <h1></h1>
                Give the second Number: <input type="text" name="secondnumber">
                <h1></h1>
                Give the operation: <select type="operation" name="operation">
                                        <option value="Addition">+</option>
                                        <option value="Substraction">-</option>
                                        <option value="Multiplication">x</option>
                                        <option value="Division">/</option>    
                                    </select>                                                                                                                    
                <input type="submit" value="Operation">
            </form>"""
        + "<b>Result: </b>"
        + str(result)
        + "<h1></h1>"
        + "<b><u>Last 10th Calculations: </b></u>"
        + firstnumberstr
    )

def operation(firstnumber,secondnumber,operator):
    """Parameters: It takes the two numbers and the operator which will be applied to the two numbers
       Output: Result of the Operation
       Summary: It is simply doing the basic calculator operations   
    """
    try:
        if operator=="Addition":
            return int(firstnumber)+int(secondnumber)
        elif operator=="Substraction":
            return int(firstnumber)-int(secondnumber)
        elif operator=="Multiplication":
            return int(firstnumber)*int(secondnumber)         
        elif operator=="Division":
            return int(firstnumber)/int(secondnumber)                  
    except ValueError:
        return "invalid input"

def getallvalueredis():
    """Parameters: None
       Output: History from the Redis
       Summary: This function is basically going into the Redis where all our user inputs
                , operators and results are stored. It is exporting those by scanning the keys
                and putting them in a Pandas dataframe. Once the dataframe is prepared we are sorting
                it descending based on the operation timestamop and finally selecting the top 10.  
    """
    keys = r.keys()
    final_val = []
    df = pd.DataFrame([],columns=['1stnum','Op','2ndnum','res','ts'])
    i=0
    for key in keys:
        val = r.get(key)
        print(val)
        df.loc[i] = val.split(',')
        i = i +1
        final_val.append(val)
    final_val_str = ""
    df =  df.sort_values('ts',ascending = False).head(10)
    if len(df.index)<10:
        k=len(df.index)
    else:
        k=10
    if df.empty:
        return ""
    else:
        for i in range(k):
            if df.iloc[i]['Op']=="Addition":
                sym = "+"
            elif df.iloc[i]['Op']=="Substraction":
                sym = "-"
            elif df.iloc[i]['Op']=="Multiplication":
                sym = "x"
            else:
                sym = "/"
            final_val_str =  final_val_str + "<h1></h1>" + df.iloc[i]['1stnum'] + sym + df.iloc[i]['2ndnum'] + "=" + df.iloc[i]['res']
        print(final_val_str)
        return final_val_str


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port,  debug=True)
