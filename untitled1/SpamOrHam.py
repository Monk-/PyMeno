bagOfWords = {} # reprezentacja Bag of words
spamMessages = 0
hamMessages = 0
spamWords = 0
hamWords = 0

def checkTypeOfMessage(spamOrHam):
    if spamOrHam == "spam":
        return 1
    elif spamOrHam == "ham":
        return 0

def store(message, spamOrHam):
    global spamWords
    global hamWords
    global spamMessages
    global hamMessages
    global bagOfWords
    type = checkTypeOfMessage(spamOrHam)
    words = message.split(" ")
    for word in words:
        try:
            bagOfWords[word][type] += 1 #add existed word to spam or ham
        except KeyError:
            bagOfWords[word] = [1 - type, type] # create dict for word if doesn't exist
        spamWords += type
        hamWords += (1 - type)
    spamMessages += type
    hamMessages += (1 - type)

def guess(message):
    global spamWords
    global hamWords
    global spamMessages
    global hamMessages
    global bagOfWords
    allMessages = spamMessages + hamMessages
    spamProbability = spamMessages / allMessages # p(spam)
    hamProbability = hamMessages / allMessages   # p(ham)
    messageSpamProbability = 1
    messageHamProbability = 1
    words = message.split(" ")
    for word in words:#for each word in message
        messageSpamProbability *= bagOfWords[word][1] / spamWords
        messageHamProbability *= bagOfWords[word][0] / hamWords
    probThatMessageIsSpam  =  spamProbability * messageSpamProbability / \
                (spamProbability * messageSpamProbability + hamProbability * messageHamProbability)
    print("P(Spam|"+ message +") = " + str(probThatMessageIsSpam))

store("offer is secret", "spam")
store("click secret link", "spam")
store("secret sports link", "spam")
store("play sports today", "ham")
store("went play sports", "ham")
store("secret sports event", "ham")
store("sports is today", "ham")
store("sports cost money", "ham")

guess("secret is secret") #25/26