import csv
import numpy as np
from keras.utils import np_utils
import FeatureExtractor as feat_ext
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

seed = 7
np.random.seed(seed)

data = []
targets = []

with open('./Resources/features.csv', 'rb') as csvfile:
    feareader = csv.reader(csvfile, delimiter=',')
    for row in feareader:
        data.append(row)

print data[0]

with open('./Resources/targets2.csv', 'rb') as csvfile:
    tareader = csv.reader(csvfile, delimiter=',')
    for row in tareader:
        if(row!=[]):
            targets.append(float(row[0]))


print np.shape(data)

data = np.asmatrix(data)
targets = np.asarray(targets).astype(np.float)

data = data[:,1:len(data)-1].astype(np.float)


print data[0]
print targets[0]

print len(targets)
print len(data)

#show pca first two components wrt targets
'''import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(data)
toplotdata = pca.transform(data)


plt.plot(toplotdata[:,0], toplotdata[:,1], 'ob')
plt.plot(toplotdata[targets==4,0], toplotdata[targets==4,1], 'or')
plt.plot(toplotdata[targets==0,0], toplotdata[targets==0,1], 'oy')
plt.plot(toplotdata[targets==3,0], toplotdata[targets==3,1], 'om')
plt.plot(toplotdata[targets==2,0], toplotdata[targets==2,1], 'oc')
plt.plot(toplotdata[targets==6,0], toplotdata[targets==6,1], 'og')


plt.show()
'''

from sklearn.model_selection import train_test_split



X_train = data  #, X_test, y_train, y_test = train_test_split(data,targets, test_size = 0.2, random_state = 0)

dummy_y_train = np_utils.to_categorical(targets)

model = feat_ext.baseline_model()
model.load_weights('./EmoDashAnnotation/Resources/EmoDashANN_weights_v1.h5')

'''classifier = KerasClassifier(build_fn=model, verbose=0, batch_size=10, epochs=90)
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(classifier, X_train, dummy_y_train, cv=kfold, n_jobs=-1)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
'''

model.fit(X_train, dummy_y_train, nb_epoch=90, batch_size=10, verbose=1)

model.save_weights('./EmoDashAnnotation/Resources/EmoDashANN_weights_v2.h5', overwrite=True)
