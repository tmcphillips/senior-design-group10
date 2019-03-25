from django.db.models import Q
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

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
        elif result.model_name == "tag" or result.model_name == "script":
            tag = Tag.objects.get(pk=result.pk)
            workflow_tags = TagWorkflow.objects.filter(tag=tag)
            for tag_workflow in workflow_tags:
                if tag_workflow.workflow.pk not in workflows:
                    workflows.add(tag_workflow.workflow.pk)
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
