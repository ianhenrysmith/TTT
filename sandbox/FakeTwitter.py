'''
Created on Feb 24, 2011

@author: Heider
'''

import random
import time

class FakeTwitter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.idCounter = 0
        
        
    def getHappy(self):
        whatToDo = random.randint(0, 1000)
        results = []
        while whatToDo < 400:
            self.idCounter +=1
            results.append(FakeTweet(self.idCounter, "happy"))
            whatToDo = random.randint(0, 1000)
        return results
        
    def getUnhappy(self):
        whatToDo = random.randint(0, 1000)
        results = []
        while whatToDo < 100:
            self.idCounter +=1
            results.append(FakeTweet(self.idCounter, "happy"))
            whatToDo = random.randint(0, 1000)
        return results
        
class FakeTweet(object):
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.created = int(time.time()) 
    
    def GetId(self):
        return self.id
    
    def GetCreatedAtInSeconds(self):
        return self.created