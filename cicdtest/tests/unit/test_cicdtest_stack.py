import aws_cdk as core
import aws_cdk.assertions as assertions

from cicdtest.cicdtest_stack import CicdtestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cicdtest/cicdtest_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CicdtestStack(app, "cicdtest")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
