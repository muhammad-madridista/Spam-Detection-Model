from flask import Flask,render_template,url_for,request
import os
import _pickle as c
from collections import Counter
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

app = Flask(__name__)

def load(clf_file):
    with open(clf_file, 'rb') as fp:
        try:
            clf=pb.load(fp)
            return clf
        except:
            return None

@app.route("/")
def home():
	return render_template('/home2.html')

@app.route("/predict",methods=['POST'])
def predict():
	def save(clf,name):
		with open(name,'wb') as fp:
			c.dump(clf,fp)
		print("Saved")

	def make_dict():
		direc ="emails/"
		files =os.listdir(direc)

		emails=[direc + email for email in files]

		words=[]
		c=len(emails)
		for email in emails:
			f=open(email,encoding="utf-8",errors="surrogateescape")
			blob=f.read()
			words +=blob.split(" ")

			print(c)
			c-=1

		for i in range(len(words)):
			if not words[i].isalpha():
				words[i]=""

		dictionary= Counter(words)
		del dictionary[""]
		return dictionary.most_common(3000)

	def make_dataset(dictionary):
		direc ="emails/"
		files =os.listdir(direc)


		emails=[direc + email for email in files]

		feature_set=[]
		labels=[]
		c=len(emails)

		for email in emails:
			data=[]
			try:
				f=open(email,encoding="utf-8")
				words=f.read().split(' ')

				for entry in dictionary:
					data.append(words.count(entry[0]))
				feature_set.append(data)
				if "ham" in email:
					labels.append(0)
				if "spam" in email:
					labels.append(1)
			except:
				continue
			print(c)
			c-=1
		return feature_set,labels



	# d=make_dict()
	# with open('d.pb', 'wb') as f:
	# 	c.dump(d, f)
	with open('d.pb', 'rb') as f:
		d = c.load(f)
	# features,labels=make_dataset(d)
	# feat = {'features': features, 'labels':labels}
	# with open('data.pb', 'wb') as f:
	# 	c.dump(feat, f)
	with open('data.pb', 'rb') as f:
		feat = c.load(f)
	features = feat['features']
	labels = feat['labels']
	# print(features)
	# cv=CountVectorizer()
	# cv.fit_transform(features[0])
	# print(features[0])
	# x_train,x_test,y_train,y_test=tts(features,labels,test_size=0.2)
	# clf=SVC(gamma="auto")
	# clf.fit(x_train,y_train)
	#
	# preds=clf.predict(x_test)
	with open("/Users/muhammadnoor1/Desktop/python/enron1/text-classifier.mdl", 'rb') as f:
		clf = c.load(f)

	if request.method == 'POST':
		comment =request.form['comment']
		data = str(comment)
		features = []
		for word in d:
		    features.append(data.count(word[0]))
		# vect = cv.transform(data).toarray()
		preds=clf.predict([features])
	return render_template('result.html',prediction = preds)


if __name__ == '__main__':
	app.run(debug=True,port=5006)
