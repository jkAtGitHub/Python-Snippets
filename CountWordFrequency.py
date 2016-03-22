import operator
import re
from operator import itemgetter

'''
Returns a list of tuples containing the top n frequent words in the given string s.
In case of tie, words are arranged aplhabetically
'''
def countFreq(s, n=None):
    words = re.sub('[^A-Za-z0-9]+', ' ', s.lower()).split(' ')
    uniqueWords = list(set(words))
    L = []
    for word in uniqueWords:
        #Add to a list, the unique word and the frequency of the words in the words list as a tuple 
        L.append((word, words.count(word)))
    
    #Sort based on alphabetical order of the word
    L.sort(key=operator.itemgetter(0))
    # Sort based on the count frequency
    L.sort(key=operator.itemgetter(1), reverse = True)
    #Return Top n words and their count as List of tuple
    return L[:n]

def main():
    s = 'Betty bought a bit of Butter! but the butter was bitter, so she got a better butter, which was better than the bitter butter'
    print countFreq(s, 3)
    print countFreq(s)
    
if __name__ == '__main__':
    main()
