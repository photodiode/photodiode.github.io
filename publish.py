
import os
import re
import markdown
	
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
		html = markdown.markdown(text, extensions=['extra'])
	# ----

	date = '<time datetime="' + date.replace('.', '-') + '">' + date + '</time>\n'
	html = '<article>\n' + date + html + '\n</article>'
	html = template.replace('<!-- CONTENT -->', html, 1)
	
	newpath = 'article/' + name + '.html'

	with open(newpath, 'w') as f:
		f.write(html)
	# ----

	# make list entry
	title = re.search("^# .*", text).group()[2:]
	
	article_list += '<li><article>\n'
	article_list += '<a href="' + newpath + '"><h1>' + title + '</h1></a>\n'
	article_list += date
	article_list += '</article></li>\n'
	
# ----

print('making "index.html"...')
article_list = '<ul>\n' + article_list + '</ul>'
html = template.replace('<!-- CONTENT -->', article_list, 1)

with open('index.html', 'w') as f:
	f.write(html)
