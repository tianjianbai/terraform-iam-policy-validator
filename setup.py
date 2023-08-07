import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="tf-policy-validator",
    packages=[
        "iam_check",
        "iam_check.lib",
        "iam_check.tools",
        "iam_check.config",
    ],
    version="0.0.3",
    author="Policy Validator Maintainers <terraform-policy-validator@amazon.com>",
    author_email="terraform-policy-validator@amazon.com",
    description="A command line tool that validates AWS IAM policies in a Terraform template against AWS IAM best practices",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/awslabs/terraform-iam-policy-validator",
    keywords="amazon aws aws-samples eks kubernetes upgrade iam_check",
    license="MIT-0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
    ],
    entry_points={
        "console_scripts": "tf-policy-validator=iam_check.iam_check:main"
    },
    python_requires=">=3.7",
    install_requires=["boto3>=1.20", "pyYAML>=5.3"],
)
