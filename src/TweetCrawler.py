'''
Created on Feb 10, 2011

@author: Paul
'''

import twitter
import time

class TweetCrawler(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.locationList= (("Boulder", (40.02, -105.25, "7mi")),
                            ("Denver", (39.45, -105.0, "7mi")),
                            ("Vail", (39.64, -106.39, "25mi")),
                            ("Colorado Springs", (38.834, -104.821, "7mi" )),
                            ("Fort Collins", (40.585, -105.084, "7mi")),
                            ("Pueblo", (38.254, -104.609, "7mi")),
                            ("Grand Junction", (39.3, -108.33, "7mi"))
                            )
        self.api = twitter.Api(consumer_key='5LhqyA0C9oCH6OcF9sVJPA', consumer_secret='EcfBtvAnAjtmws5hM0EDpphJVres6FReJwJYEsKuU', access_token_key='250215778-dU99B2GmRdlkXBB1MLqnDP26HUmPMhKD7juZXHmZ', access_token_secret='DyST01S2rurrFtzQzKIK7lJC2JTqPP3Y2kBgVcgd0') 
        print self.api.VerifyCredentials()
        self.locations = {}        
        self.recentTweets = {}       
        self.lastFifteen = {}
        self.lastHalf = {}
        self.lastHour = {}
        self.timeStores = self.lastFifteen, self.lastHalf, self.lastHour
        self.timeResolutions = 900, 1800, 3600
        self.happySearch = "love OR happy OR yay OR sweet OR awesome OR good"
        self.unhappySearch = "hate OR angry OR sad OR boo OR crapy"
        self.initLocations()
        self.initRecentTweets()
        
        
        
    def initLocations(self):
        for loc in self.locationList:
            self.locations[loc[0]] = loc[1]
            
        
            for item in self.timeStores:                
                item[loc[0]] = []        
        
    def initRecentTweets(self):
        for name,loc in self.locations.iteritems():
            results = self.api.GetSearch("love OR happy OR yay OR sweet OR awesome OR good", geocode =(loc))
            mostRecent = 0
            for result in results:
                if result.GetId() > mostRecent:
                    mostRecent = result.GetId()
            self.recentTweets[name] = mostRecent
    
    def locationString(self, location):
        res = ""
        for element in location:
            res += str(element)+","
        res = res[:-1]
        return res
    
    '''
    Tallys when/where tweets came from
    '''
    def keepStats(self, location, results):        
        for store, limit in map(None, self.timeStores, self.timeResolutions):
            curTime = time.time()
            if len(store[location]) is not 0:
                while store[location][0].GetCreatedAtInSeconds() - curTime > limit:
                    del store[location][0]
            for res in results:
                store[location].append(res)
            
             
    def run(self, timeoutInSeconds):
        while(True):            
            for name,loc in self.locations.iteritems():
                sinceID = self.recentTweets[name]
                print name + ": most recent id - " + str(sinceID)          
                
                try:
                    results = self.api.GetSearch("love OR happy OR yay OR sweet OR awesome OR good", geocode = (loc), since_id = self.recentTweets[name])
                    
                    if len(results) is 0:
                        print "No new results"
                    else:
                        ########Connec to arduino##########
                        #got a happy tweet
                        print "Happy"
                        #########/arduino##############
                        self.keepStats(name, results)
                    print "\t" + str(len(self.lastHour[name]))
                    
                    #keeping track of the ID of the most recent tweet
                    mostRecent = self.recentTweets[name]    
                    for result in results:
                        if result.GetLocation() is not None:
                            print name + ": " + result.GetText()                        
                            print "\t" + result.GetLocation()
                            print "\t" + result.GetCreatedAt()
                            print "\t" + str(result.GetId())
                            print "\t" + str(result.GetUser().GetId())
                            if result.GetId() > mostRecent:
                                mostRecent = result.GetId()                           
                                self.recentTweets[name] = result.GetId()
                except:
                    pass
            status = self.api.GetRateLimitStatus()
            print status
            print "Sleeping for " + str(timeoutInSeconds) + " seconds."
            time.sleep(timeoutInSeconds)


if __name__ == '__main__':
    crawler = TweetCrawler()
    crawler.run(30)