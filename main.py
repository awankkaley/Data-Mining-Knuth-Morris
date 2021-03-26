# import StemmerFactory class
import json
from flask import Flask, request
import nltk
# nltk.download('punkt')
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import source as model
from time import process_time

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

app = Flask(__name__)


# CLASS PERHITUNGAN KMP
class KMP:
    def partial(self, pattern):
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, T, P):
        partial, ret, j = self.partial(P), [], 0

        for i in range(len(T)):
            while j > 0 and T[i] != P[j]:
                j = partial[j - 1]
            if T[i] == P[j]: j += 1
            if j == len(P):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret


# sort match value
def sortSecond(val):
    return val[0]


# GET ALL DATA
@app.route('/hello', methods=['GET'])
def hello():
    return {'code': 200, 'msg': 'success'}, 200


# GET ALL DATA
@app.route('/api/all', methods=['POST'])
def get_all():
    hasilnya = model.all()
    if hasilnya:
        return {'code': 200, 'msg': 'success', 'total': len(hasilnya),
                'data': hasilnya}, 200
    else:
        return {'code': 400, 'msg': 'Data Tidak Ditemukan'}, 200


# KMP SEARCH
@app.route('/api/kmp', methods=['POST'])
def get_data():
    # MENGHILANGKAN SPESIAL KARAKTER
    t1_start = process_time()
    req = request.get_json()
    query = req['query']
    filter = req['filter']
    sentence = nltk.re.sub('[^A-Za-z/ ]', '', query)
    # CASE FOLDING
    output = stemmer.stem(sentence)
    # STOPWORD
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(output)
    # TOKENIZE
    tokens = nltk.tokenize.word_tokenize(stop)
    data = model.persamaan(tokens)
    # COSINE
    for index in data:
        splits = index[0].split(",")
        for split in splits:
            tokens.append(split)

    print(tokens)
    # GET KMP CLASS
    kmp = KMP()
    data = []
    profile = model.alldata()
    if filter == "2":
        profile = model.alldataNama()
    if filter == "3":
        profile = model.alldataZat()
    # FILTERING
    for index, it in profile:
        t0 = nltk.re.sub('[^A-Za-z/ ]', '',
                         stemmer.stem(it)
                         .replace("obat", "")
                         .replace("sakit", "")
                         .replace("buah", "")
                         .replace("kulit", "")
                         .replace("batang", "")
                         .replace("kayu", "")
                         .replace("kelopak", "")
                         .replace("bunga", "")
                         .replace("daun", "")
                         .replace("tangkai", "")
                         .replace("akar", ""))
        t1 = stopword.remove(t0)
        counts = 0
        for i in tokens:
            if kmp.search(t1, i):
                counts += 1
        if counts != 0:
            data.append((counts, index))
    data.sort(key=sortSecond, reverse=True)
    print(data)
    array_data = []
    for key in data:
        array_data.append(key[1])
    # Get Match Data from DB
    hasilnya = model.byid(array_data)
    t1_stop = process_time()
    if hasilnya:
        return {'code': 200, 'msg': 'success', 'total': len(hasilnya), 'key': t1_stop - t1_start,
                'data': hasilnya}, 200
    else:
        return {'code': 400, 'msg': 'Data Tidak Ditemukan'}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=3000)
