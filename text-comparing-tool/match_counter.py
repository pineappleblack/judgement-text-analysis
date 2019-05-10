import highlight
import os
import re

from tqdm import tqdm

def return_table_of_matches(filenames, courtname, window, porog, mode):
    if mode == 'fab':
        tag = 'fab'
        pattern = re.compile(f'\\\\{tag}b.*\\\\{tag}e', re.S|re.M)
    else:
        tag = ''
        pattern = re.compile(f'.*', re.S|re.M)

    files_structure = []

    # Create structure like a {'filename': 'text, contains in the tag'}
    for filename in filenames:
        try:
            fs = {}
            fs['name'] = filename.strip('.txt')
            with open('input_files/'+filename, encoding='utf-8') as f:
                fs['text'] = ' '.join( 
                                        [el.lstrip('\\'+tag+'b').rstrip('\\'+tag+'e') 
                                            for el in re.findall(pattern, f.read())
                                        ]
                )
            files_structure.append(fs)
        except:
            pass

    # Count matching percent
    matr = []
    for i, el1 in enumerate(tqdm(files_structure)):
        row = []
        for j, el2 in enumerate(files_structure):
            
            matches = 0
            words = el1['text'].split(' ')
            
            for k in range(len(words[:-1*(window-1)])):
                frag = ' '.join(words[k:k+window])
                if frag in el2['text']:
                    matches += 1
            
            row.append(round(matches/(len(words) - (window-1)), 2))
        matr.append(row)  

    fns = [el['name'] for el in files_structure]

    if courtname:
        table_filename = f'matches_{courtname}.csv'
    else:
        table_filename = 'matches.csv'

    # Create table of matching percents 
    with open(f'output_files/match_tables/{table_filename}', 'w') as f:
        head = ';'.join(fns)
        f.write(';'+head+'\n')
        for row, fn in zip(matr, fns):
            rstr = ';'.join([str(el) for el in row])
            f.write(fn + ';' + rstr + '\n')  

    # Create top of matched files
    top_of_matches = []
    for i in range(len(matr)):
        for j in range(i+1, len(matr[i])):
            if matr[i][j] > porog/100:
                top_of_matches.append([fns[i], fns[j], matr[i][j]])

    top_of_matches.sort(key=lambda el:el[2], reverse = True)

    return top_of_matches

def create_comparing_results_html(courtname, top_of_matches):
    with open('workfiles/page_header', encoding='utf-8') as f:
        page_header = f.read()   
    with open('workfiles/page_footer', encoding='utf-8') as f:
        page_footer = f.read()

    full_page = page_header  

    if courtname:   
        pagename = courtname
    else:
        pagename = 'matches_result'

    for el in tqdm(top_of_matches):
        full_page += '<table><tr><td class="text">' + highlight.return_highlighted_part(el[0], el[1]) + '</td><td class="text">' + \
                    highlight.return_highlighted_part(el[1], el[0]) + '</td></tr></table><hr>'

    full_page += page_footer

    if len(top_of_matches) > 0:
        with open(f'output_files/grouped_html/{pagename}.html', 'w', encoding='utf-8') as f:
            f.write(full_page) 

def create_personal_files_and_contents(courtname, top_of_matches):
    with open('workfiles/page_header', encoding='utf-8') as f:
        page_header = f.read()   
    with open('workfiles/page_footer', encoding='utf-8') as f:
        page_footer = f.read()

    if len(top_of_matches) > 0:
        newfile = False
        with open(f'output_files/pairs_and_contents/!contents.html', 'a+', encoding='utf-8') as f:
            filetext = f.read()

            if filetext == '':
                newfile = True
    
            if newfile:
                page_content = page_header
            else:
                page_content = filetext.strip(page_footer)

            if (courtname):
                page_content +=  f'<h2>{courtname}</h2>'

            for el in tqdm(top_of_matches):
                page_content += f'<li><a href="{el[0]}_{el[1]}.html">{el[0]} - {el[1]}: {(el[2] * 100):.2f}%</a>'
                highlight.create_highligthted_file(el[0], el[1])
                
            page_content += page_footer
            f.write(page_content)

def create_all_dirs():
    directory = "input_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "output_files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    directory = "output_files/match_tables"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "output_files/grouped_html"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "output_files/pairs_and_contents"
    if not os.path.exists(directory):
        os.makedirs(directory)

def match_files(filenames=None, courtname=None, window=10, porog=10, mode='fab'):

    create_all_dirs()

    if not filenames:
        filenames = [el for el in os.listdir('./input_files') if 'txt' in el]
    
    top_of_matches = return_table_of_matches(filenames, courtname, window, porog, mode)
   
    create_comparing_results_html(courtname, top_of_matches)
    create_personal_files_and_contents(courtname, top_of_matches)