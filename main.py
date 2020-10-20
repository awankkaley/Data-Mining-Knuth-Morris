# import StemmerFactory class
import json
from flask import Flask, request
import nltk
# nltk.download()
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import source as model
from time import process_time

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

app = Flask(__name__)


# kmp class process
class KMP:
    def partial(self, pattern):
        """ Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, T, P):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
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


@app.route('/api/kmp', methods=['POST'])
def get_data():
    # specialcaracter cleaning
    req = request.get_json()
    query = req['query']
    filter = req['filter']
    sentence = nltk.re.sub('[^A-Za-z/ ]', '', query)
    # stem
    output = stemmer.stem(sentence)
    # stopword
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(output)
    # tokenize
    tokens = nltk.tokenize.word_tokenize(stop)
    # kmp
    kmp = KMP()
    data = []

    profile = model.alldata()
    if filter == 2:
        profile = model.alldataNama()
    if filter == 3:
        profile = model.alldataZat()

    for index, it in profile:
        t0 = nltk.re.sub('[^A-Za-z/ ]', '', stemmer.stem(it)).replace("daun", "").replace("obat", "").replace(
            "sakit",
            "")
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
    if hasilnya:
        return {'code': 200, 'msg': 'success', 'total': len(hasilnya), 'key': json.dumps(tokens),
                'data': hasilnya}, 200
    else:
        return {'code': 400, 'msg': 'Data Tidak Ditemukan'}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5004)
