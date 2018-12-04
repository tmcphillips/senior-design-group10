let options = {
    "zoom":false,
};
let graph = "";
let graphid = 0;

String.prototype.replaceAll = function(search, replacement){
    return this.replace(new RegExp(search, 'g'), replacement);
}

repl = [
    [
        `&quot`,
        `"`,
    ],
    [
        `&gt`,
        `>`,
    ],
]
