import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer, wordnet

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
schedule = json.loads(open('schedule.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("\nThe Bot is online! Say 'exit' to quit. Why not start off with a greeting?\n")

global find_tutor

find_tutor = False

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Bye! Thanks for talking to me!")
        break
    
    intents_list = predict_class(user_input.lower())
    
    #print(intents_list) #Debugging use, prints out the intent as well as probability of the intent

    # handles edge case where the result is empty (Has no tag). Rare but can happen.
    if intents_list == []:
        intents_list = predict_class("")
    

    if intents_list[0]['intent'] == 'tutoring':
        find_tutor = True
        result = get_response(intents_list, intents)
        print("Bot: " + result)
        continue
    
    # intitally set class name to be blank. 
    class_name = ''

    if find_tutor:
        class_name = intents_list[0]['intent']
        try:
            print("Bot:", schedule["class"][0][class_name])
            print("If you need to find a tutor for another class, just mention 'tutoring' or 'help' again, or if you need any general tips, just type the class name.")
            find_tutor = False

        except:
            if class_name in ['noresponse', 'thanks', 'greetings', 'tutoring']:
                result = get_response(intents_list, intents)
                print("Bot: " + result)
            else:
                print("Bot: Sorry, that class does not have tutors.")

    else:
        result = get_response(intents_list, intents)
        print("Bot: " + result)
    
    #result = get_response(intents_list, intents)
    #print("Bot:", result)
