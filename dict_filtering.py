import argparse, os, json

def real_word(word):
    
    tags = [',', '.', ':', ';','‘','’',',,','“','„', '»', "«", '"', "'", " "]

    word = word.replace('ſ', 's')

    # Fully ignores all syntax listed within list "tags"
    # -> may be changed to (merely) simplify " and ' 
    for tag in tags:
        word = word.replace(tag, '')
        
    if word in open('german/german.dic', 'r', encoding="latin-1").read():
        return True
    else:
        return False


def main():
    # Convert Input.jsonl to list of .json - Objects [ARGPARSE]
    with open("completely_new_gt.jsonl", 'r', encoding="utf-8") as json_file:
        json_list = list(json_file)

    # Open Output File [ARGPARSE]
    realWordsOutputFile = open('outputfile_real_words.jsonl', 'w+', encoding="UTF-8")
    unsortedOutputFile = open('outputfile_unsorted_words.jsonl', 'w+', encoding="UTF-8")
    
    # Go through every json object in jsonlist
    for json_str in json_list:
        result = json.loads(json_str)
        current_word = result['source_word']

        if real_word(current_word):
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