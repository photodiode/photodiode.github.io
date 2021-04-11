
'use strict';

function matchChar(src, matches) {
	let i = matches.indexOf(src[0]);
	return (i != -1) ? 1 : 0;
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

function matchRegion(src, start, end) {
	if (src.substr(0, start.length) != start) return 0;
	for (let i = 1; i < src.length; i++) {
		if (src.substr(i, end.length) == end || i == src.length-1) {
			return i + end.length;
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
		if (tmp) {match = tmp; type = 'symbol';}

		tmp = matchNumber(code.substr(i-1));
		if (tmp) {match = tmp; type = 'number';}

		// strings
		tmp = matchRegion(code.substr(i), '"', '"');
		if (tmp) {match = tmp; type = 'string';}

		tmp = matchRegion(code.substr(i), '\'', '\'');
		if (tmp) {match = tmp; type = 'string';}
		
		// comments
		tmp = matchRegion(code.substr(i), '//', '\n');
		if (tmp) {match = tmp; type = 'comment';}

		tmp = matchRegion(code.substr(i), '/*', '*/');
		if (tmp) {match = tmp; type = 'comment';}

		if (match) {
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
	const code     = codeNode.textContent;

	// line numbers
	let lines = code.split('\n');
	if (lines.slice(-1) == '') lines.pop();
	let lineNumbers = lines.map((_, i) => (i+1)).join('\n');

	let lineNumbersDiv = document.createElement('div');
	    lineNumbersDiv.setAttribute('class', 'line_numbers');
	    lineNumbersDiv.setAttribute('aria-hidden', true);
	    lineNumbersDiv.appendChild(document.createTextNode(lineNumbers));
	
	preNode.prepend(lineNumbersDiv);
	// ----

	if (codeNode.classList.contains('language-mina')) {
		codeNode.innerHTML = mina(code);
	}
}

function code() {
	[...document.getElementsByTagName('pre')].forEach(formatCode);
}
