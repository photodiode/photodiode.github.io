
import os
import re
import markdown

md = markdown.Markdown(output_format="html5", extensions=['extra']);

website_name = 'photodiode'
root = 'docs/'
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

	# title & date header
	match = re.search("<h1>.*</h1>*", html)
	title = match.group()[4:-5]
	date  = '<time datetime="' + date.replace('.', '-') + '">' + date + '</time>\n'
	html  = html[0:match.span()[1]] + '\n' + date + html[match.span()[1]:]
	# ----

	# apply template
	article = '<article>\n' + html + '\n</article>'
	html = template.replace('<!-- TITLE -->', title + ' - ' + website_name, 1)
	html = html.replace('<!-- CONTENT -->', article, 1)
	# ----

	newpath = 'article/' + name + '.html'

	with open(root + newpath, 'w') as f:
		f.write(html)
	# ----

	# make list entry
	article_list += '\t\t\t<li>\n'
	article_list += '\t\t\t\t<a href="' + newpath + '">' + title + '</a>\n'
	article_list += '\t\t\t\t' + date
	article_list += '\t\t\t</li>\n'
	# ----
# ----

print('making "index.html"...')

article_list = '\t\t<ol>\n' + article_list + '\t\t</ol>'
html = template.replace('<!-- TITLE -->', website_name , 1)
html = html.replace('<!-- CONTENT -->', article_list, 1)

with open(root + 'index.html', 'w') as f:
	f.write(html)
