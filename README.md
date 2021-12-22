# CS370 Project 2

Amandeep Singh

as3627

## Startup Guide

1) Save these files in the same directory.
    - `intents.json`
    - `schedule.json`
    - `training.py`
    - `chatbot.py`
    - `requirements.txt`

2) Startup and run a virtual environment, then install the required packages.
    - `python -m virtualenv env`
    - `.\env\Scripts\activate`
    - `pip install -r requirements.txt`

3) Run `python training.py` to train the chatbot.
4) Run `python chatbot.py` to start the chatbot.

To disable the virtual environment, type `deactivate` in the command line.

## Description

I mostly just followed a few tutorials on how to make a chatbot. 
This specific one uses NLTK (Natural Language Toolkit), Tensorflow, Keras, numpy, and a few other basic python libraries. 

The chatbot can respond to classes in the CS cirriculum and find tutors for some of those classes. 

Talk with the chatbot by entering the class name, for example 'CS100'. 
If you want to look for a tutor, just mention the words 'tutor' or 'help' in the chat. 
