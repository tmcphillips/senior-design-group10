/*
Options for renderer
https://github.com/magjac/d3-graphviz#examples
*/

// we can turn off zoom in detailed view for enhanced viewing
let options1 = {
    zoom:false,
}

let options2 = {
    zoom:true,
}

let renderer1 = d3.select("#graph1")
                    .graphviz(options1)
let renderer2 = d3.select("#graph2")
                    .graphviz(options2)

renderer1.dot(raw_string_container.yw_raw_string1)
            .render()
renderer2.dot(raw_string_container.regular_raw_string1)
            .render()