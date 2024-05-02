import flask
import pickle
from datetime import datetime,timedelta

app = flask.Flask(__name__)


#Index Page
@app.route('/')
def index():
    file = open('menu.dat','rb')
    data = pickle.load(file)
    file.close()
    file1 = open('cart.dat','rb')
    data1 = pickle.load(file1)
    file1.close()
    dat=[data,data1]
    prize=0
    for i in data:
        try:
            prize=prize+int(dat[0][i])*dat[1][i]
        except:
            pass
    return flask.render_template('index.html',data=[data,data1,prize])

#Edit Menu
@app.route('/edit')
def Edit():
    file = open('menu.dat','rb')
    data=pickle.load(file)
    file.close()
    return flask.render_template('edit.html',data=data)

@app.route('/update/<item>', methods=['GET', 'POST'])
def update_item(item):
    if flask.request.method == 'POST':
        price = flask.request.form['item-price']
        file = open('menu.dat','rb')
        data = pickle.load(file)
        file.close()
        for i in data:
            print(i)
        file = open('menu.dat','wb')
        data[item]=price
        pickle.dump(data,file)
        file.close()
        return flask.redirect('/edit')
    file = open('menu.dat','rb')
    data=pickle.load(file)
    file.close()
    return flask.render_template('update.html',data=[data,item])

#delete item
@app.route('/delete/<item>', methods=['GET', 'POST'])
def delete_item(item):
    file = open('menu.dat','rb')
    data = pickle.load(file)
    file.close()
    file = open('menu.dat','wb')
    try:
        del data[item]
    except:
        pass
    pickle.dump(data,file)
    file.close()
    return flask.redirect('/edit')

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if flask.request.method == 'POST':
        item = flask.request.form['item-name']
        price = flask.request.form['item-price']
        file = open('menu.dat','rb')
        data = pickle.load(file)
        file.close()
        file = open('menu.dat','wb')
        data[item]=price
        pickle.dump(data,file)
        file.close()
        return flask.redirect('/edit')

#Cart
@app.route('/add/<name>')
def add(name):
    file1 = open('menu.dat','rb')
    data1 = pickle.load(file1)
    file1.close()
    file = open("cart.dat",'rb')
    data = pickle.load(file)
    file.close()
    file = open("cart.dat",'wb')
    if name in data:
        data[name]=data[name]+1
    else:
        data[name]=1
    pickle.dump(data,file)
    file.close()
    return flask.redirect('/')

@app.route('/sub/<name>')
def sub(name):
    file1 = open('menu.dat','rb')
    data1 = pickle.load(file1)
    file1.close()
    file = open("cart.dat",'rb')
    data = pickle.load(file)
    file.close()
    file = open("cart.dat",'wb')
    if name in data:
        if data[name]==0:
            data[name]=0
        else:
            data[name]=data[name]-1
    else:
        data[name]=0
    pickle.dump(data,file)
    file.close()
    return flask.redirect('/')

#payment
@app.route('/payment/<prize>')
def payment(prize):
    file = open('menu.dat','rb')
    data = pickle.load(file)
    file.close()
    file1 = open('cart.dat','rb')
    data1 = pickle.load(file1)
    file1.close()
    data2={}
    for i in data1:
        if data1[i] != 0:
            data2[i]=data1[i]
    l =[]
    for i in data2:
        if i in data:
            l.append([i,data2[i],data[i],int(data[i])*data2[i]])
    return flask.render_template('payment.html',data=[l,prize])

#Payment Complete
@app.route('/complete/<id>/<d>')
def complete(id,d):
    f = open('orders.dat','rb')
    data = pickle.load(f)
    f.close()
    file1 = open('cart.dat','rb')
    data1 = pickle.load(file1)
    file1.close()
    data2={}
    for i in data1:
        if data1[i] != 0:
            data2[i]=data1[i]
    data.append([data[-1][0]+1,data2,date.today(),id,d])
    f = open('orders.dat','wb')
    pickle.dump(data,f)
    f.close()
    f=open('cart.dat','wb')
    pickle.dump({},f)
    f.close()
    return flask.redirect('/')

#Orders
@app.route('/orders')
def Orders():
    f = open('orders.dat','rb')
    data = pickle.load(f)
    f.close()
    return flask.render_template('orders.html',data=data[1:])

#Reports
@app.route('/reports')
def Reports():
    return flask.render_template('reports.html')

#View 
@app.route('/view/<id>')
def View(id):
    f = open('orders.dat','rb')
    data = pickle.load(f)
    for i in data:
        if id==str(i[0]):
            data1 = i
    f.close()
    file = open('menu.dat','rb')
    menu = pickle.load(file)
    l ={}
    total = 0
    for i in data1:
        for j in data1[1]:
            if j in menu:
                l[j]=[data1[1][j],int(menu[j])]
    file.close()
    for i in l:
        total+=l[i][0]*int(l[i][1])
    return flask.render_template('order-display.html',data=[data[1:],l,total])

#Display
@app.route('/display/<id>')
def Display(id):
    l={}
    d={}
    online={}
    f = open('orders.dat','rb')
    data = pickle.load(f)
    if (id=='day'):
        for i in data:
            if i[2]==date.today():
                for j in i[1]:
                    if j in d:
                        d[j]+=i[1][j]
                    else:
                        d[j]=i[1][j]    
    if(id=='week'):
        for i in data:
            for k in range(7):
                if i[2]== date.today() - timedelta(days=k):
                    for j in i[1]:
                        if j in d:
                            d[j]+=i[1][j]
                        else:
                            d[j]=i[1][j]    
    if(id=='month'):
        for i in data:
            for k in range(30):
                if i[2]== date.today() - timedelta(days=k):
                    for j in i[1]:
                        if j in d:
                            d[j]+=i[1][j]
                        else:
                            d[j]=i[1][j]
    for i in data:
        if i[2]==date.today():
            if i[3] == 'online':
                for j in i[1]:
                    if j in online:
                        online[j]+=i[1][j]
                    else:
                        online[j]=i[1][j]
    file = open('menu.dat','rb')
    menu = pickle.load(file)
    for i in data:
        if i[2]==date.today():
            for j in i[1]:
                try:
                    l[j]=[menu[j],d[j],online[j],d[j]-online[j],int(menu[j])*d[j]]
                except:
                    l[j]=[menu[j],d[j],0,d[j],int(menu[j])*d[j]]
    return flask.render_template('display.html',data=l)

if __name__=="__main__":
    app.run(host='0.0.0.0', port='9000', debug='True')