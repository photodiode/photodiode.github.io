
import os
import re
import markdown

md = markdown.Markdown(output_format="html5", extensions=['extra']);

website_name = 'photodiode'
root = 'docs/'
src_dir = 'src/articles/'

# template
with open('src/template.html', 'r') as f:
	template = f.read()

def applyTemplate(title, content):
	html = template.replace('<!-- TITLE -->', title , 1)
	html = html.replace('<!-- CONTENT -->', content, 1)
	return html
# ----

def lineNumbers(html):

	output = ''
	code = 0

	for line in html.splitlines():

		pre = ''

		if not code:
			match = re.search('<pre><code\s?([\S]+)?>', line)
			if match:
				pre  = line[0:match.span()[1]]
				line = line[match.span()[1]:]
				code = 1

		else:
			match = re.search('</code></pre>', line)
			if match:
				code = 0

		if code:
			output += pre + '<line>' + line + '</line>\n'
		else:
			output += line + '\n'

	return output
# ----

files = os.listdir(src_dir)
article_list = ''

for filename in list(reversed(sorted(files))):

	print('converting "{:s}"...'.format(filename))

	parts = filename.split(' ', 1)
	date = parts[0]
	name = os.path.splitext(parts[1])[0]

	with open(src_dir+filename, 'r') as f:
		text = f.read()
	# ----
	
	
	html = md.convert(text)
	html = lineNumbers(html)

	# title & date header
	match = re.search('<h1>.*</h1>*', html)
	title = match.group()[4:-5]
	date  = '<time datetime="' + date.replace('.', '-') + '">' + date + '</time>\n'
	html  = html[0:match.span()[1]] + '\n' + date + html[match.span()[1]:]
	# ----

	# apply template
	article = '<article>\n' + html + '\n</article>'
	html = applyTemplate(title + ' - ' + website_name, article)
	# ----

	newpath = 'article/' + name + '.html'

	with open(root + newpath, 'w') as f:
		f.write(html)
	# ----

	# make list entry
	article_list += '\t\t\t\t<li>\n'
	article_list += '\t\t\t\t\t<a href="' + newpath + '">' + title + '</a>\n'
	article_list += '\t\t\t\t\t' + date
	article_list += '\t\t\t\t</li>\n'
	# ----
# ----

print('making "index.html"...')

article_list = '\t\t\t<h2>Articles</h2>\n\t\t\t<ol>\n' + article_list + '\t\t\t</ol>'
html = applyTemplate(website_name, article_list)

with open(root + 'index.html', 'w') as f:
	f.write(html)
