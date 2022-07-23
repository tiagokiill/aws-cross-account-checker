"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import botocore
import boto3
import os


class Session:

    def __init__(self, remote_account_name, remote_account_id):
        self.remote_account_name = remote_account_name
        self.remote_account_id = remote_account_id
        self.remote_sts_role_name = os.environ.get('OrganizationAccountAccessRole')


    def get_remote_session_token(self):
        """
            Explanation: Method defined to get credentials to access other accounts
            :params: str Account_name
            :return: dict with new session data
        """
        self.rolearn = '{}{}{}{}'.format('arn:aws:iam::', self.remote_account_id, ':role/', self.remote_sts_role_name)
        client = boto3.client('sts')
        try:
            self.response = client.assume_role(
                RoleArn=self.rolearn,
                RoleSessionName=self.remote_account_name,
                DurationSeconds=3600
            )

            return self.response

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                return 'The role {} is not authorized to assume role at account {}'.format(self.remote_sts_role_name, self.remote_account_name)




