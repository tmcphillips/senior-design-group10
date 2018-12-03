graphid = graphid + 1
graph = graph.replaceAll(`&quot;`, `"`).replaceAll(`&gt;`, `>`)
d3.select(`#graph${graphid}`)
    .graphviz(options)
    .dot(graph)
    .render()
