
'use strict';

function newElement(name, attributes, children) {
	const e = document.createElement(name);
	for(const key in attributes) {
		if (key == 'content') {
			e.appendChild(document.createTextNode(attributes[key]));
		} else {
			e.setAttribute(key.replace(/_/g, '-'), attributes[key]);
		}
	}
	for(const child of children || []) {
		e.appendChild(child);
	}
	return e;
}

function matchChar(src, matches) {
	for (let i = 0; i < matches.length; i++) {
		if (src[0] == matches[i]) {
			return 1;
		}
	}
	return 0;
}

function matchNumber(src) {
	if (matchChar(src[0], ':!%()+,-*<=>[]{}|~^ \t\r\n') == 0) return 0;

	let i = 1;

	if (src[1] == '0' && matchChar(src[2], 'box') == 1) {
		i = 3;
	}
	
	while (!isNaN(src.substr(1, i)) && i < src.length && matchChar(src[i], ' \t\r\n') == 0) {
		i++;
	}
	return i-1;
}

function matchRegion(src, begin, end) {
	if (src.substr(0, begin.length) == begin) {
		for (let i = 1; i < src.length; i++) {
			if (src.substr(i, end.length) == end || i == src.length-1) {
				return i + end.length;
			}
		}
	}
	return 0;
}

function mina(code) {
	let output = '';
	let i = 0;

	while (i < code.length) {

		let match, tmp, type;

		tmp = matchChar(code.substr(i), ':!%&()+,-/.*<=>?[]{}|~^;');
		if (tmp > 0) {
			match = tmp;
			type = 'symbol';
		}

		tmp = matchNumber(code.substr(i-1));
		if (tmp > 0) {
			match = tmp;
			type = 'number';
		}

		// strings
		tmp = matchRegion(code.substr(i), '"', '"');
		if (tmp > 0) {
			match = tmp;
			type = 'string';
		}

		tmp = matchRegion(code.substr(i), '\'', '\'');
		if (tmp > 0) {
			match = tmp;
			type = 'string';
		}
		
		// comments
		tmp = matchRegion(code.substr(i), '//', '\n');
		if (tmp > 0) {
			match = tmp;
			type = 'comment';
		}

		tmp = matchRegion(code.substr(i), '/*', '*/');
		if (tmp > 0) {
			match = tmp;
			type = 'comment';
		}

		if (match > 0) {
			output += '<span class="' + type + '">' + code.substr(i, match) + '</span>';
			i += match;
		} else {
			output += code[i];
			i++;
		}
	}

	return output;
}

function formatCode(preNode) {
	
	const codeNode = preNode.getElementsByTagName('code')[0];

	const code = codeNode.textContent;

	// line numbers
	let lines = code.split('\n');
	let lineNumbers = '';

	if (lines[lines.length-1] == '') lines.pop();

	for(let i = 1; i <= lines.length; ++i){
		lineNumbers += i+'\n';
	}

	preNode.prepend(newElement('div', {'content': lineNumbers, 'class': 'line_numbers', 'aria-hidden': true}));
	// ----

	// high lighting
	if (codeNode.classList.contains('language-mina')) {
		codeNode.classList.add('mina');
		codeNode.innerHTML = mina(code);
	}
	// ----
}

function code() {
	[...document.getElementsByTagName('pre')].forEach(formatCode);
}
