graphid = graphid + 1

d3.select(`#graph${graphid}`)
    .graphviz(options)
    .dot(graph)
    .render()
