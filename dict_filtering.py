import argparse, os, json


def real_word(word):
    
    tags = [',', '.', ':', ';','‘','’',',,','“','„', '»', "«", '"', "'", " ", "-"]

    word = word.replace('ſ', 's')

    # Fully ignores all syntax listed within list "tags"
    # -> may be changed to (merely) simplify " and ' 
    for tag in tags:
        word = word.replace(tag, '')
        
    wordfile = open('german/wordlist-german.txt', 'r', encoding="latin-1")
    if "\n"+word+"\n" in wordfile.read():
        wordfile.close()
        return True
    else:
        return False
    
def checkWord(word):
    if real_word(word):
        return True
    for i in range(2,len(word)):
        first_part = word[:i]
        second_part = word[i:]
        if real_word(first_part) and checkWord(second_part):
            return True
        #if (real_word(first_part) and checkWord(second_part)):
        #    return True
    return False


def main():
    # Convert Input.jsonl to list of .json - Objects [ARGPARSE]
    with open("inputfile_unsorted_words.jsonl", 'r', encoding="utf-8") as json_file:
        json_list = list(json_file)

    # Open Output File [ARGPARSE]
    realWordsOutputFile = open('outputfile_real_words_vers2.jsonl', 'a+', encoding="UTF-8")
    unsortedOutputFile = open('outputfile_unsorted_words_vers2.jsonl', 'w+', encoding="UTF-8")
    
    # Go through every json object in jsonlist
    for json_str in json_list:
        result = json.loads(json_str)
        current_word = result['source_word']

        print(current_word)
        if checkWord(current_word):
            json.dump(result, realWordsOutputFile)
            realWordsOutputFile.write("\n")
        else:
            json.dump(result, unsortedOutputFile)
            unsortedOutputFile.write("\n")
    
    
    """
fullOutputFile.close()
    
    # Split outputfile into the four respective HitTypes 
    with open(args.output_file+'/entire_gt.txt') as f:
        lines = f.read().splitlines()
    
    generalAnalysis(lines, args.output_file)
    """
 
        
if __name__ == "__main__":
    main()