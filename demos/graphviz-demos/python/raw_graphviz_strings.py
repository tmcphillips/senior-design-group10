test1 = """graph {
    rankdir=LR; // Left to Right, instead of Top to Bottom
    a -- { b c d };
    b -- { c e };
    c -- { e f };
    d -- { f g };
    e -- h;
    f -- { h i j g };
    g -- k;
    h -- { o l };
    i -- { l m j };
    j -- { m n k };
    k -- { n r };
    l -- { o m };
    m -- { o p n };
    n -- { q r };
    o -- { s p };
    p -- { s t q };
    q -- { t r };
    r -- t;
    s -- z;
    t -- z;
}"""

yw_test1 = """digraph Workflow {
rankdir=LR
fontname=Helvetica; fontsize=18; labelloc=t
label=clean_name_and_date_workflow
subgraph cluster_workflow_box_outer { label=""; color=black; penwidth=2
subgraph cluster_workflow_box_inner { label=""; penwidth=0
node[shape=box style=filled fillcolor="#CCFFCC" peripheries=1 fontname=Helvetica]
node[shape=box style=filled fillcolor="#CCFFCC" peripheries=2 fontname=Helvetica]
validate_scientificName_field_of_data
validate_eventDate_field_of_data
edge[fontname=Helvetica]
validate_scientificName_field_of_data -> validate_eventDate_field_of_data [label=output1_data]
validate_scientificName_field_of_data -> validate_eventDate_field_of_data [label=record_id_data]
}}
subgraph cluster_input_ports_group_outer { label=""; penwidth=0
subgraph cluster_input_ports_group_inner { label=""; penwidth=0
node[shape=circle style=filled fillcolor="#FFFFFF" peripheries=1 fontname=Helvetica width=0.2]
input1_data_input_port [label=""]
}}
subgraph cluster_output_ports_group_outer { label=""; penwidth=0
subgraph cluster_output_ports_group_inner { label=""; penwidth=0
node[shape=circle style=filled fillcolor="#FFFFFF" peripheries=1 fontname=Helvetica width=0.2]
name_val_log_output_port [label=""]
output2_data_output_port [label=""]
date_val_log_output_port [label=""]
}}
edge[fontname=Helvetica]
local_authority_source_input_port -> validate_scientificName_field_of_data [label=local_authority_source]
input1_data_input_port -> validate_scientificName_field_of_data [label=input1_data]
edge[fontname=Helvetica]
validate_scientificName_field_of_data -> name_val_log_output_port [label=name_val_log]
validate_eventDate_field_of_data -> output2_data_output_port [label=output2_data]
validate_eventDate_field_of_data -> date_val_log_output_port [label=date_val_log]
}"""
