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
