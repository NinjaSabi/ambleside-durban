import os

BASE = r'C:\Users\Kurt\OneDrive\Documents\Claude Projects\ambleside-durban'
path = os.path.join(BASE, 'about', 'our-story', 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use ASCII straight quotes to match the actual file
old = 'By "discipline" Mason did not mean punishment or rigidity \u2014 she meant the formation of good habits: of attention, of honesty, of perseverance. These habits, she believed, are the quiet engine of a well-lived life.'

new = 'By <em>\u201catmosphere\u201d</em> Mason meant the living environment in which a child learns \u2014 the tone, the relationships, and the spirit of the home and school. By <em>\u201cdiscipline\u201d</em> she did not mean punishment or rigidity, but the formation of good habits: of attention, honesty, and perseverance. And by <em>\u201clife\u201d</em> she meant that education is not a preparation for living \u2014 it is living itself, encountered through real ideas, real books, and real relationships.'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("PATCHED: about/our-story/index.html — CM quote (all three terms)")
else:
    print("NOT FOUND — checking what is in the file...")
    # Show the relevant lines
    for line in content.split('\n'):
        if 'discipline' in line.lower() and 'mason' in line.lower():
            print(f"  Found: {repr(line[:120])}")
