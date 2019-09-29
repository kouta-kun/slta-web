const classMap = {
  blockquote: 'blockquote text-center'
}

const bindings = Object.keys(classMap)
  .map(key => ({
    type: 'output',
    regex: new RegExp(`<${key}(.*)>`, 'g'),
    replace: `<${key} class="${classMap[key]}" $1>`
  }));

const ext_source = { type: 'lang', regex: /source! (.*)/g, replace: '<footer class="blockquote-footer">$1</footer>'};

const ext_video = { type: 'lang', regex: /video! (.*)/g, replace: '<video controls><source src="$1"></video>'};

const conv = new showdown.Converter({
  extensions: [...bindings, ext_source, ext_video]
});

async function loadMarkDown(url, htmlCallback) {
    let text = await (await fetch(url)).text();
    htmlCallback(conv.makeHtml(text));
}

function setSiteHtml(html) {
    document.getElementById('siteBox').innerHTML=html;
}

function strMarkdown(str, htmlContentCallback, finalCallback) {
    htmlContentCallback(conv.makeHtml(str));
    if(finalCallback !== undefined) finalCallback();
}
