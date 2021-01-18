import questionGeneratorFunction

def main():
    qg = questionGeneratorFunction.QuestionGenerator()

    inputTextPath = "./DB/sinput.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")

    inputText = readFile.read()

    questionList = qg.aqgParse(inputText)
    qg.display(questionList)

    return 0

if __name__ == "__main__":
    main()

