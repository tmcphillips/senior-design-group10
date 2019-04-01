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
        SearchQuerySet().filter(content=aq).models(Workflow, Version, Tag, Script, Run)
    )
    workflows = set()

    for result in sqs:
        if result.model_name == "workflow":
            workflows.add(result.object.pk)
        elif result.model_name == "version":
            workflows.add(result.workflow_id)
        elif result.model_name == "run":
            version = Version.objects.get(pk=result.version_id)
            workflows.add(version.workflow_id)
        elif result.model_name == "tag":
            pass
            # TODO: Add support for WorkflowTag in rest API so workflows have a relation to tags
            # tag_workflows = Workflow.objects.all().select_related("tag").filter(pk=results.pk)
            # for item in tag_workflows:
            #     workflows.add(item.pk)
        elif result.model_name == "script":
            version = Version.objects().get(pk=result.version_id)
            workflows.add(version.workflow_id)
        # TODO: Add searching to files
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
