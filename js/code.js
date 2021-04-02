
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

function formatCode(codeNode) {

	const code = codeNode.textContent;

	// line numbers
	let lines = code.split('\n');

	if (lines[lines.length-1] == '') lines.pop();

	let lineNumbers = '';

	for(let i = 1; i <= lines.length; ++i){
		lineNumbers += i+'\n';
	}

	//codeNode.innerHTML = '';
	codeNode.prepend(newElement('div', {'content': lineNumbers, 'class': 'line_numbers'}));
	//codeNode.appendChild(newElement('code', {'content': code}));
	// ----

	// high lighting

	// ----
}
