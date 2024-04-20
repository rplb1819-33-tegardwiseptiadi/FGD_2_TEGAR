import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson import ObjectId

# tegar dwi septiadi

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def home():
    # menampilkan seluruh data yg ada di db fruit
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit=fruit)

@app.route('/fruit',methods=['GET', 'POST'])
def fruit():
    # menampilkan seluruh data yg ada di db fruit
    fruit = list(db.fruit.find({}))
    return render_template('fruit.html', fruit=fruit)

# Create Data
# method get : untuk me-render template
# method post : untuk menerima data dari client
@app.route('/addFruit',methods=['GET', 'POST'])
def addFruit():
    if request.method == "POST":
        # Mengambil data dari client
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        
        nama_gambar = request.files['gambar']
        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
        # jika user tidak me insert gambar maka
        else:
            nama_gambar = None
        
        #masukkan data ke database 
        doc = {
            'nama':nama,
            'harga':harga,
            'gambar':nama_file_gambar,
            'deskripsi':deskripsi
        }
        # masukkan ke database yg bernama fruit
        db.fruit.insert_one(doc)  
        return redirect(url_for('fruit'))
    return render_template('AddFruit.html')

# Edit Data
@app.route('/editFruit/<_id>',methods=['GET', 'POST'])
# ada _id karna untuk edit berdasarkan data yg dipilih
def editFruit(_id):
    
    # Mengambil data dari client
    if request.method == "POST":
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        #update data baru ke database 
        doc = {
            'nama':nama,
            'harga':harga, 
            'deskripsi':deskripsi
        }
        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            print(nama_file_asli)
            nama_file_gambar = nama_file_asli. split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar'] = nama_file_gambar
        # update data
        db.fruit.update_one({"_id":ObjectId(id)},{'$set':doc})
        return redirect(url_for('fruit'))
    
    id = ObjectId(_id)
     # menampilkan seluruh data yg ada di db fruit
    data = list(db.fruit.find({'_id':id}))
    return render_template('EditFruit.html', data=data)
    # data = data | namaVariabel data = ambilvariabel datayangdiatasnya

# Delete Data
@app.route('/deleteFruit/<_id>',methods=['GET', 'POST'])
def deleteFruit(_id):
    # menampilkan seluruh data yg ada di db fruit
    db.fruit.delete_one({"_id":ObjectId(_id)})
    return redirect(url_for('fruit'))
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
