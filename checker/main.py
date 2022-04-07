"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import json


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
                #print(
                #    f'**ALERT** External account ID: {external_arn[13:25]}, '
                #    f'Effect of role: {effect}, '
                #    f'Action of role: {external_action}')

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


def send_msg(accounts_from_roles):
    """
        Explanation: Method defined to send msg with report
        :params: list
        :return: Date of msg sent
    """

    client = boto3.client('sns')
    msg = str(accounts_from_roles)
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:325868435144:aws-cross-account-checker',
        Message=str(accounts_from_roles),
        Subject=' ** - REPORT - ** AWS Cross Account Checker'
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('msg sent at {}'.format(response['ResponseMetadata']['HTTPHeaders']['date']))


def lambda_handler(event, context):

    accounts_from_roles = get_roles()
    send_msg(accounts_from_roles)
    return {
        'statusCode': 200,
        'body': json.dumps('')
    }


