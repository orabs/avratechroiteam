from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('worshipers.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result2 = request.form
      result2=list(result2)
      return "{}".format(result2)
      # return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)