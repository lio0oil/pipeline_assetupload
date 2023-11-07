#!/usr/bin/env python3
import os
import aws_cdk as cdk

from pipeline.pipeline_stack import PipelineStack


app = cdk.App()
PipelineStack(
    app,
    "PipelineStack",
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")),
)

app.synth()
