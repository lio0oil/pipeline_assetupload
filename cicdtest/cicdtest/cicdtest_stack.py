from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
)
from constructs import Construct


class CicdtestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_.Function(
            self,
            "cicd_lambda",
            code=lambda_.AssetCode.from_asset("./lambda"),
            handler="lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
        )
