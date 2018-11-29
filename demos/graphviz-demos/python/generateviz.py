import graphviz
import raw_graphviz_strings

src = graphviz.Source(raw_graphviz_strings.yw_test1)
src.render(format='png')
src.view()
