from flask import Flask,request 
import jwt,datetime,os


from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# Config 

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login",methods=["POST","GET"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials",401

    
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email,password FROM user WHERE email=%s",(auth.username,)
    )
    if res > 0:
        user_row = cur.fetchone()
        emaiL = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials",401
        else:
            return createJWT(auth.username,os.environ.get("JWT_SECRET"),True)
        
        
    else:
        return "Invalid Credentials",401


if __name__== "__main__":
    server.run()