"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import botocore


class AwsIamLocal:
    def __init__(self):
        self.local_client = boto3.client('iam')

    def get_list_of_role_names_and_ids_from_local_account(self):
        """
            Explanation: Method defined to get all rule names from AWS remote account
            :params: N/A
            :return: List of rules found in local AWS account
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

    def remove_policies_from_local_account(self, role_name):
        """
            Explanation: Method defined to detach policies from roles in local account
            :params: Role name
            :return: Return True if had success
        """
        try:
            list_of_policies = self.local_client.list_attached_role_policies(RoleName=role_name)
            if not list_of_policies['AttachedPolicies']:
                print('There aren´t policy attached in this role')
                return True
            else:
                for policy in list_of_policies['AttachedPolicies']:
                    response = self.local_client.detach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy['PolicyArn']
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print('The Policy "{}" was removed from role "{}" in {} '.format(policy['PolicyName'],
                                                                                         role_name,
                                                                                         'Organization Account'))
                return True

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print('The role is not authorized to execute this action')
            elif e.response['Error']['Code'] == 'NoSuchEntity':
                print('The role "{}" not found'.format(role_name))
            return False


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

    def remove_policies_from_remote_account(self, role_name):
        """
            Explanation: Method defined to detach policies from roles in remote account
            :params: Role Name
            :return: Return True if had success
        """
        try:
            list_of_policies = self.remote_client.list_attached_role_policies(RoleName=role_name)
            if not list_of_policies['AttachedPolicies']:
                print('There aren´t policy attached in this role')
                return True
            else:
                for policy in list_of_policies['AttachedPolicies']:
                    response = self.remote_client.detach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy['PolicyArn']
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print('The Policy "{}" was removed from role "{}" in {} '.format(policy['PolicyName'],
                                                                                         role_name,
                                                                                         'Organization Account'))
                return True

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print('The role is not authorized to execute this action')
            elif e.response['Error']['Code'] == 'NoSuchEntity':
                print('The role "{}" not found'.format(role_name))
            return False
