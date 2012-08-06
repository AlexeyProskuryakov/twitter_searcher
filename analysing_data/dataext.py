# coding=utf-8

# Surik Sayadyan
# 2012

import html2text, urllib, re, lxml.html, markdown, sys, getopt

html2text.BODY_WIDTH = 0
html2text.SKIP_INTERNAL_LINKS = True
html2text.INLINE_LINKS = False

LimitValueForSentenceLength = 5 # граничное значение критерия длинны предложений
LimitValueForLinksCount = 0.9   # граничное значение критерия отношения колличетва слов со ссылок к колличеству слов
CountParagraphArticle = 3       # минимальное колличество параграфов в статье
CountWrongParagraphArticle = 3  # максимальное колличество параграфов, не несущих смысловой нагрузки

htmlOut = 0

def doConvert(url):
    # загрузка страницы
    j = urllib.urlopen(url)
    try:
        from feedparser import _getCharacterEncoding as enc
    except ImportError:
        enc = lambda x, y: ('utf-8', 1)
    text = j.read()
    encoding = enc(j.headers, text)[0]
    if encoding == 'us-ascii': encoding = 'cp1251'
    data = text.decode(encoding)
    # конвертирование html документа в markdown
    originalMarkdownDocument = html2text.html2text(data, url)
    markdownDocument = originalMarkdownDocument.split("\n")
    # поиск верхней границы статьи
    title = lxml.html.document_fromstring(text)
    startLine = findStartMerker(title.find(".//title").text, markdownDocument)
    # удаление текста выше верхней границы
    del markdownDocument[:startLine]
    # поиск нижней границы статьи
    skiplist = []
    endLine = findEndMarker(markdownDocument, skiplist)
    # удаление строк из skiplist
    for x in range(len(skiplist)-1,0, -1):
        markdownDocument.pop(skiplist[x])
    # отсечение статьи по нижней границе
    if endLine <> -1:
            del markdownDocument[endLine-len(skiplist)+1:]
    else:
        return;
    # замена ссылок линками
    fragment = listToString(markdownDocument)
    fragment = replaceInternalLinks(originalMarkdownDocument, fragment)
    global htmlOut
    if htmlOut == 1:
        # конвертирование markdown в html
        html = markdown.markdown(fragment)
        print html.encode('utf-8')
    else:
        print fragment.encode('utf-8')

def findStartMerker(title, markdownTextList):
    titleList = title.split(" ")

    for mask in range(len(titleList),0, -1):
        pos = 0
        result = -1
        while pos <= len(titleList) - mask:
            substring = ""
            for indx in range(pos, pos+mask):
                substring = substring + titleList[indx] + " "
            substring = substring[0:-1:]
            pos = pos+1

            candidat = -1
            for index in range(0,len(markdownTextList)):
                result = markdownTextList[index].find(substring)
                if result <> -1:
                    if substringInLineIsLink(substring, markdownTextList[index]):
                        if candidat == -1:
                            candidat = index
                    else:
                        candidat = index
                        break

            if candidat <> -1:
                #print "LINE = " + str(index) + " RESULT: " + substring.encode("utf-8")
                return candidat
    return -1

def findEndMarker(markdownDocument, skiplist):
    marker = 0
    startPost = False
    endMarker = -1
    for x in range(1, len(markdownDocument)):
        line = markdownDocument[x]
        if line == "" :
            paramS = "free"
            paramL = "free"
        else:
            paramS = avrLenSentCret(markdownDocument[x])
            paramL = refCountCret(markdownDocument[x])
            
        if paramS <> "free":
            paramS = float(paramS)
            paramL = float(paramL)

            if paramS == 0 and paramL == 0:
                continue

            # find start post
            if startPost == False:
                if paramL < LimitValueForLinksCount and paramS >= LimitValueForSentenceLength:
                    marker = marker + 1
                else:
                    marker = 0
                    skiplist.append(x)
                if marker >= CountParagraphArticle:
                        startPost = True
                        marker = 0

            # start marker found. Search stop
            if startPost == True:
                if marker >= CountWrongParagraphArticle:
                    # end search
                    #print "End search end marker x=" + str(endMarker)
                    return endMarker
                if paramL < LimitValueForLinksCount and paramS >= LimitValueForSentenceLength:
                    marker = 0
                    endMarker = -1
                else:
                    if endMarker == -1:
                        endMarker = x
                    marker = marker + 1

    # nothing found
    return -1

def refCountCret(text):
    # remove pictures
    pattern = r"(!\[[\w\W]*?\]\[[\d]*\])"
    number_re = re.compile(pattern, re.UNICODE)
    text = number_re.sub("", text)

    # remove links markers
    pattern = r"(\[[\d]*\])"
    number_re = re.compile(pattern, re.UNICODE)
    text = number_re.sub("", text)

    # remove symbols
    pattern = r"[^\w\s\[\]]"
    number_re = re.compile(pattern, re.UNICODE)
    text = number_re.sub("", text) + " "

    symbol = False
    isLink = 0
    wordsWithLink = 0
    wordsWithoutLink = 0
    for ch in text:
        if ch.isalpha() or ch.isdigit() :
            symbol = True
        if ch == "[" :
            # check symbols
            if symbol == True:
                symbol = False
                if isLink == 0:
                    wordsWithoutLink = wordsWithoutLink + 1
                else:
                    wordsWithLink = wordsWithLink + 1
            isLink = isLink + 1
        if ch == "]" :
            # check symbols
            if symbol == True:
                symbol = False
                if isLink == 0:
                    wordsWithoutLink = wordsWithoutLink + 1
                else:
                    wordsWithLink = wordsWithLink + 1
            isLink = isLink - 1
        if ch.isspace() :
            # check symbols
            if symbol == True:
                symbol = False
                if isLink == 0:
                    wordsWithoutLink = wordsWithoutLink + 1
                else:
                    wordsWithLink = wordsWithLink + 1
    if wordsWithoutLink == 0:
        wordsWithoutLink = 1
    return float(wordsWithLink)/float(wordsWithoutLink)

def avrLenSentCret(text):
    # remove pictures
    pattern = r"(!\[[\w\W]*?\]\[[\d]*\])"
    number_re = re.compile(pattern, re.UNICODE)
    text = number_re.sub("", text)

    pattern = r"[^\.\w\s]+"
    number_re = re.compile(pattern, re.UNICODE)
    text = number_re.sub("", text)
    if text == "":
        return 0
    sent = text.split(u". ")
    pattern = r"[\s]+"
    number_re = re.compile(pattern, re.UNICODE)
    sum = 0
    llen = 0
    for one in sent:
        if number_re.sub("", one) <> "":
            llen += 1
            for two in one.split(u" "):
                if two <> "":
                    sum += 1

    if not llen:
        return float(0)
    else:
        return float(sum)/float(llen)

def replaceInternalLinks(original, fragment):
    x = 0
    while 1:
        x = fragment.find("][", x)
        if x == -1:
            break
        x += 2
        start = x
        dig = ""
        while fragment[x].isdigit():
            dig = dig + fragment[x]
            x += 1
        if fragment[x] == ']':
            if dig == "":
                continue
            else:
                match = findLinkByNumber(original, dig)
                if match is not None:
                    fragment = fragment[0:start-1] + "(" + match + ")" + fragment[start+len(dig)+1:]
    return fragment

def findLinkByNumber(text, number):
    pattern = r"\[(" + number + r")\]: ([\w\W]*?) ?(\([\w\W]*?\))?\n"
    number_re = re.compile(pattern, re.UNICODE)
    match = number_re.search(text)
    if match is not None:
        return match.groups()[1]
    else:
        return None

def listToString(list):
    return "\n".join(list)

def substringInLineIsLink(substring, line):
    index = line.find(substring)
    if index == -1:
        return False
    for x in range(index-1, -1, -1):
        if line[x] == "]":
            return False
        if line[x] == '[':
            return True
    return False

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'Hh')
    except getopt.error, msg:
        print msg
        print "for help use -h"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h"):
            print "python dataext.py [http://sour.ce]\n-h\thelp\n-H\thtml output"
            sys.exit(0)
        if o in ("-H"):
            global htmlOut
            htmlOut = 1
    # process arguments
    if not len(args):
        print "Source url not found"
        sys.exit(2)
    else:
        doConvert(args[0])

if __name__ == "__main__":
    main()
    