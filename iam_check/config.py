import logging
import yaml
import sys

# logging configuration
LOGGER = logging.getLogger("iam-policy-validator-for-terraform")

# AWS Account ID to use when unknown
awsAccount = "123456789012"

# IAM policy resources
iamPolicyAttributes = {}

# Generate fake ARN
# default substitube is {<key>?<default>}
arnServiceMap = {}

validatePolicyResourceType = {}

json_config = {
    "arnServiceMap": {
        "aws_iam_policy": "name?fakename",
        "aws_iam_role": "name?fakename",
        "aws_api_gateway_rest_api_policy": "rest_api_id?fakeRestApiId",
        "aws_backup_vault_policy": "backup_vault_name?fakeBackupVaultName",
        "aws_cloudwatch_event_bus_policy": "event_bus_name?fakeEventBusName",
        "aws_cloudwatch_log_destination_policy": "destination_name?fakeDestinationName",
        "aws_codeartifact_domain_permissions_policy": "domain?fakeDomain",
        "aws_codeartifact_repository_permissions_policy": "repository?fakeRepository",
        "aws_codebuild_resource_policy": "fakename",
        "aws_ecr_registry_policy": "fakename",
        "aws_ecr_repository_policy": "repository?fakeRepositoryName",
        "aws_ecrpublic_repository_policy": "repository_name?fakeRepositoryName",
        "aws_efs_file_system_policy": "file_system_id?fakeFileSystemId",
        "aws_elasticsearch_domain": "domain_name?fakeDomainName",
        "aws_elasticsearch_domain_policy": "domain_name?fakeDomainName",
        "aws_glacier_vault": "name?fakename",
        "aws_glacier_vault_lock": "vault_name?fakeVaultName",
        "aws_glue_resource_policy": "fakeName",
        "aws_iot_policy": "name?fakename",
        "aws_kms_external_key": "fakeName",
        "aws_kms_key": "fakeName",
        "aws_kms_replica_external_key": "fakeName",
        "aws_kms_replica_key": "fakeName",
        "aws_media_store_container_policy": "container_name?fakeContainerName",
        "aws_networkfirewall_resource_policy": "resource_arn?fakeResourceArn",
        "aws_organizations_policy": "name?fakename",
        "aws_s3_access_point": "name?fakename",
        "aws_s3_bucket": "bucket?fakeBucket",
        "aws_s3_bucket_policy": "bucket?fakeBucket",
        "aws_s3control_access_point_policy": "access_point_arn?fakeAccessPointArn",
        "aws_s3control_bucket_policy": "bucket?fakeBucket",
        "aws_s3control_multi_region_access_point_policy": "details.name?fakename",
        "aws_s3control_object_lambda_access_point_policy": "name?fakename",
        "aws_ses_identity_policy": "name?fakename",
        "aws_sns_topic": "name?fakename",
        "aws_sns_topic_policy": "arn?fakename",
        "aws_sqs_queue": "name?fakename",
        "aws_sqs_queue_policy": "fakeQueueUrl",
        "aws_ssoadmin_permission_set_inline_policy": "instance_arn?fakeSSOInstanceArn",
        "aws_sagemaker_model_package_group_policy": "model_package_group_name?fakeModelPackageGroupName",
        "aws_secretsmanager_secret": "name?fakename",
        "aws_secretsmanager_secret_policy": "secret_arn?fakeSecretArn",
        "aws_transfer_access": "server_id?fakeServerId",
        "aws_transfer_user": "user_name?fakeUserName",
        "aws_vpc_endpoint": "fakeName",
    },
    "iamPolicyAttributes": {
        "aws_iam_group_policy": "policy",
        "aws_iam_policy": "policy",
        "aws_iam_role": ["assume_role_policy", "inline_policy.policy"],
        "aws_iam_role_policy": "policy",
        "aws_iam_user_policy": "policy",
        "aws_api_gateway_rest_api": "policy",
        "aws_api_gateway_rest_api_policy": "policy",
        "aws_backup_vault_policy": "policy",
        "aws_cloudwatch_event_bus_policy": "policy",
        "aws_cloudwatch_log_destination_policy": "access_policy",
        "aws_cloudwatch_log_resource_policy": "policy",
        "aws_codeartifact_domain_permissions_policy": "policy_document",
        "aws_codeartifact_repository_permissions_policy": "policy_document",
        "aws_codebuild_resource_policy": "policy",
        "aws_ecr_registry_policy": "policy",
        "aws_ecr_repository_policy": "policy",
        "aws_ecrpublic_repository_policy": "policy",
        "aws_efs_file_system_policy": "policy",
        "aws_elasticsearch_domain": "access_policies",
        "aws_elasticsearch_domain_policy": "access_policies",
        "aws_glacier_vault": "access_policy",
        "aws_glacier_vault_lock": "access_policy",
        "aws_glue_resource_policy": "policy",
        "aws_iot_policy": "policy",
        "aws_kms_external_key": "policy",
        "aws_kms_key": "policy",
        "aws_kms_replica_external_key": "policy",
        "aws_kms_replica_key": "policy",
        "aws_media_store_container_policy": "policy",
        "aws_networkfirewall_resource_policy": "policy",
        "aws_organizations_policy": "content",
        "aws_s3_access_point": "policy",
        "aws_s3_bucket": "policy",
        "aws_s3_bucket_policy": "policy",
        "aws_s3control_access_point_policy": "policy",
        "aws_s3control_bucket_policy": "policy",
        "aws_s3control_multi_region_access_point_policy": "details.policy",
        "aws_s3control_object_lambda_access_point_policy": "policy",
        "aws_ses_identity_policy": "policy",
        "aws_sns_topic": "policy",
        "aws_sns_topic_policy": "policy",
        "aws_sqs_queue": "policy",
        "aws_sqs_queue_policy": "policy",
        "aws_ssoadmin_permission_set_inline_policy": "inline_policy",
        "aws_sagemaker_model_package_group_policy": "resource_policy",
        "aws_secretsmanager_secret": "policy",
        "aws_secretsmanager_secret_policy": "policy",
        "aws_transfer_access": "policy",
        "aws_transfer_user": "policy",
        "aws_vpc_endpoint": "policy",
    },
    "validatePolicyResourceType": {
        "aws_s3_bucket": "AWS::S3::Bucket",
        "aws_s3_bucket_policy": "AWS::S3::Bucket",
        "aws_s3control_access_point_policy": "AWS::S3::AccessPoint",
        "aws_s3control_multi_region_access_point_policy": "AWS::S3::MultiRegionAccessPoint",
        "aws_s3control_object_lambda_access_point_policy": "AWS::S3ObjectLambda::AccessPoint",
    },
}


def configure_logging(enable_logging):
    console_handler = logging.StreamHandler(sys.stdout)
    LOGGER.setLevel(logging.INFO)
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(log_formatter)
    LOGGER.propagate = False
    LOGGER.addHandler(console_handler)
    if not enable_logging:
        LOGGER.disabled = True


def loadConfigYaml(file=None):
    global arnServiceMap
    global iamPolicyAttributes
    global validatePolicyResourceType

    if file is None:
        arnServiceMap = json_config["arnServiceMap"]
        iamPolicyAttributes = json_config["iamPolicyAttributes"]
        validatePolicyResourceType = json_config["validatePolicyResourceType"]
        return

    with open(file, "r") as fh:
        data = yaml.safe_load(fh)

    arnServiceMap = data.get("arnServiceMap", arnServiceMap)
    if "arnServiceMap" in data:
        arnServiceMap = data["arnServiceMap"]

    if "iamPolicyAttributes" in data:
        iamPolicyAttributes = data["iamPolicyAttributes"]

    if "validatePolicyResourceType" in data:
        validatePolicyResourceType = data["validatePolicyResourceType"]
