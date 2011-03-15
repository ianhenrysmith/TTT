'''
Created on Feb 10, 2011

@author: Paul
'''

import twitter
import time
from FakeTwitter import FakeTwitter
from serial_comm import Arduino

class TweetCrawler(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.testing = True
        self.FT = FakeTwitter()
        self.ard = Arduino()
        self.locationList= (("Boulder", (40.02, -105.25, "7mi")),
                            ("Denver", (39.45, -105.0, "7mi")),
                            ("Vail", (39.64, -106.39, "25mi")),
                            ("Colorado Springs", (38.834, -104.821, "7mi" )),
                            ("Fort Collins", (40.585, -105.084, "7mi")),
                            ("Pueblo", (38.254, -104.609, "7mi")),
                            ("Grand Junction", (39.3, -108.33, "7mi")),
                            ("Longmont", (40.17, -105.10, "7mi")),
                            ("Durango", (37.27, -107.86, "10mi")),
                            ("Fort Morgan", (40.25, -103.85, "10mi"))
                            )
        self.api = twitter.Api(consumer_key='5LhqyA0C9oCH6OcF9sVJPA', consumer_secret='EcfBtvAnAjtmws5hM0EDpphJVres6FReJwJYEsKuU', access_token_key='250215778-dU99B2GmRdlkXBB1MLqnDP26HUmPMhKD7juZXHmZ', access_token_secret='DyST01S2rurrFtzQzKIK7lJC2JTqPP3Y2kBgVcgd0') 
        print self.api.VerifyCredentials()
        print self.api.GetRateLimitStatus()
        self.locations = {}        
        self.mostRecentHappyTweet = {}       
        self.recentHappyTweets = {}
        self.mostRecentUnhappyTweet = {}       
        self.recentUnhappyTweets = {}
        self.timeResolution = 3600
        self.happySearch = "love OR happy OR yay OR sweet OR awesome OR good"
        self.unhappySearch = "hate OR angry OR sad OR boo OR crapy OR crappy OR depressed"
        self.beiberSearch = "bieber"
        self.initLocations()
        self.initRecentTweets()
        
        
        
    def initLocations(self):
        for loc in self.locationList:
            self.locations[loc[0]] = loc[1]      
            self.recentHappyTweets[loc[0]] = []
            self.recentUnhappyTweets[loc[0]] = []
           
        
    def initRecentTweets(self):
        for name,loc in self.locations.iteritems():
            results = self.api.GetSearch("love OR happy OR yay OR sweet OR awesome OR good", geocode =(loc))
            results += self.api.GetSearch(self.unhappySearch, geocode = loc)
            mostRecent = 0
            for result in results:
                if result.GetId() > mostRecent:
                    mostRecent = result.GetId()
            self.mostRecentHappyTweet[name] = mostRecent
            self.mostRecentUnhappyTweet[name] = mostRecent 
            time.sleep(1)   
    
    def locationString(self, location):
        res = ""
        for element in location:
            res += str(element)+","
        res = res[:-1]
        return res
    
    '''
    Tallys when/where tweets came from
    '''
    def keepStats(self, location, happyResults, unhappyResults):        
        curTime = time.time()
        if len(self.recentHappyTweets[location]) is not 0:
            while self.recentHappyTweets[location][0].GetCreatedAtInSeconds() - curTime > self.timeResolution:
                del self.recentHappyTweets[location][0]
        if len(self.recentUnhappyTweets[location]) is not 0:
            while self.recentUnhappyTweets[location][0].GetCreatedAtInSeconds() - curTime > self.timeResolution:
                del self.recentUnhappyTweets[location][0]
        for res in happyResults:
            self.recentHappyTweets[location].append(res)
        for res in unhappyResults:
            self.recentUnhappyTweets[location].append(res)
             
    def run(self, timeoutInSeconds):
        while(True):            
            for name,loc in self.locations.iteritems():
                time.sleep(2)
                happySinceID = self.mostRecentHappyTweet[name]
                unhappySinceID = self.mostRecentUnhappyTweet[name]
                print name + ": most recent ids - " 
#                print "\t" + str(happySinceID)
#                print "\t" + str(unhappySinceID)          
                if not self.testing:
#                    try:
                    happyResults = self.api.GetSearch(self.happySearch, geocode = (loc), since_id = self.mostRecentHappyTweet[name])
                    unhappyResults = self.api.GetSearch(self.unhappySearch, geocode = loc, since_id = self.mostRecentUnhappyTweet[name])
                    #bieberResults =  self.api.GetSearch(self.beiberSearch, geocode = (loc), since_id = self.mostRecentHappyTweet[name]) 
#                    except:
#                        print "API ERROR!!!"
                else:
                    happyResults = self.FT.getHappy()
                    unhappyResults = self.FT.getUnhappy()
                if len(happyResults) is 0:
                    print "\tNo new results"
                else:
                    ########Connect to arduino##########
                    #got a happy tweet
                    print "Happy"
                    #########/arduino##############
                    self.keepStats(name, happyResults, unhappyResults)
                self.outputToArduino(name, len(happyResults), len(unhappyResults))
                print "\t# Happy: " + str(len(self.recentHappyTweets[name]))
                print "\t# Unhappy: " + str(len(self.recentUnhappyTweets[name]))
                #print "\t# Bieber: " + str(len(bieberResults))
                #keeping track of the ID of the most recent tweet
                mostRecent = self.mostRecentHappyTweet[name]    
                for result in happyResults:   
                    """print name + ": " + result.GetText()                        
                    print "\t" + result.GetLocation()
                    print "\t" + result.GetCreatedAt()
                    print "\t" + str(result.GetId())
                    print "\t" + str(result.GetUser().GetId())"""
                    if result.GetId() > mostRecent:
                        mostRecent = result.GetId()                           
                        self.mostRecentHappyTweet[name] = result.GetId()
                mostRecent = self.mostRecentUnhappyTweet[name]
                for result in unhappyResults:   
                    """print name + ": " + result.GetText()                        
                    print "\t" + result.GetLocation()
                    print "\t" + result.GetCreatedAt()
                    print "\t" + str(result.GetId())
                    print "\t" + str(result.GetUser().GetId())"""
                    if result.GetId() > mostRecent:
                        mostRecent = result.GetId()                           
                        self.mostRecentUnhappyTweet[name] = result.GetId()

            
            print self.api.GetRateLimitStatus()
            print "Sleeping for " + str(timeoutInSeconds) + " seconds."
            time.sleep(timeoutInSeconds)

    def outputToArduino(self, name, happy, unhappy):
        return
        if happy is 0 and unhappy is 0:
            self.ard.write(name.upper(), "GREEN")
        elif unhappy > 0:
            self.ard.write(name.upper(), "RED")
        else:
            self.ard.write(name.upper(), "YELLOW")
            
if __name__ == '__main__':
    crawler = TweetCrawler()
    crawler.run(60)