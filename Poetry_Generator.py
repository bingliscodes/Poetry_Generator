#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import all necessary libraries; download corupuses; define corpus functions
"""Pairs in CMU is a 2D list of every word pair from the corpus text that match words in the dictionary, 
then cfd creates a conditional frequency distribution, which tracks the frequency of each pair"""

import nltk
import random
nltk.download('cmudict')
nltk.download('brown')
from nltk.corpus import cmudict
from nltk.corpus import brown
from nltk.util import bigrams
corp = brown.words(categories='science_fiction')
lc_corp = [w.lower() for w in corp]
pro = cmudict.dict()
pairs_in_cmu = [(x,y) for (x,y) in bigrams(lc_corp) if x in pro and y in pro]
cfd = nltk.ConditionalFreqDist(pairs_in_cmu)
from IPython.display import clear_output
#testing cmudict 
#print(pro['syllable'])


# In[2]:


"""define count_syllables(word). A function to return the number of syllables in a word.  This is important to help dictate the
"flow" of the poem that we are going to generate.
"""

def count_syllables(word):
    num_syllables = 0
   
    #isolate first pronunciation of word, will return a list of phones.
    ret = pro[word][0]
    
    #for each item in ret, check if last index of string is a digit.
    for i in ret:
        if i[-1].isdigit():
            num_syllables+=1
        else:
            continue
   
    return num_syllables

def test_count_syllables():
    print("testing count_syllables:")
    print("count_syllables('fire'). . .", end = " ")
    if(count_syllables('fire') == 2):
        print("success")
    else:
        print("failed")
    
    print("count_syllables('participated'). . .", end = " ")
    if(count_syllables('participated')==5):
        print("success")
    else:
        print("failed")
    print("count_syllables('madelyn'). . .", end = " ")
    if(count_syllables('madelyn')==3):
        print("success")
    else:
        print("failed")
    return
#test_count_syllables()


# In[5]:


#define sort_words(pro).  A function that takes the pronunciation dictionary and returns a list with pronunciation of n syllables
def sort_words(pro):
    sorted_words = [[], [], [], [], [], [], [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for w in pro:
        for p in pro[w]:
               # drop w into bin for syllables in p
            ret = count_helper(p)
            index = ret - 1
            if ret <= 22: 
                sorted_words[index].append(w)
            else:
                continue
                
    return sorted_words

def count_helper(pronunciation):
    num_syllables = 0
    #print(pronunciation)
   #isolate first pronunciation of word, will return a list of phones.
    #for each item in ret, check if last index of string is digit.
    for i in pronunciation:
        if i[-1].isdigit():
            num_syllables+=1
        else:
            continue
   
    return num_syllables

#let sorted_words be a two-dimensional array of words separated by number of syllables. The index corresponds to # of syllables-1
sorted_words = sort_words(pro)

#testing sort_words
def test_sort_words():

    print("sort_words[4]. . .", end = " ")
    if(len(sorted_words[4])==3924):
        print("success")
    else:
        print("failed")
    print("sort_words[6]. . .", end =" ")
    if(len(sorted_words[6])==126):
        print("success")
    else:
        print("failed")
    return

#test_sort_words()


# In[6]:


#define construct_next_words(sorted_words) as 
def construct_next_words(sorted_words):
    next_words = []
    cumulative_words = []
    for i in range(22):
        word_pairs = [(w, i + 1) for w in sorted_words[i]]
        cumulative_words.extend(word_pairs)
        next_words.append(list(set(cumulative_words)))
    return next_words


# In[7]:


#define other variables that we will need to start making lines

#define num_next, a helper function to determine sorted_next. This 
num_next = [(len(cfd[x]), x) for x in cfd]

#define sorted_next, a list of the 100 most "continuable" words. 
sorted_next = sorted(num_next)

#define good_starts, a list of the 100 most common starting words.  This is important to create more realistic sounding lines.
good_starts = [w for (n, w) in sorted_next[-100:]]

next_words = construct_next_words(sorted_words)


# In[8]:


#Now that we have defined everything required to construct a line. . .
def construct_line(total, previous_word = None):
    continuing = False
    if previous_word:
        # select the next word based on the previous one
        options = [(w,s) for (w,s) in next_words[total-1] if w in cfd[previous_word]]
        if len(options) > 0:
            continuing = True            
    
    if not continuing:
        # select the first word however we like from good_starts
        options = [(w,s) for (w,s) in next_words[total-1] if w in good_starts]
        word = random.choice(options)
        
    else:
        word = random.choice(options)
        
    remaining = total - word[1]
    line = [word[0]]
    
    if remaining == 0:
        line = [word[0]]
    else:
        line = [word[0]] + construct_line(remaining, word[0])
    
    return line

def test_haiku():
    print('category = science_fiction')
    print(' '.join(construct_line(5)))
    print(' '.join(construct_line(7)))
    print(' '.join(construct_line(5)))
    print()
    return

#test_haiku()


# In[9]:


"""Now we have a function that is capable of generated one line of n syllables at a time.  Now it is time to create
another function construct_poem() that takes in user input to generate a poem of a category from the brown corpus and length. 
"""


# In[10]:


def div_helper(n,y):
    num, div = n, y
    lc = ([num // div + (1 if x < num % div else 0) for x in range (div)])
    return lc


# In[11]:


#a dictionary of the categories labeled by number for accessibility reasons
categories = {1:'adventure', 2:'belles_lettres', 3:'editorial', 4:'fiction', 5:'government', 6:'hobbies', 7:'humor', 8:'learned', 9:'lore', 10:'mystery', 11:'news', 12:'religion', 13:'reviews', 14:'romance', 15:'science_fiction'}
def construct_poem():
    print("Welcome to Ben's poetry generator!\n")
    while True:
        #first create the user interface, where we will collect two variables: category, and length
        length = ""
        while True:
            num = int(input("Please select a category from the following options:\n 1.Adventure \n 2.Belles Letters \n 3.Editorial \
                            \n 4.Fiction \n 5.Government \n 6.Hobbies \n 7.Humor \n 8.Learned \n 9.Lore \n 10.Mystery \n 11.News \n 12.Religion \n 13.Reviews \n 14.Romance \n 15.Science-Fiction\n 16.Random\n 0.Exit\n"))
            if num not in (range(0,17)):
                print("Not an appropriate choice.")
            else:
                break

        if(num == 0):
            print("Goodbye!")
            return
        elif(num == 16):
            num = random.randrange(16)
            category = categories[num]
        else:
            print()
            print("Great choice!")
            category = categories[num]

        while True:
            length = input("How long would you like your poem to be?\nPlease type either short, medium, long, extra long, idc, or nevermind\n\n")

            if length not in ('short', 'medium', 'long', 'extra long', 'nevermind', 'idc'):
                print("Please enter a valid selection")
            else:
                if length == 'nevermind':
                    print("Sorry to see you go :(")
                    return
                print("Coming right up!")
                break

        #now we have a category stored in the category variable, and a length stored in the length variable.

        #next we have to set the new corpus and update/redefine necessary features.
        corp = brown.words(categories=category)
        lc_corp = [w.lower() for w in corp]
        pairs_in_cmu = [(x,y) for (x,y) in bigrams(lc_corp) if x in pro and y in pro]
        cfd = nltk.ConditionalFreqDist(pairs_in_cmu)

        """Next we use the length to determine how long the poem will be using the arbitrary calculations as follows: 
        short = 10-20 syllables
        medium = 20-35 syllables
        long = 35-45 syllables
        extra long = 45-65 syllables
        """

        if length == 'short':
            s_count = random.randrange(10,21)
            num_lines = random.randrange(3,5)
        elif length == 'medium':
            s_count = random.randrange(20,45)
            num_lines = random.randrange(3,7)
        elif length == 'long':
            s_count = random.randrange(35,75)
            num_lines = random.randrange(3,9)
        elif length == 'extra long':
            s_count = random.randrange(45,100)
            num_lines = random.randrange(3,11)
        else:
            s_count = random.randrange(10,66)
            num_lines = random.randrange(3,7)


        lines = div_helper(s_count, num_lines)
      #  print(s_count)
        #print(lines)
        num_lines = len(lines)
       # print(num_lines)
        #and then finally, we call construct_lines of arbitrary length
        print('Here is your personalized poem!\n')

        for x in range(len(lines)):
            print(' '.join(construct_line(lines[x])))
            x = x + 1


        repeat = input("would you like to make another poem? (please enter some variation of 'yes')\n")
        if repeat not in('yes', 'yep', 'yea', 'okay', 'ok', 'affirmative', 'ye', 'ya'):
            print('Pathetic. . .')
            break
        else:
            clear_output(wait=True)
            print('woohoo!')
            continue
    return  
#a helper function to determine the distribution of line lengths in syllables
print("test")
construct_poem()



# In[ ]:





# In[ ]:





# In[ ]:




