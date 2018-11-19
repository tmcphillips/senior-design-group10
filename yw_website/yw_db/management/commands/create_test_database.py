from autofixture import AutoFixture
from django.core.management.base import BaseCommand
from yw_db.models import Workflow, Version, Tag, Run, File, RunFile, TagWorkflow, TagVersion, TagRun, TagFile
import uuid
TEMP_NUM_ENTRIES = 100

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        tag_fixture = AutoFixture(Tag)
        _ = tag_fixture.create(TEMP_NUM_ENTRIES)

    def _create_workflows(self):
        workflow_fixture = AutoFixture(Workflow, field_values={'user':None} )
        _ = workflow_fixture.create(TEMP_NUM_ENTRIES)

    def _create_versions(self):
        version_fixture = AutoFixture(Version)
        _ = version_fixture.create(TEMP_NUM_ENTRIES)

    def _create_runs(self):
        run_fixture = AutoFixture(Run)
        _ = run_fixture.create(TEMP_NUM_ENTRIES)

    def _create_files(self):
        for i in range(0, TEMP_NUM_ENTRIES):
            files_fixture = AutoFixture(File, field_values={'file_checksum':str(uuid.uuid4()), 'input_data':None})
            _ = files_fixture.create_one()

    def _create_run_files(self):
        runfile_fixture = AutoFixture(RunFile)
        _ = runfile_fixture.create(TEMP_NUM_ENTRIES)

    def _create_tag_workflow(self):
        tagworkflow_fixture = AutoFixture(TagWorkflow)
        _ = tagworkflow_fixture.create(TEMP_NUM_ENTRIES)

    def _create_tag_run(self):
        tagrunfixture = AutoFixture(TagRun)
        _ = tagrunfixture.create(TEMP_NUM_ENTRIES) 

    def _create_tag_file(self):
        tagfilefixture = AutoFixture(TagFile)
        _ = tagfilefixture.create(TEMP_NUM_ENTRIES)

    def _create_tag_version(self):
        tagversionfixture = AutoFixture(TagVersion)
        _ = tagversionfixture.create(TEMP_NUM_ENTRIES) 

    def handle(self, *args, **options):
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
