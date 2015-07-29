import re
from collections import Counter
import random

# IRC related imports
import sys
import socket
import string


# A dictionary of words with the pobability of a word that follows
Nextword_count = {} 

# A counter of words
Word_count = Counter()

# A counter of pair of consecutive words
Pair_count = Counter()

# Feeding text variable
txtfile = re.findall(r'\w+', open('shakespeare.txt').read().lower())

# Having a dict with pair of words as key
word_pairs = {}

# A function taking a list of words and returning a pair of consecutive words in a text
def give_me_pairs(words):
    prev = None
    for word in words:
        if not prev is None:
            yield prev, word
        prev = word

# A function taking a list of words and returning a triplet of consecutive words in a text
def give_me_triplets(words):
    prev = None
    current = None
    for word in words:
        if not (prev and current) is None:
            yield prev, current, word 
        prev = current    
        current = word

# A function taking a word and returning (with a wheited random choice) the next word that follows
def weighted_random(counte):
    dalist = list(counte.elements())
    return random.choice(dalist)


# Taking probably the most rare word from the sentence
def what_i_hear(sentence, list_of_words):
    valid_words = list_of_words & sentence
    if valid_words == Counter():
        return ""
    rare = Counter({ key: value for key,value in list_of_words.items() if key in valid_words})
    rare = Counter(dict(rare.most_common()[:-3-1:-1]))
    return str(weighted_random(rare))

# Taking probably the most rare pair of words from the sentence


# Filling the dictionary of words
for current_word, next_word in give_me_pairs(txtfile):
    if not current_word in Nextword_count: 
        Nextword_count[current_word] = Counter()

    cnt = Nextword_count[current_word]
    cnt[next_word] += 1

# Filling the dict with pair of words as key
for prev_word, current_word, next_word in give_me_triplets(txtfile):
    word_tuple = prev_word, current_word
    if not (prev_word, current_word) in word_pairs: 
        word_pairs[word_tuple] = Counter()
    cnt = word_pairs[word_tuple]
    cnt[next_word] += 1

# Filling the counter of words
for word in txtfile:
    Word_count[word] += 1

# Filling the counter of pair of words
for word, next in give_me_pairs(txtfile):
    word_tuple = word, next
    Pair_count[word_tuple] += 1

# Making a counter from the raw input
def the_brain(in_words):
    the_sentence = Counter(re.findall(r'\w+', str(in_words).lower()))

    wordot = ""
    wordot = what_i_hear(the_sentence, Word_count)
    i = 0
    rechenica = []
    if not wordot:
        wordot = random.choice(Nextword_count.keys())

    rechenica = [str(wordot).title()]
    while i < 15:
        wordot = weighted_random(Nextword_count[wordot])
        rechenica.append(wordot)
        i += 1
    return str(' '.join(rechenica) + ".")

# Making the 2nd Brane
def the_brain2nd(in_words):
    the_sentence = Counter(re.findall(r'\w+', str(in_words).lower()))

    wordot = ""
    wordot = what_i_hear(the_sentence, Word_count)
    i = 0
    rechenica = []
    if not wordot:
        wordot = random.choice(Nextword_count.keys())

    rechenica = [str(wordot).title()]
    while i < 15:
        wordot = weighted_random(Nextword_count[wordot])
        rechenica.append(wordot)
        i += 1
    return str(' '.join(rechenica) + ".")

# # The irc part taken from http://archive.oreilly.com/pub/h/1968

# # IRC configuration
# HOST="irc.freenode.net"
# PORT=6667
# NICK="Markobototo"
# IDENT="markobototo"
# REALNAME="markobot"
# readbuffer=""
# CHANNEL="#lugola"

# # Connecting to IRC using socket
# s=socket.socket( )
# s.connect((HOST, PORT))
# s.send("NICK %s\r\n" % NICK)
# s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
# s.send("JOIN %s\r\n" % CHANNEL)


# # Put everything you receive in a readbuffer
# while True:
#     readbuffer=readbuffer+s.recv(4096)
#     temp=string.split(readbuffer, "\n")
#     readbuffer=temp.pop()

#     for line in temp:
#         line=string.rstrip(line)
#         line=string.split(line)

#         if(line[0]=="PING"):
#             s.send("PONG %s\r\n" % line[1])

#         if(line[1] == "PRIVMSG") and (line[2] == NICK):
#             sender = re.search(':(.*)!', line[0])
#             sender = sender.group(1)
#             line[3] = string.strip(line[3], ":")

#             print sender + ": " + str(' '.join(line[3:]))
            
#             message = the_brain(str(' '.join(line[3:])))
#             print "Bot: " + message
#             s.send("PRIVMSG %s :%s \r\n" % (sender, message))