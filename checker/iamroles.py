"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3


class AwsIamLocal:
    def __init__(self):
        self.local_client = boto3.client('iam')

    def get_list_of_role_names_and_ids_from_local_account(self):
        """
            Explanation: Method defined to get all rule names from AWS remote account
            :params: str session
            :return: List of rules found in remote AWS account
        """
        local_list_of_roles = self.local_client.list_roles()
        list_of_local_role_name = dict()

        for a in local_list_of_roles['Roles']:
            for b in a['AssumeRolePolicyDocument']['Statement']:
                # Don't get AWS native rules services
                external_arn = b['Principal'].get('AWS', 'Access From AWS Native Service')
                if external_arn != 'Access From AWS Native Service':
                    for authorized_account_id in a['AssumeRolePolicyDocument']['Statement']:
                        list_of_local_role_name[a['RoleName']] = authorized_account_id['Principal']['AWS'][13:25]

        return list_of_local_role_name


class AwsIamRemote:
    def __init__(self, token_session):
        self.remote_client = boto3.client('iam',
                                          aws_access_key_id=token_session['Credentials']['AccessKeyId'],
                                          aws_secret_access_key=token_session['Credentials']['SecretAccessKey'],
                                          aws_session_token=token_session['Credentials']['SessionToken'])

    def get_list_of_role_names_and_ids_from_remote_account(self):
        """
            Explanation: Method defined to get all rule names from AWS remote account
            :params: str session
            :return: List of rules found in remote AWS account
        """
        remote_list_of_roles = self.remote_client.list_roles()
        list_of_remote_role_name = dict()

        for a in remote_list_of_roles['Roles']:
            for b in a['AssumeRolePolicyDocument']['Statement']:
                # Don't get AWS native rules services
                external_arn = b['Principal'].get('AWS', 'Access From AWS Native Service')
                if external_arn != 'Access From AWS Native Service':
                    for authorized_account_id in a['AssumeRolePolicyDocument']['Statement']:
                        list_of_remote_role_name[a['RoleName']] = authorized_account_id['Principal']['AWS'][13:25]

        return list_of_remote_role_name
