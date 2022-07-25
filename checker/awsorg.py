"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3


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


#lista = AwsOrg()
#print(lista.get_org_account_list_name_and_id().items())




#{'Organization': {'Id': 'o-8ht5o37fth', 'Arn': 'arn:aws:organizations::325868435144:organization/o-8ht5o37fth',
# 'FeatureSet': 'ALL', 'MasterAccountArn': 'arn:aws:organizations::325868435144:account/o-8ht5o37fth/325868435144',
# 'MasterAccountId': '325868435144', 'MasterAccountEmail': 'tdk9831@nyu.edu', 'AvailablePolicyTypes':
# [{'Type': 'SERVICE_CONTROL_POLICY', 'Status': 'ENABLED'}]}, 'ResponseMetadata': {'RequestId': '821166d4-13ac-4161-ba37-4919179092f9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '821166d4-13ac-4161-ba37-4919179092f9', 'content-type': 'application/x-amz-json-1.1', 'content-length': '368', 'date': 'Sun, 24 Jul 2022 14:28:00 GMT'}, 'RetryAttempts': 0}}

