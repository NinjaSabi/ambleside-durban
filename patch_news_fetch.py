import os

BASE = r'C:\Users\Kurt\OneDrive\Documents\Claude Projects\ambleside-durban'

# Fix 1: news/index.html — use download_url from API response (pre-encoded)
path = os.path.join(BASE, 'news', 'index.html')
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace fetchRaw(f.path) with fetch of download_url directly
old = """    const posts = await Promise.all(mdFiles.map(async (f, i) => {
      const text = await fetchRaw(f.path);"""
new = """    const posts = await Promise.all(mdFiles.map(async (f, i) => {
      const text = f.download_url ? await fetch(f.download_url).then(r=>r.ok?r.text():null) : null;"""
c = c.replace(old, new, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('PATCHED: news/index.html')

# Fix 2: news/article/index.html — encode path segments when fetching
path2 = os.path.join(BASE, 'news', 'article', 'index.html')
with open(path2, 'r', encoding='utf-8') as f:
    c2 = f.read()

old2 = """  async function fetchRaw(path) {
    try {
      const r = await fetch(`${RAW}/${path}`);
      return r.ok ? r.text() : null;
    } catch { return null; }
  }"""
new2 = """  async function fetchRaw(path) {
    try {
      const encoded = path.split('/').map(s => encodeURIComponent(s)).join('/');
      const r = await fetch(`${RAW}/${encoded}`);
      return r.ok ? r.text() : null;
    } catch { return null; }
  }"""
c2 = c2.replace(old2, new2, 1)

with open(path2, 'w', encoding='utf-8') as f:
    f.write(c2)
print('PATCHED: news/article/index.html')
print('Done — commit and push.')
