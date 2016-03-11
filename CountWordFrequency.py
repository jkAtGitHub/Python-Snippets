import operator
from operator import itemgetter


def countFreq(s, n=None):
    words = s.lower().replace(',','').replace('.', ' ').split(' ')
    uniqueWords = list(set(words))
    L = []
    for word in uniqueWords:
        L.append((word, words.count(word)))
        
    L.sort(key=operator.itemgetter(0))
    L.sort(key=operator.itemgetter(1), reverse = True)
    print L[:n]

def main():
    s = 'betty bought a bit of butter, but the butter was bitter, so she got a better butter, which was better than the bitter butter'
    countFreq(s, 3)
    
if __name__ == '__main__':
    main()