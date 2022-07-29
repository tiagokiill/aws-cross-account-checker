"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import os


class AwsOrg:
    def __init__(self):
        self.organization_client = boto3.client('organizations')
        self.response_list = self.organization_client.list_accounts()
        self.response_description = self.organization_client.describe_organization()


    def get_org_account_list_name_and_id(self):
        """
            Explanation: Method defined to get all accounts from AWS Organization
            :params: Params required 0 to get orgs details
            :return: Dict of AWS accounts from organization
        """
        dic_itens = dict()
        for a in self.response_list['Accounts']:
            dic_itens[a['Name']] = a['Id']

        return dic_itens


    def get_org_id(self):
        """
            Explanation: Method defined to get the ID of AWS Organization
            :params: N/A
            :return: String with AWS Organization ID
        """
        return self.response_description['Organization']['Id']


    def get_org_arn(self):
        """
            Explanation: Method defined to get the ARN of AWS Organization
            :params: N/A
            :return: String with AWS Organization ARN
        """
        return self.response_description['Organization']['Arn']


    def get_org_master_account_arn(self):
        """
            Explanation: Method defined to get the ACCOUNT ARN of AWS Organization
            :params: N/A
            :return: String with AWS MASTER ACCOUNT ARN of Organization
        """
        return self.response_description['Organization']['MasterAccountArn']


    def get_org_master_account_id(self):
        """
            Explanation: Method defined to get the MASTER ACCOUNT ID of AWS Organization
            :params: N/A
            :return: String with AWS MASTER ACCOUNT ID of Organization
        """
        return self.response_description['Organization']['MasterAccountId']


    def get_org_master_account_email(self):
        """
            Explanation: Method defined to get the Email of AWS Organization
            :params: N/A
            :return: String with AWS MASTER ACCOUNT EMAIL of Organization
        """
        return self.response_description['Organization']['MasterAccountEmail']

class AuthourizedAccount:
    def __init__(self):
        self.list_of_authorized_accounts = os.environ.get('AuthorizedAccounts')


    def check_authorized(self, account_id):
        """
            Explanation: Method defined to validate if the account was authorized
            :params: str account_id
            :return: bol True if account was authorized.
        """
        authorized_account = False
        for a in (self.list_of_authorized_accounts).split(','):
            if account_id == a:
                authorized_account = True

        return authorized_account