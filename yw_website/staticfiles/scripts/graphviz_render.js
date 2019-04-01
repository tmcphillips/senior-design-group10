console.log(graph)
console.log(options)

d3.select(`#graph`)
    .graphviz(options)
    .renderDot(graph)
