from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html")
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')
@app.route('/chatbotrecommendation')
def chatbotrecommendation():
    return render_template("chatbot.html")
if __name__=='main':
    app.run(debug=True)
