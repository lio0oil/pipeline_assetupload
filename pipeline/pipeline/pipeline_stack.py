import os
from aws_cdk import (
    # Duration,
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_iam as iam,
)
from constructs import Construct


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = codepipeline.Pipeline(
            self,
            id="sample_pipeline",
            pipeline_name="sample_pipeline",
        )

        source_output = codepipeline.Artifact("source_output")

        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="sanple_action",
            repository=codecommit.Repository.from_repository_arn(
                self,
                "codecommit",
                os.getenv("CODECOMMIT_ARN"),  # type: ignore
            ),
            trigger=codepipeline_actions.CodeCommitTrigger.NONE,
            branch="master",
            output=source_output,
        )
        # Add source stage to my pipeline.
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        build_spec = {
            "version": 0.2,
            "phases": {
                "install": {
                    "runtime-versions": {
                        "python": "3.9",
                    },
                    "commands": [
                        "npm install -g aws-cdk",
                        "npm install -g cdk-assets",
                        "pip install -r $CODEBUILD_SRC_DIR/requirements.txt",
                    ],
                },
                "pre_build": {
                    "commands": [
                        "cdk synth",
                    ]
                },
                "build": {
                    "commands": [
                        "cdk-assets --path $CODEBUILD_SRC_DIR/cdk.out/CicdtestStack.assets.json publish --verbose ",
                    ]
                },
            },
            "artifacts": {"files": []},
        }

        project = codebuild.PipelineProject(
            self,
            id="sample_build_project",
            project_name="sample_build_project",
            environment=codebuild.BuildEnvironment(
                privileged=False,
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.SMALL,
            ),
            build_spec=codebuild.BuildSpec.from_object(build_spec),
        )

        assetsPublishingPermissions = iam.PolicyStatement(
            sid="extraPermissionsRequiredForPublishingAssets",
            effect=iam.Effect.ALLOW,
            actions=["sts:AssumeRole"],
            resources=[
                "arn:aws:iam::{0}:role/cdk-{1}-file-publishing-role-{0}-{2}".format(
                    self.account, self.synthesizer.bootstrap_qualifier, self.region
                )
            ],
        )

        project.add_to_role_policy(assetsPublishingPermissions)

        build_output = codepipeline.Artifact("build_output")
        actions = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=project,  # type: ignore
            input=source_output,
            outputs=[build_output],
            type=codepipeline_actions.CodeBuildActionType.TEST,
        )

        pipeline.add_stage(
            stage_name="Build",
            actions=[actions],
        )
