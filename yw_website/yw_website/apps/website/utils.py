from django.db.models import Q
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

from .program_blocks import *

from .models import *

def search_and_create_query_set(q):
    """
    This function takes a user search as a parameter and then uses the
    Django haystack API to create a Django QuerySet containing all related
    Workflows
    """
    aq = AutoQuery(q)
    sqs = (
        SearchQuerySet()
        .filter(content=aq)
        .models(
            Workflow,
            Version,
            Tag,
            Script,
            ProgramBlock,
            Data,
            Port,
            UriVariable,
            Resource,
            UriVariableValue,
        )
    )

    workflows = set()

    for result in sqs:
        if result.model_name == "workflow":
            workflows.add(result.object.pk)
        elif result.model_name == "version":
            workflows.add(result.object.workflow.pk)
        elif result.model_name == "run":
            version = Version.objects.get(pk=result.version_id)
            workflows.add(version.workflow_id)
        elif result.model_name == "tag":
            tag = Tag.objects.get(pk=result.pk)
            workflow_tags = TagWorkflow.objects.filter(tag=tag)
            for tag_workflow in workflow_tags:
                if tag_workflow.workflow.pk not in workflows:
                    workflows.add(tag_workflow.workflow.pk)
        elif result.model_name == "script":
            script = Script.objects.get(pk=result.pk)
            workflows.add(script.version.workflow.pk)         
        elif (
            result.model_name == "programblock"
            or result.model_name == "data"
            or result.model_name == "port"
            or result.model_name == "urivariable"
            or result.model_name == "resource"
            or result.model_name == "urivariablevalue"
        ):
            run = Run.objects.get(pk=result.object.run.pk)
            workflows.add(run.version.workflow.pk)

    queries = [Q(pk=key) for key in workflows]
    if len(queries) > 0:
        query = queries.pop()
        for item in queries:
            query |= item
        return Workflow.objects.filter(query).exclude(version__isnull=True)
    else:
        return Workflow.objects.none()

def get_block_data(run_id):
    '''
    This function sets up the block structure so that from a parent program
    block you may drill down into a child of that program block
    '''
    program_blocks = ProgramBlock.objects.filter(run=run_id)
    data = Data.objects.filter(run=run_id)
    # print(data)
    # data_vals = []

    # grab parent block
    parents = get_direct_descendants(None, program_blocks)
    print(parents)
    # for data in parent_data:
    #     parent.data_objs.append(data)
    return parents

def get_direct_descendants(program_block_id, program_blocks):
    descendants = []
    for child in program_blocks.filter(in_program_block=program_block_id):
        new_child = ProgramBlock()
        new_child.name = child.name
        new_child.programblock_id = child.programblock_id
        new_child.id = child.id
        new_child.direct_descendants = get_direct_descendants(new_child.programblock_id, program_blocks)
        descendants.append(new_child)
    return descendants
