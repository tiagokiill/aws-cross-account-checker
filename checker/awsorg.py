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


class AuthorizedAccounts:
    def __init__(self):
        self.list_of_accounts_from_org = AwsOrg().get_org_account_list_name_and_id()
        self.list_of_accounts_from_user = os.environ.get('AuthorizedAccounts')

    def authorized_account_list(self):
        """
            Explanation: Method to build a list of authorized accounts
            :params: N/A
            :return: list with authorized account id.
        """
        list_of_accounts = list()
        for org_account_name, org_account_id in self.list_of_accounts_from_org.items():
            list_of_accounts.append(org_account_id)

        for user_authorized_accounts in self.list_of_accounts_from_user.split(','):
            list_of_accounts.append(user_authorized_accounts)

        return list_of_accounts

    def check_authorized(self, account_id):
        """
            Explanation: Method defined to validate if the account was authorized
            :params: str account_id
            :return: bol True if account is authorized.
        """
        if account_id in AuthorizedAccounts().authorized_account_list():
            return True
        else:
            return False
