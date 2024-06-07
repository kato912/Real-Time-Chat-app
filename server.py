from flask import Flask , request ,jsonify
app = Flask(__name__)

msg = []

@app.route('/send' ,methods =["POST"])
def send_msg():
    #get messages
    newmsg = request.get_json()
    msg.append(newmsg)
    return jsonify({'status': 'Message received'})

@app.route('/refmsg',methods = ["GET"])
def ref_msg():
    # return array messages
    return jsonify(msg)

if __name__ == "__main__":
    app.run(debug=True)