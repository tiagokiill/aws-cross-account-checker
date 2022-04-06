"""
    __autor__ = "Tiago kiill"
    __email__ = "tiagokiill@gmail.com"
    __credits__ = "Tiago Kiill"
"""
import boto3

def get_roles():
    """
        Explanation: Method defined to get all rules from AWS
        :params: No params required
        :return: list os AWS accounts from rules
    """

    client = boto3.client('iam')
    response = client.list_roles()
    list = []
    for a in response['Roles']:
        path = a['Path']
        role_name = a['RoleName']
        role_id = a['RoleId']
        arn = a['Arn']

        for b in a['AssumeRolePolicyDocument']['Statement']:
            effect = b['Effect']
            external_arn = b['Principal'].get('AWS', 'Access From AWS Native Service')
            external_action = b['Action']

            if external_arn != 'Access From AWS Native Service':
                list.append(external_arn[13:25])

    print(list)
    return list


def get_orgs():
    """
        Explanation: Method defined to get all accounts from AWS Organization
        :params: No params required
        :return: list of AWS accounts from organization
    """

    client = boto3.client('organizations')
    response = client.list_accounts()
    list = []
    for a in response['Accounts']:
        list.append(a['Id'])

    return list

def send_msg():
    """
        Explanation: Method defined to send msg with report
        :params: list
        :return: list of AWS accounts from organization
    """

    client = boto3.client('sns')
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:325868435144:aws-cross-account-checker',
        Message='teste',
        Subject='teste'
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('msg sent at {}'.format(response['ResponseMetadata']['HTTPHeaders']['date']))
