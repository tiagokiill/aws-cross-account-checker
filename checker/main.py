"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import json


def get_roles(session):
    """
        Explanation: Method defined to get all rules from AWS
        :params: str session
        :return: dict of os AWS accounts from rules found
    """

    client = boto3.client('iam',
                        aws_access_key_id=session['Credentials']['AccessKeyId'],
                        aws_secret_access_key=session['Credentials']['SecretAccessKey'],
                        aws_session_token=session['Credentials']['SessionToken'])

    response = client.list_roles()
    list_of_roles = []

    for a in response['Roles']:

        for b in a['AssumeRolePolicyDocument']['Statement']:
            effect = b['Effect']
            external_arn = b['Principal'].get('AWS', 'Access From AWS Native Service')
            #external_action = b['Action']

            if external_arn != 'Access From AWS Native Service':
                list_of_roles.append(a)

#                dic_item[a['RoleId']] = a['RoleName']
#                dic_item['external_account_id'] = external_arn[13:25]
#                dic_item['role_arn'] = a['Arn']



    return list_of_roles


def get_orgs(x=0):
    """
        Explanation: Method defined to get all accounts from AWS Organization
        :params: Params required 0 to get orgs details
        :return: Dict of AWS accounts from organization
    """

    client = boto3.client('organizations')

    if x == 0:
        response_desc = client.describe_organization()
        return response_desc
    else:
        response = client.list_accounts()
        dic_item = dict()
        for a in response['Accounts']:
            dic_item[a['Name']] = a['Id']

        return dic_item


def send_msg(accounts_from_roles):
    """
        Explanation: Method defined to send msg with report
        :params: list
        :return: Date of the message sent
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


def get_session(account_name, account_id):
    """
        Explanation: Method defined to get credentials to access other accounts
        :params: str Account_name
        :return: dict with new session data
    """
    rolearn = '{}{}{}'.format('arn:aws:iam::', account_id, ':role/OrganizationAccountAccessRole')
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=rolearn,
        RoleSessionName=account_name,
        DurationSeconds=3600)

    return response


def lambda_handler(event, context):

    list_of_roles_from_accounts = list()
    report_error = list()
    org_details = get_orgs(0)
    orgs_from_accounts = get_orgs(1)

    for account_name, account_id in orgs_from_accounts.items():
        try:
            session = get_session(account_name, account_id)
            for roles_from_accounts in get_roles(session):
                for account in roles_from_accounts['AssumeRolePolicyDocument']['Statement']:
                    if org_details['Organization']['MasterAccountId'] != account['Principal']['AWS'][13:25]:
                        if account_id not in account['Principal']['AWS'][13:25]:
                            list_of_roles_from_accounts.append(roles_from_accounts)
                            #print(account['Principal']['AWS'][13:25])

        except:
            #report_error.append(('Error: Without permission to assume role at AWS Account: {} Id : {}'.format(account_name,account_id)))
            error = dict()
            error['access_error_account_name'] = account_name
            error['access_error_account_id'] = account_id
            report_error.append(error)

    #todo building msg
    for a in list_of_roles_from_accounts:
        print(a)
    #send_msg(report)


    return {
        'statusCode': 200,
        'body': json.dumps('')
    }

lambda_handler('a','b')
