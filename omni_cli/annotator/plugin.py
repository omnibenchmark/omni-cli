# -*- coding: utf-8 -*-
import logging

import subprocess

from renku.core.models.provenance.annotation import Annotation
from renku.core.plugin import hookimpl

@hookimpl
def activity_annotations(activity):
    """``activity_annotations`` hook implementation."""
    print("Generating annotations for activity:", activity)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

    # TODO check configuration and generate only the annotations that are enabled for this project

    return [
        Annotation(
            id=Annotation.generate_id(),
            source="omni-cli",
            body={
                "@type": "http://usefulinc.com/ns/doap#revision",
                "@purpose": "reference",
                "@value": commit,
            }
        )
    ]
