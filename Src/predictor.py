import pickle

#load model
model = pickle.load(open('model.pkl', 'rb'))

input_mail = ["I've been searching for the right words to thank you for this breather. I promise i wont take your help"
              " for granted and will fulfil my promise. You have been wonderful and a blessing at all times"]
input_mail_1 = ["Congratulations ur awarded either £500 of CD gift vouchers & Free entry 2 our £100 weekly draw txt MUSIC to 87066 TnCs www.Ldew.com1win150ppmx3age16"]

# convert text to feature vectors and load vectorizer
feature_extraction = pickle.load(open('vectorizer.pickle', 'rb'))
input_data_features = feature_extraction.transform(input_mail_1)

# making prediction
prediction = model.predict(input_data_features)
print(prediction)

if prediction[0] == 1:
    print('Ham mail')
else:
    print('Spam mail')
