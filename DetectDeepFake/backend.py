from distutils.log import debug
from fileinput import filename
from flask import *  
from predict import detect_deepfake
from flask_cors import CORS
app = Flask(__name__)  
app.secret_key = '123'
CORS(app)
@app.route('/')  
def main():  
    return render_template('index.html')  
@app.route('/upload', methods = ['POST'])  
def success():  
    session['result']=0
    if request.method == 'POST':  
        f = request.files['file']
        f.save("video/"+f.filename)  
        path_video="video/"+f.filename
        if detect_deepfake(path_video)==1:
            data={'message': 'Upload successful', 'filename': f.filename,'result':'REAL'} 
            session['result']=data          
            return jsonify({'message': 'Upload successful', 'filename': f.filename,'result':'REAL'})
        else:
            data={'message': 'Upload successful', 'filename': f.filename,'result':'FAKE'}
            session['result']=data
            return jsonify(data)
@app.route('/result')
def result():
    data=session.get('result','No data found')
    print(data)
    return render_template("result.html")
@app.route('/api/result',methods=['GET'])
def api_result():
    if request.method == 'GET':
        data=session.get('result','No data found')
        print(data)
        return jsonify(data)
if __name__ == '__main__':  
    app.run(debug=True,port=8080)