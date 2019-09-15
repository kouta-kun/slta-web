
async function loadMarkDown(url, htmlCallback) {
    let converter = new showdown.Converter();
    let text = await (await fetch(url)).text();
    htmlCallback(converter.makeHtml(text));
}

function setSiteHtml(html) {
    document.getElementById('siteBox').innerHTML=html;
}

function strMarkdown(str, htmlCallback) {
    let converter = new showdown.Converter();
    htmlCallback(converter.makeHtml(str));
}
