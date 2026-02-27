import sys
import glob
import os
import nbformat
from deep_translator import GoogleTranslator
from time import sleep

def translate_markdown(text):
    if not text.strip():
        return text
    
    # We translate line by line or chunk by chunk to avoid API limits
    # and to preserve formatting somewhat (Google translator might mess up markdown)
    # A simple approach for this script:
    translator = GoogleTranslator(source='auto', target='ko')
    
    lines = text.split('\n')
    translated_lines = []
    
    for line in lines:
        if not line.strip():
            translated_lines.append(line)
            continue
            
        # Ignore lines that are raw HTML or image imports if possible, or attempt translation
        if line.lstrip().startswith('<') or line.lstrip().startswith('!['):
            translated_lines.append(line)
            continue
            
        try:
            # Simple chunk translation
            res = translator.translate(line)
            translated_lines.append(res if res else line)
            sleep(0.1)
        except Exception as e:
            print(f"Error translating: {e}")
            translated_lines.append(line)
            
    return '\n'.join(translated_lines)

def translate_notebook(notebook_path):
    print(f"Translating: {notebook_path}")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            cell.source = translate_markdown(cell.source)
            
    temp_path = f"/tmp/{os.path.basename(notebook_path)}"
    with open(temp_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    os.system(f"mv -f '{temp_path}' '{notebook_path}'")

if __name__ == '__main__':
    notebooks_to_translate = sorted(glob.glob("notebooks/0*.ipynb"))
    for nb in notebooks_to_translate:
        translate_notebook(nb)
    print("All notebooks translated!")
