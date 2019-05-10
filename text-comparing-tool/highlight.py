import json
import os
import re


# Returns list of matched words positions
def get_matched_words(text1, text2, window):
    matched_words = set()

    words = text1.split(' ')

    # Make {window}-words fragments from first file and search for them in second file 
    for k in range(len(words[:-1*(window-1)])):
        frag = ' '.join(words[k:k+window])
        if frag in text2:
            matched_words.update([el for el in range(k, k+window)])
            
    return list(matched_words)


# Changes matched words' position list to list of start and end of matching positions
def get_markers_position(matched_words):
    markers = []
    last_marked = -1

    for i in matched_words: 
        if i == matched_words[0]:
            marker = [i]
        elif i == matched_words[-1]:
            marker.append(matched_words[-1])
            markers.append(marker)
        else:
            if (i - last_marked) != 1:
                marker.append(last_marked)
                markers.append(marker)
                marker = [i]

        last_marked = i

    markers.sort()

    return markers


# Adds html-tags to colorize the text
def mark_text(text, markers, tags):
    
    words = text.split(' ')
    
    for el in markers[::-1]:
        words = words[:el[0]] + [f'<div class = "marked">'] \
            + words[el[0]:el[1]+1] + ['</div>'] + words[el[1]+1:]

    out_text = ' '.join(words)

    # Close conflicted tags
    for tag in tags:
        tag = tag.replace('\\', '\\\\')
        out_text = re.sub(f'<div class = "marked">(.*?){tag}(.*)</div>', \
        rf'<div class = "marked">\1</div>{tag}<div class = "marked">\2</div>', out_text, flags=re.S|re.M)

    return out_text


# Replaces our tags for html
def replace_tags(text, replacements):
    for tag in replacements:
        text = text.replace(tag, replacements[tag])
    return text

# Adds spaces to all space symbols to count words correctly
def add_spaces(text):
    space_symbols = ['\n', '\t']
    for s in space_symbols:
        text = text.replace(s, ' ' + s + ' ')
    return text

# Deletes junk spaces
def preprocess_text(text):
    text = re.sub('(\n){3,}', r'\1\1', text)
    text = add_spaces(text)
    return text

# Main function
def create_highligthted_file(file1, file2, window = 10):
    
    with open('workfiles/replacements.json') as f:
        replacements = json.loads(f.read())

    with open(f'input_files/{file1}.txt', encoding='utf-8') as f:
        text1 = preprocess_text(f.read())
    with open(f'input_files/{file2}.txt', encoding='utf-8') as f:
        text2 = preprocess_text(f.read())
        
    matched_words = get_matched_words(text1, text2, window)
    markers = get_markers_position(matched_words)
    marked_text = mark_text(text1, markers, replacements)
    marked_text = replace_tags(marked_text, replacements)

    with open('workfiles/page_header') as f:
        page_header = f.read()   
    with open('workfiles/page_footer') as f:
        page_footer = f.read()

    info_header = f'<h1>Фрагменты файла {file1}.txt, которые присутствуют в {file2}.txt</h1><br>'    

    with open('output_files/pairs_and_contents/' + file1 + '_' + file2 + '.html', 'w', encoding = 'utf-8') as f:
        f.write(page_header + info_header + marked_text.replace('\n', '<br>\n') + page_footer)
        

# Returns a part of document to create one page        
def return_highlighted_part(file1, file2, window = 10):

    with open('workfiles/replacements.json') as f:
        replacements = json.loads(f.read())

    with open(f'input_files/{file1}.txt', encoding='utf-8') as f:
        text1 = preprocess_text(f.read())
        
    with open(f'input_files/{file2}.txt', encoding='utf-8') as f:
        text2 = preprocess_text(f.read())
        
    matched_words = get_matched_words(text1, text2, window)
    markers = get_markers_position(matched_words)
    
    marked_text = mark_text(text1, markers, replacements)
    marked_text = replace_tags(marked_text, replacements)

    info_header = f'<h1>Фрагменты файла {file1}.txt, которые присутствуют в {file2}.txt</h1><br>'    
    
    return info_header + marked_text.replace('\n', '<br>\n') + '<br>\n<br>\n'