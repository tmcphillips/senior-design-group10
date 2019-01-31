from autofixture import AutoFixture
from django.core.management.base import BaseCommand
from website.models import Workflow, Version, Tag, Run, File, RunFile, TagWorkflow, TagVersion, TagRun, TagFile
import uuid

# Graphviz output string for an example workflow
DUMMY_GRAPH_STRING = """digraph Workflow {
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

# TODO: Add file outputs
# > recon
# > extract
# > model/graph


class Command(BaseCommand):

    help = 'create_test_database creates mock entries into the YesWorkflow database. This command should only be run in a test environment.'

    def add_arguments(self, parser):
        parser.add_argument('--entries', type=int, dest='entries',
                            help='Number of mock entries to create. Default is 10.')

    def _create_tags(self):
        tag_fixture = AutoFixture(Tag)
        _ = tag_fixture.create(self.num_entries)

    def _create_workflows(self):
        workflow_fixture = AutoFixture(Workflow, field_values={'user': None})
        _ = workflow_fixture.create(self.num_entries)

    def _create_versions(self):
        version_fixture = AutoFixture(
            Version, field_values={'yw_graph_output': DUMMY_GRAPH_STRING})
        _ = version_fixture.create(self.num_entries)

    def _create_runs(self):
        run_fixture = AutoFixture(Run)
        _ = run_fixture.create(self.num_entries)

    def _create_files(self):
        for i in range(0, self.num_entries):
            files_fixture = AutoFixture(
                File, field_values={'file_checksum': str(uuid.uuid4()), 'input_data': None})
            _ = files_fixture.create_one()

    def _create_run_files(self):
        runfile_fixture = AutoFixture(RunFile)
        _ = runfile_fixture.create(self.num_entries)

    def _create_tag_workflow(self):
        tagworkflow_fixture = AutoFixture(TagWorkflow)
        _ = tagworkflow_fixture.create(self.num_entries)

    def _create_tag_run(self):
        tagrunfixture = AutoFixture(TagRun)
        _ = tagrunfixture.create(self.num_entries)

    def _create_tag_file(self):
        tagfilefixture = AutoFixture(TagFile)
        _ = tagfilefixture.create(self.num_entries)

    def _create_tag_version(self):
        tagversionfixture = AutoFixture(TagVersion)
        _ = tagversionfixture.create(self.num_entries)

    def handle(self, *args, **options):
        if type(options['entries']) == int and options['entries'] >= 0:
            self.num_entries = options['entries']
        else:
            self.num_entries = 10

        self._create_workflows()
        self._create_tags()
        self._create_versions()
        self._create_runs()
        self._create_files()
        self._create_run_files()
        self._create_tag_workflow()
        self._create_tag_run()
        self._create_tag_file()
        self._create_tag_version()
