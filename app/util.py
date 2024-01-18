from typing import Optional

import boto3
from botocore.exceptions import ClientError


class ParameterStore:
    SSM = boto3.client('ssm')

    @staticmethod
    def get_parameter(name: str) -> Optional[str]:
        try:
            response = ParameterStore.SSM.get_parameter(Name=name, WithDecryption=True)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ParameterNotFound':
                raise ValueError(
                    f'The specified parameter ({name}) was not found. '
                    f'Please ensure that it is set in AWS Systems Manager Parameter Store.'
                )
            raise ValueError(f'Unknown boto3 error occurred. Full message:\n{repr(ex)}.')
        except Exception as ex:
            raise ValueError(f'Unknown general error occurred. Full message:\n{repr(ex)}.')

        try:
            parameter = response['Parameter']['Value']
        except KeyError as ex:
            raise KeyError(
                f'Could not parse parameter value from AWS parameter store API response. '
                f'Accessing ["Parameter"]["Value"] resulted in KeyError:\n{repr(ex)}.'
            )

        # This class treats parameters with value "-" as empty (not set) parameters
        # and instead of returning "-", will return None indicating that the parameter exists,
        # however it's value was not set.
        if parameter == '-':
            return None

        return parameter
