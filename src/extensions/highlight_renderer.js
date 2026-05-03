const hljs = require('highlight.js');
const fs = require('fs');

let inputData = '';
process.stdin.on('data', chunk => {
    inputData += chunk;
});

process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);

        if (Array.isArray(data)) {
            const results = data.map(item => {
                const { code, language } = item;
                if (language && hljs.getLanguage(language)) {
                    return hljs.highlight(code, { language }).value;
                } else {
                    return hljs.highlightAuto(code).value;
                }
            });
            console.log(JSON.stringify(results));
        } else {
            const { code, language } = data;
            let highlightedCode = '';
            if (language && hljs.getLanguage(language)) {
                highlightedCode = hljs.highlight(code, { language }).value;
            } else {
                highlightedCode = hljs.highlightAuto(code).value;
            }
            console.log(highlightedCode);
        }
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
});