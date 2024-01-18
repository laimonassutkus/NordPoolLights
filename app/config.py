import os

from util import ParameterStore


class Config:
    def __init__(self):
        # Retrieve credentials from AWS parameter store. These parameters are defined in Terraform
        # infrastructure script. By default, these values are empty and must be set manually
        # within AWS console for security reasons.

        self.username = ParameterStore.get_parameter('NordPoolLightsMiAccountUsername')
        if self.username is None:
            raise ValueError('Username not set. Go to AWS Systems Manager Parameter Store and set the value manually.')

        self.password = ParameterStore.get_parameter('NordPoolLightsMiAccountPassword')
        if self.password is None:
            raise ValueError('Password not set. Go to AWS Systems Manager Parameter Store and set the value manually.')

        # Retrieve configuration from AWS Lambda environment variables.

        self.mi_device_id = os.environ.get('MI_DEVICE_ID')
        if self.mi_device_id is None:
            raise ValueError('Mi device id not set. Set it in Lambda function environment variables.')

        self.vat_percentage = os.environ.get('VAT_PERCENTAGE')
        if self.vat_percentage is None:
            raise ValueError('Vat percentage not set. Set it in Lambda function environment variables.')
        self.vat_percentage = int(self.vat_percentage)

        self.country = os.environ.get('COUNTRY')
        if self.country is None:
            raise ValueError('Country not set. Set it in Lambda function environment variables.')

        self.price_threshold = os.environ.get('PRICE_THRESHOLD')
        if self.price_threshold is None:
            raise ValueError('Price threshold not set. Set it in Lambda function environment variables.')
        self.price_threshold = int(self.price_threshold)
