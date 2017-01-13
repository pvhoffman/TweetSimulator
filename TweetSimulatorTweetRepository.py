import os.path
import sqlite3
import TweetSimulatorConfig
import TweetSimulatorTweet

class TweetSimulatorTweetRepository:

    def __init__(self):
        self._config = TweetSimulatorConfig.TweetSimulatorConfig()
        dbexists = os.path.isfile(self._config.DatabasePath())
        self._connection = sqlite3.connect(self._config.DatabasePath())
        if dbexists == False:
            self._init_database()

    def insert(self, tweet):
        print "Inserting tweet with id %s" % (tweet.id)
        c = self._connection.cursor()
        c.execute("INSERT INTO Tweets (TWEET_ID, TWEET_DATE, TWEET_TEXT) VALUES (?, ?, ?)", (tweet.id, tweet.date, tweet.text))
        self._connection.commit()

    def select_all(self):
        res = []
        c = self._connection.cursor()
        c.execute('select tweet_text from tweets order by tweet_id')
        for result in c.fetchall():
            res.append(result[0])
        return '\n'.join(res) 

    def count(self):
        c = self._connection.cursor()
        c.execute("SELECT COUNT(*) FROM Tweets")
        r = c.fetchone()
        return r[0]

    def getVerificationCode(self):
        c = self._connection.cursor()
        c.execute("SELECT SETTING_VCODE FROM Settings")
        r = c.fetchone()
        return r[0]

    def setVerificationCode(self, vcode):
        c = self._connection.cursor()
        c.execute("UPDATE Settings SET SETTING_VCODE = ? WHERE 1 = 1", (vcode,))
        self._connection.commit()


    def _init_database(self):
        self._connection.execute("""CREATE TABLE Tweets(
            TWEET_ID INT NOT NULL
            , TWEET_DATE TEXT NOT NULL
            , TWEET_TEXT TEXT NOT NULL)""")
        self._connection.execute("""CREATE TABLE Settings(
            SETTING_VCODE TEXT NOT NULL)""")

        c = self._connection.cursor()
        c.execute("INSERT INTO Settings (SETTING_VCODE) VALUES ('None')")
        self._connection.commit()



