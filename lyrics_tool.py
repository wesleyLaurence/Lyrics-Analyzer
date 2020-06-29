from sql_kit import SQL_kit

import lyricsgenius
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import getpass
import pathlib
from pathlib import Path


class Lyrics_Tool:
    
    def __init__(self):
        
        # genius API key
        self.genius_api_key = getpass.getpass('Enter Genius API Key: ')
        
        # connect to MySQL database
        self.database_connect = False
        self.userID = None
        self.password = None
        self.database = 'lyrics'
        
        file_path = Path(str(pathlib.Path(__file__).parent.absolute())+'/'+'curse_words.csv')
   
        # import xlsx file of curse words from Wiki, convert to list
        self.curse_words_df = list(pd.read_csv(file_path,encoding='latin1')['curse_words'])
        self.curse_words_list = []

        for word in self.curse_words_df:
            new_word = word.replace('\xa0','')
            self.curse_words_list.append(new_word)
            
            
    def connect(self):
        """ Enter MySQL credentials and connect to database"""
        self.database_connect = True
        self.userID = input('User ID: ')
        self.password = getpass.getpass('Password: ')
        

    def show_lyrics(self,song_name, artist_name):
        """ print song lyrics """
        genius = lyricsgenius.Genius(self.genius_api_key)
        song = genius.search_song(str(song_name), str(artist_name))
        return print(song.lyrics)
        
    
    def vet(self,song_name, artist_name):
        
        """ 
        This method checks if a song has explicit lyrics. 
        You input a song & artist and it retrieves the lyrics from Genius API.
        It returns True if the song is clean and False if explicit lyrics are detected
        """

        # use Genius API to retreive lyrics data
        genius = lyricsgenius.Genius(self.genius_api_key)
        song = genius.search_song(str(song_name), str(artist_name))
        
        # remove unneccesary characters and split string into list
        lyrics = song.lyrics
        remove_characters = [".", ",", "!", "'", '"', "?", "(", ")","[","]"]
        for character in remove_characters:
            lyrics = lyrics.replace(character, "")             
        lyrics = lyrics.split()

        # list to store curse words in song    
        song_curse_words = []

        # iterate through each word in lyrics, check if it is in curse_words_list
        # if a word is a curse word, store in song_curse_words list
        for word in lyrics:
            word=word.lower()
            
            if word in self.curse_words_list:
                song_curse_words.append(word) 
            else:
                pass

        # If song is clean...
        if len(song_curse_words) == 0:
            clean=True
            print("\nClean lyrics")

        # If song is explicit...
        else: 
            clean=False
            print('\nExplicit lyrics detected!\n')   

        if self.database_connect:
            # update MySQL database 
            db = SQL_kit(self.userID, self.password, self.database)
            db.cleanlyrics_table(song_name, artist_name, clean)
        else:
            pass
        
        return clean
    
    
    def unique_word_count(self, song_name, artist_name):
        
        """
        lyrics unique value counts series
        
        """
        
        # use Genius API to retreive lyrics data
        genius = lyricsgenius.Genius(self.genius_api_key)
        song = genius.search_song(str(song_name), str(artist_name))

        # remove unneccesary characters and split string into list
        lyrics = song.lyrics
        remove_characters = [".", ",", "!", "'", '"', "?", "(", ")","[","]"]
        for character in remove_characters:
            lyrics = lyrics.replace(character, "")             
        lyrics = lyrics.split()
        
        # remove most common words
        common_words = ['a','an','and','the','it']
        comp_lyrics = []
        for item in lyrics:
            item=item.lower()
            if '[' in item or ']' in item or item in common_words:
                pass
            else:
                comp_lyrics.append(item)
        
        # unique word value count series
        lyrics = pd.Series(comp_lyrics).value_counts()
        lyrics = pd.DataFrame(lyrics,columns=['count'])
        lyrics.index.name = 'word'
            
        # create sample of 20 unique words in lyrics
        sample = list(lyrics.index)[:20]
        
        # container for final concatenated sample
        final_sample = sample[0]
        for item in sample[1:]:
            final_sample = final_sample+" "+item
            
        return lyrics
    
    
    def lyrics_sample(self, song_name, artist_name):
        
        # use Genius API to retreive lyrics data
        genius = lyricsgenius.Genius(self.genius_api_key)
        song = genius.search_song(str(song_name), str(artist_name))
        
        # remove unneccesary characters and split string into list
        lyrics = song.lyrics
        remove_characters = [".", ",", "!", "'", '"', "?", "(", ")",'[',']']
        for character in remove_characters:
            lyrics = lyrics.replace(character, "")             
        lyrics = lyrics.split()
        
        # create sample of 20 unique words in lyrics
        sample = list(lyrics)[:20]
        
        # container for final concatenated sample
        final_sample = sample[0]
        for item in sample[1:]:
            final_sample = final_sample+" "+item
            
        return final_sample
        
        
        
    def data(self): 
        """ Returns a DataFrame of all information in the cleanlyrics table """
        db = SQL_kit(self.userID, self.password, self.database)
        return db.get_data()
    
    
    def dashboard(self):
        """ Visual dashboard displaying trends in the cleanlyrics table """
        df = self.data()
        
        """ Top 3 Instruments """

        objects = ['Clean','Explicit']
        y_pos = np.arange(len(objects))

        # get class info from class_absence_stats dataframe
        performance = list(df['Clean'].value_counts())
        #fig3 = plt.figure(3) 
        plt.bar(y_pos, performance, color='mediumblue', align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.title('Clean vs Explict')
        plt.ylabel('Number of Songs')
        plt.xlabel('Lyrics')

        plt.show()