from django.db.models import Q
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

from .program_blocks import ProgramBlocks
from .ports import Ports, PortResource

from .models import *


def search_and_create_query_set(q, tag=False, resource=False):
    """
    This function takes a user search as a parameter and then uses the
    Django haystack API to create a Django QuerySet containing all related
    Workflows
    """
    aq = AutoQuery(q)
    workflows = set()
    if tag:
        sqs = SearchQuerySet().filter(content=aq).models(Tag)
    elif resource:
        sqs = SearchQuerySet().filter(content=aq).models(Resource)
    else:
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
    """
    This function sets up the block structure so that from a parent program
    block you may drill down into a child of that program block
    """
    program_blocks = ProgramBlock.objects.filter(run=run_id)
    data = Data.objects.filter(run=run_id)
    parents = get_direct_descendants(None, program_blocks)
    return parents


def get_direct_descendants(program_block_id, program_blocks):
    descendants = []
    for child in program_blocks.filter(in_program_block_id=program_block_id):
        new_child = ProgramBlocks()
        new_child.name = child.name
        new_child.program_block_id = child.programblock_id
        new_child.id = child.id
        new_child.direct_descendants = get_direct_descendants(
            new_child.id, program_blocks
        )
        get_ports(new_child)
        descendants.append(new_child)
    return descendants


def get_ports(program_block):
    for port in Port.objects.filter(on_program_block_id=program_block.id):
        new_port = Ports()
        new_port.name = port.name
        new_port.id = port.id
        new_port.is_inport = port.is_inport
        new_port.is_outport = port.is_outport
        new_port.data_id = port.data.id
        new_port.on_program_block_id = port.on_program_block_id
        new_port.run_id = port.run.id
        new_port.resources = get_port_resources(new_port.data_id)

        if new_port.is_inport and not new_port.is_outport:
            program_block.in_ports.append(new_port)
        elif new_port.is_outport and not new_port.is_inport:
            program_block.out_ports.append(new_port)
        else:
            # both in port and out port
            # TODO: error handle gracefully if we have a port that is both in and out
            pass


def get_port_resources(data_id):
    resources = []
    for resource in Resource.objects.filter(data=data_id):
        port_resource = PortResource()
        port_resource.id = resource.id
        port_resource.data = resource.data.id
        port_resource.run_id = resource.run.id
        port_resource.checksum = resource.checksum
        port_resource.last_modified = resource.last_modified
        port_resource.name = resource.name
        port_resource.resource_id = resource.resource_id
        port_resource.size = resource.size
        port_resource.uri = resource.uri
        resources.append(port_resource)
    return resources

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    truncated = int(n * multiplier) / multiplier
    return int(truncated) if truncated.is_integer() else truncated
