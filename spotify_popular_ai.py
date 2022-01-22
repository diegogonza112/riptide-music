import pickle
import warnings

import numpy
import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier, BaggingClassifier, \
    RandomForestClassifier

from spotify_search import SpotifySearch
import csv
from sklearn.model_selection import train_test_split

warnings.simplefilter(action='ignore', category=FutureWarning)


def analyse_audio(uri):
    ss = SpotifySearch()
    return load_model(ss.track_info_search(uri))


def make_model():
    raw_pop = open('popular.csv', 'rt')
    reader = list(csv.reader(raw_pop, delimiter=',', ))
    data_pop = numpy.array(reader)

    raw_avg = open('average.csv', 'rt')
    read = list(csv.reader(raw_avg, delimiter=','))
    data_avg = numpy.array(read)

    all_info = numpy.concatenate((data_avg, data_pop))

    true = np.ones(320)
    false = np.zeros(320)

    all_values = numpy.concatenate((false, true))

    gnb = GaussianNB()
    rfc = RandomForestClassifier()
    bc = BaggingClassifier()

    predictor = VotingClassifier([('gnb', gnb), ('rfc', rfc), ('bc', bc)])

    train_in, test_in, train_out, test_out = train_test_split(all_info,
                                                              all_values)
    train_i, test_i, train_o, test_o = train_test_split(all_info,
                                                        all_values)
    predictor.fit(train_in, train_out)

    print(predictor.score(test_i, test_o))

    pickle.dump(predictor, open('finalized.sav', 'wb'))


def load_model(value):
    raw_pop = open('popular.csv', 'rt')
    reader = list(csv.reader(raw_pop, delimiter=',', ))
    data_pop = numpy.array(reader)

    raw_avg = open('average.csv', 'rt')
    read = list(csv.reader(raw_avg, delimiter=','))
    data_avg = numpy.array(read)

    all_info = numpy.concatenate((data_avg, data_pop))

    true = np.ones(320)
    false = np.zeros(320)

    all_values = numpy.concatenate((false, true))

    train_in, test_in, train_out, test_out = train_test_split(all_info,
                                                              all_values)

    model = pickle.load(open('finalized.sav', 'rb'))
    percentage = model.score(test_in, test_out)

    value = np.array(value).reshape(1, -1)
    verdict = model.predict(value).flat[0]

    if verdict:
        popularity = "Popular"
    else:
        popularity = "Unpopular"

    return round(percentage * 100, 2), popularity
