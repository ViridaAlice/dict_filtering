import argparse, os, json, requests
from PIL import ImageDraw, Image, ImageTk
import urllib.request as request
import tkinter as tk

def displayImage(bbox_x1, bbox_y1, bbox_x2, bbox_y2, lit_name, page_name):
    """
    Given the bbox_edges as well as the library and document name, 
    visually display the bbox:
    """
    file_dir = os.path.dirname( __file__ )

    # Download respective .tif 
    local_file = file_dir+"/images/"+lit_name+"_"+page_name+".tif"
    if not os.path.exists(local_file):
        #print(local_file+" does not exist yet! Downloading...")
        file_url = 'https://webis56.medien.uni-weimar.de/vlp/scan-tif/'+lit_name+'/'+page_name+'.tif'
        # Download remote and save locally
        response = requests.head(file_url)
        if response.status_code == 200:
            request.urlretrieve(file_url, local_file)
        else:
            file_url = 'https://webis56.medien.uni-weimar.de/vlp/scan-tif/'+lit_name+'/'+page_name+'.TIF'
            request.urlretrieve(file_url, local_file)
    
    cropped_path = file_dir+"/images/"+lit_name+"_"+page_name+"_short.jpg"
    # Open image and display zoomed excerpt
    with Image.open(local_file) as img:
        cropped = img.crop((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        try: 
            cropped.save(cropped_path)
        except OSError:
            cropped_path = file_dir+"/images/"+lit_name+"_"+page_name+"_short.tif"
            cropped.save(cropped_path)

        
    if os.path.exists(local_file):
        try:
            os.remove(local_file)
        except OSError as e:
            print("could not remove file.")

    return cropped_path


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
    return False


def main():
    # Convert Input.jsonl to list of .json - Objects [ARGPARSE]
    with open("real/!outputfile_real_words.jsonl", 'r', encoding="utf-8") as json_file:
        json_list = list(json_file)
    
    i = 0
    # Go through every json object in jsonlist
    for json_str in json_list:
        # Open Output File [ARGPARSE]
        realWordsOutputFile = open('real/real_vers1.jsonl', 'a+', encoding="UTF-8")
        unsortedOutputFile = open('wrong/wrong_vers1.jsonl', 'a+', encoding="UTF-8")
        result = json.loads(json_str)
        current_word = result['source_word']
        
        cropped_path = displayImage(result['bbox_xy'][0][0],result['bbox_xy'][0][1],result['bbox_xy'][1][0],
                     result['bbox_xy'][1][1], result['document_id'], result['page_id'])
        
        def funcYes(event=None):
            json.dump(result, realWordsOutputFile)
            realWordsOutputFile.write("\n")
            realWordsOutputFile.close()
            main.destroy()
            
        def funcNo(event=None):
            json.dump(result, unsortedOutputFile)
            unsortedOutputFile.write("\n")
            unsortedOutputFile.close()
            main.destroy()

        main = tk.Tk()
        bRoll = tk.Button(text = "Yes", command = funcYes)
        cRoll = tk.Button(text = "No", command = funcNo)
        img = ImageTk.PhotoImage(Image.open(cropped_path))
        panel = tk.Label(main, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        cRoll.pack()
        bRoll.pack()
        tk.Label(main, text=str(i)+": "+current_word, font="10").pack()
        main.bind('y',funcYes)
        main.bind('n', funcNo)

        main.mainloop()
        i += 1
 
        
if __name__ == "__main__":
    main()