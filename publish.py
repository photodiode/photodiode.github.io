
import os
import re
import markdown

md = markdown.Markdown(extensions=['extra']);
	
src_dir = 'src/articles/'
files = os.listdir(src_dir)

with open('src/template.html', 'r') as f:
	template = f.read()
# ----

article_list = ''


for filename in list(reversed(sorted(files))):

	print('converting "{:s}"...'.format(filename))

	parts = filename.split(' ', 1)
	date = parts[0]
	name = os.path.splitext(parts[1])[0]

	with open(src_dir+filename, 'r') as f:
		text = f.read()
		html = md.convert(text)
	# ----

	date = '<time datetime="' + date.replace('.', '-') + '">' + date + '</time>\n'
	html = '<article>\n' + date + html + '\n</article>'
	html = template.replace('<!-- CONTENT -->', html, 1)
	
	newpath = 'article/' + name + '.html'

	with open(newpath, 'w') as f:
		f.write(html)
	# ----

	# make list entry
	match = re.search("^# .*", text)
	title = match.group()[2:]
	summary = re.search("[\s\S]*(?=\n---)", text[match.span()[1]:]).group().strip()

	article_list += '<li><article><a href="' + newpath + '">\n'
	article_list += '<h1>' + title + '</h1>\n'
	article_list += date
	article_list += md.convert(summary) + '\n'
	article_list += '</a></article></li>\n'
	# ----
# ----

print('making "index.html"...')
article_list = '<ul>\n' + article_list + '</ul>'
html = template.replace('<!-- CONTENT -->', article_list, 1)

with open('index.html', 'w') as f:
	f.write(html)
