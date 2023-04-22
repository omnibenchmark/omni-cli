# -*- coding: utf-8 -*-
from renku.core.models.provenance.annotation import Annotation
from renku.core.plugin import hookimpl

@hookimpl
def activity_annotations(activity):
    """``activity_annotations`` hook implementation."""
    print(">>> generating annotation for activity", activity)
    return [
        Annotation(
            id=Annotation.generate_id(),
            source="Dummy Annotation plugin",
            body={"@id": "dummyId"},
        )
    ]
