import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 

f = open("input.txt","r")
content = f.read()

text = sent_tokenize(content)

NNP = set()
QUE = []
ANS = []
for pos in range(len(text)):
    i = text[pos]
    if " " not in i.split(",")[0]:
        m = i.split(",")
        i = ""
        i+=m[1][1].upper()
        i+=m[1][2:]
        for k in range(2,len(m)):
            i+=m[k]

    sent = ""
    for l in i:
        if l in '"':
            sent+=""
        elif l in '.,':
            sent+=" "+l
        else:
            sent+=l

    tagged = nltk.pos_tag(sent.split())
    question = ""
    answer = []
    k = -1
    done = -1
    none = -1
    for posW in range(len(tagged)-1):
        if tagged[posW][1]!="NNP" and posW != 0 and str(tagged[posW][0])[0].isupper():
            tagged[posW] = (tagged[posW][0],"NNP")
        elif posW != 0 and tagged[posW-1][1]=="NNP" and tagged[posW+1][1]=="NNP" and tagged[posW][0] in "&-~":
            tagged[posW] = (tagged[posW][0],"NNP")
    
    for posW in range(len(tagged)):
        j = tagged[posW]
        if j[0]=='.':
            question += '?'
        elif j[1]!="NNP" and j[1]!="NNS" and j[1]!="NN":
            question += j[0]+" "
        elif done==-1:
            if posW == 0:
                question += "Who "
            else:
                question += "______ "
            none = posW
            answer.append(j[0]+" ")
            done = posW
            k += 1
        elif posW-1==done and none==posW-1:
            answer[k] += j[0]+" "
            done = posW
            none = posW
        elif posW-1!=done:
            question += j[0]+" "
            answer.append(j[0]+" ")
            done = posW
            k += 1
        else:
            question += j[0]+" "
            answer[k] += j[0]+" "
            done = posW
    # print(question)
    # print(answer)
    if none != -1:
        QUE.append(question.strip())
        ANS.append(answer[0].strip().lower())
        for a in answer:
            NNP.add(a.strip().lower())

# print(QUE)
# print(ANS)
# print(NNP)

mcqtf = ""

import random

for i in range(len(QUE)):
    mcqtf += "Q"+""+". "+QUE[i]+"\n"
    corps = random.randint(0,3)
    opt = NNP.difference({ANS[i]})
    optns = []
    for j in range(3):
        optns.append(list(opt)[random.randint(0,len(opt)-1)])
        opt = opt.difference(set(optns))
    opt = []
    k = 0
    for j in range(4):
        if j == corps:
            opt.append(ANS[i]+" (correct)")
        else:
            opt.append(optns[k])
            k += 1
    optns = opt
    for opt in range(4):
        if opt == 0:
            mcqtf += "A)"+str(optns[opt])+"\n"
        elif opt == 1:
            mcqtf += "B)"+str(optns[opt])+"\n"
        elif opt == 2:
            mcqtf += "C)"+str(optns[opt])+"\n"
        else:
            mcqtf += "D)"+str(optns[opt])+"\n\n"

print(mcqtf)
f = open("output.txt", "w")
f.write(mcqtf)
f.close()