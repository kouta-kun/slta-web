
async function loadMarkDown(url, htmlCallback) {
    let converter = new showdown.Converter();
    let text = await (await fetch(url)).text();
    htmlCallback(converter.makeHtml(text));
}

function setSiteHtml(html) {
    document.getElementById('siteBox').innerHTML=html;
}

function strMarkdown(str, htmlContentCallback, finalCallback) {
    let converter = new showdown.Converter();
    htmlContentCallback(converter.makeHtml(str));
    if(finalCallback !== undefined) finalCallback();
}
