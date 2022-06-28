# importing modules
# import requirements needed
from flask import Flask, request, redirect, url_for, render_template, session
from flask import url_for
#from utils import get_base_url

#from aitextgen import aitextgen
import os
import requests
from bs4 import BeautifulSoup
def permute(the_word):   #Uses recursion to find all ways to order letters of a word
    '''permute(the_word) -> list
    returns list of all permutations of the input word, but if a word has
    multiple of the same letter, there are repeats.'''
    # base case
    inputList = list(the_word)
    if len(inputList) == 1:
        return [inputList[:]]
    # recursive step
    outputList = []  # to store permutations
    for index in range(len(inputList)):
        # construct all permutations that start with the item
        #   at location give by index
        # remove item and permute the rest
        restOfList = inputList[:index]+inputList[index+1:]
        perms = permute(restOfList)
        # add all permutations starting with inputList[index]
        #   and ending with each permuatation just generated
        for wordending in perms:
            outputList.append([inputList[index]]+wordending)
    return outputList

def anagrams(inputStr):
    '''finds all distint permutations after using the permute function'''
    gooddone = []
    newList = permute(inputStr)
    for i in newList:
        n = ''.join(i) 
        gooddone.append(n)
    outPut = []    
    for i in gooddone: # This is if we have a string that has more than one of the same letter.
        if i not in outPut:   # So we only have one of each
            outPut.append(i)
            
    return outPut

def find_anagrams(inputStr):
    inputStr = inputStr.lower()
    outputWords = ''
    ourList = anagrams(inputStr)
    wasoriginalaword = False
    words = requests.get('https://www.mit.edu/~ecprice/wordlist.10000')
    parser = BeautifulSoup(words.content, "html.parser").text
    wordlist = parser.splitlines()
    outputWords = []
    for i in ourList:   # Goes over each letter combination in ourList
        if i in wordlist:  # If the combination is a word in the file
            if i == inputStr:
                wasoriginalaword = True
            outputWords.append(i)  # It adds the word to the ones we output
    if wasoriginalaword is True:
        outputWords[0]= outputWords[0].upper()
    return outputWords
# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
base_url = '/'
app = Flask(__name__)

# set up the routes and logic for the webserver

"""
1. Copy and paste the home function right below the home function.
2. /generate
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate/', methods = ["POST"])
def generate():

    word = request.form['promptForm']
    newstring = ' \n'.join(find_anagrams(word))
    print(newstring)
    return render_template('generate.html', data = newstring)



# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    #website_url = 'vscode.dev' # Put the name of the server url you're on in here
    
    #print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(debug=True)

