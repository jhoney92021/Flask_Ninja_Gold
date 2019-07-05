from flask import Flask, render_template, request, redirect, session
import random, datetime
app = Flask(__name__)
app.secret_key = 'invisible poops'



def earnGold(minnum,maxnum):
    goldRand = random.randint(minnum, maxnum)
    session['gold'] += goldRand
    session['transaction'] += 1
    if goldRand < 0:
        session["activities"].append("Lost " + str(goldRand) + " gold from the " + str(session['workplace']))
        session['text_color'].append('red')
    else: 
        session["activities"].append("Earned " + str(goldRand) + " gold from the " + str(session['workplace']))
        session['text_color'].append('green')
    endGame()

def endGame():
    if session['gold'] >= 450:
        session["activities"].append('You Win!!!')
        session['text_color'].append('purple')
        return redirect('/') 
    if session['transaction'] >= 14:
        session["activities"].append('You lose...')
        session['text_color'].append('yellow') 
        session['reset'] = 'submit'  
        return redirect('/')    
    else: pass


placeDict={
'Farm' : {'min':10,'max':12},
'Cave' : {'min':5, 'max':10},
'House' : {'min':2, 'max':5},
'Casino' : {'min':-50, 'max':50}
}

@app.route('/')
def default():
    if "gold" not in session:
        session["gold"] = 0
    if "activities" not in session:
        session["activities"] = [] 
    if "transaction" not in session:
        session['transaction'] = 0
    if "workplace" not in session:
        session['workplace'] = 0
    if "text_color" not in session:
        session['text_color'] = []
    if "reset" not in session:
        session['reset'] = 'hidden'    

    
    return render_template('index.html',
        gold= session['gold'],
        workplace= session['workplace'],
        transactions= session['transaction'],
        activities= session['activities'],
        datetime= datetime.datetime.now(),
        text_color = session['text_color'],
        reset = session['reset']
            )

@app.route('/process', methods=['POST'])
def process():
    session['workplace'] = request.form['workplace']
    if session['workplace'] == 'Reset':
        session["gold"] = 0
        session['transaction'] = 0
        session["activities"] = []
        session['text_color'] = []
        session['reset'] = 'hidden' 
        return redirect('/')
    x= session['workplace']
    earnGold(placeDict[x]['min'], placeDict[x]['max'])
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)