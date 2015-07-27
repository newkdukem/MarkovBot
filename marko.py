import re
from collections import Counter
import random


import sys
import socket
import string


# A dictionary of words with the pobability of a word that follows
Rechnik = {} 

# A counter of words
Brojach = Counter()

# Feeding text variable
txtfile = re.findall(r'\w+', open('shakespeare.txt').read().lower())

# A function taking a list of words and returning a pair of consecutive words in a text
def give_me_pairs(words):
    prev = None
    for word in words:
        if not prev is None:
            yield prev, word
        prev = word

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

# Filling the dictionary of words
for segashen, sleden in give_me_pairs(txtfile):
    if not segashen in Rechnik: 
        Rechnik[segashen] = Counter()

    cnt = Rechnik[segashen]
    cnt[sleden] += 1

# Filling the counter of words
for word in txtfile:
    Brojach[word] += 1

# Making a counter from the raw input
def the_brain(in_words):
    the_sentence = Counter(re.findall(r'\w+', str(in_words).lower()))

    wordot = ""
    wordot = what_i_hear(the_sentence, Brojach)
    i = 0
    rechenica = []
    if not wordot:
        wordot = random.choice(Rechnik.keys())

    rechenica = [str(wordot).title()]
    while i < 15:
        wordot = weighted_random(Rechnik[wordot])
        rechenica.append(wordot)
        i += 1
    return str(' '.join(rechenica) + ".")

# # The irc part

HOST="irc.freenode.net"
PORT=6667
NICK="Markobototo"
IDENT="markobototo"
REALNAME="markobot"
readbuffer=""
CHANNEL="#lugola"

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHANNEL)

while True:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )


    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])

        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0]:
                if(char == "!"):
                    break
                if(char != ":"):
                    sender += char 

            for char in line[3]:
                if char == ":":
                    line[3] = ""
                else:
                    line[3] += char
                
            message = the_brain(str(' '.join(line[3:])))
            message.lstrip(":")
            print message
            s.send("PRIVMSG %s :%s \r\n" % (sender, message))