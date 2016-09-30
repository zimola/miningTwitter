#imports
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import MySQLdb


"""mysql -h localhost -u root -p database_name     eventually change from utf8 to utf8mb4"""


##---- SET UP DATABASE CONNECTION -----#
#connect to db
db = MySQLdb.Connection(host="localhost", user="root", passwd="thekindisdead", db="halifax")
db.set_character_set('utf8')

#create a cursor
c=db.cursor()






#bounding box locations of cities  http://boundingbox.klokantech.com/

halifax = [-63.9844,44.421,-63.2071,44.8948]
nyc = [-74.1687,40.5722,-73.8062,40.9467]





## ---------   setting up the keys
consumer_key = 'XXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXX' 
access_token = 'XXXXXXXXXXXXX-XXXXXXXXXXXXXX'
access_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

class TweetListener(StreamListener):
# A listener handles tweets are the received from the stream.
#This is a basic listener that just prints received tweets to standard output

   def on_data(self, data):
        alldata = json.loads(data)


#tweet entity
      
        tweet = alldata["text"]
        tweetid = alldata["id"]
#user entity
        user = alldata["user"]["screen_name"]
        print ("user: "), user
        print ("tweet: "),tweet
        print ("tweetid: "), tweetid



        c.executemany(
      """INSERT INTO Halifax 
      VALUES (%s, %s, %s)""",
      [
      (tweetid, user, tweet),

      ] )

        print (" ")
        return True

   def on_error(self, status):
       print (status)

        



#printing all the tweets to the standard output
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

stream = Stream(auth, TweetListener())

#track a word
#t = u"toronto"
#stream.filter(track=[t])

#track a location
stream.filter(locations=nyc)
