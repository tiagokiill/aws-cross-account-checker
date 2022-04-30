"""
    __autor__ = "Tiago kiill and Teogenes Panella"
    __email__ = "tiagokiill@gmail.com and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import json
import os


def get_roles(session, org_account):
    """
        Explanation: Method defined to get all rules from AWS
        :params: str session
        :params: bol or_account
        :return: dict of os AWS accounts from rules found
    """
    if org_account is False:
        client = boto3.client('iam',
                            aws_access_key_id=session['Credentials']['AccessKeyId'],
                            aws_secret_access_key=session['Credentials']['SecretAccessKey'],
                            aws_session_token=session['Credentials']['SessionToken'])
    else:
        client = boto3.client('iam')

    response = client.list_roles()
    list_of_roles = []

    for a in response['Roles']:

        for b in a['AssumeRolePolicyDocument']['Statement']:
            external_arn = b['Principal'].get('AWS', 'Access From AWS Native Service')
            if external_arn != 'Access From AWS Native Service':
                list_of_roles.append(a)

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
    topic = os.environ.get('TopicArn')
    client = boto3.client('sns')
    msg = str(accounts_from_roles)
    response = client.publish(
        TopicArn=topic,
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
    env_role_name = os.environ.get('OrganizationAccountAccessRole')
    rolearn = '{}{}{}{}'.format('arn:aws:iam::', account_id, ':role/', env_role_name)
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=rolearn,
        RoleSessionName=account_name,
        DurationSeconds=3600)

    return response


def check_authorized(account_id):
    """
        Explanation: Method defined to validate if the account was authorized
        :params: str account_id
        :return: bol True if account was authorized.
    """

    authorized_account = False
    for a in (os.environ.get('AuthorizedAccounts')).split(','):
        if account_id == a:
            authorized_account = True

    return authorized_account


def remove_policies(rolename, org_account, session):
    if org_account is False:
        client = boto3.client('iam',
                            aws_access_key_id=session['Credentials']['AccessKeyId'],
                            aws_secret_access_key=session['Credentials']['SecretAccessKey'],
                            aws_session_token=session['Credentials']['SessionToken'])
    else:
        client = boto3.client('iam')

    response = client.list_attached_role_policies(
        RoleName=rolename
    )

    for a in response['AttachedPolicies']:
        response = client.detach_role_policy(
            RoleName=rolename,
            PolicyArn=a['PolicyArn']
        )


def del_role(rolename, org_account, session):

    remove_policies(rolename, org_account, session)

    if org_account is False:
        client = boto3.client('iam',
                            aws_access_key_id=session['Credentials']['AccessKeyId'],
                            aws_secret_access_key=session['Credentials']['SecretAccessKey'],
                            aws_session_token=session['Credentials']['SessionToken'])
    else:
        client = boto3.client('iam')

    response = client.delete_role(
        RoleName=rolename,
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True

    else:
        return False

def lambda_handler(event, context):
    print('Params...')
    print('Using role name {} to STS'.format(os.environ.get('OrganizationAccountAccessRole')))
    print('Authorized accounts: {}'.format(os.environ.get('AuthorizedAccounts')))
    print('Sending message on Topic: {}'.format(os.environ.get('TopicArn')))
    if os.environ.get('Action').lower() == 'delete':
        print('Auto Delete "on"')
    else:
        print('Auto Delete "off"')
    print('---------------------------------------------------------')
    print('Starting JOB...')

    list_of_roles_from_accounts = list()
    list_of_deleted_roles = list()
    report_error = list()
    print('Getting org Details')
    org_details = get_orgs(0)

    print('Getting accounts from organization')
    orgs_from_accounts = get_orgs(1)

    for account_name, account_id in orgs_from_accounts.items():
        try:
            session = str
            is_org = False
            if str(org_details['Organization']['MasterAccountId']) == str(account_id):
                is_org = True
            else:
                print('Getting Session to check Account {}'.format(account_name))
                session = get_session(account_name, account_id)

            for roles_from_accounts in get_roles(session, is_org):
                print('Analyzing role {} at account {} '.format(roles_from_accounts['RoleName'], account_name))
                for account in roles_from_accounts['AssumeRolePolicyDocument']['Statement']:
                    if org_details['Organization']['MasterAccountId'] != account['Principal']['AWS'][13:25]:
                        if account_id not in account['Principal']['AWS'][13:25]:
                            if check_authorized(account['Principal']['AWS'][13:25]) is False:
                                print('Role {} with account not authorized {}'.format(roles_from_accounts['RoleName'],
                                                                                      account['Principal']['AWS'][13:25]
                                                                                      ))
                                if os.environ.get('Action').lower() == 'delete':
                                    if del_role(roles_from_accounts['RoleName'], is_org, session) is True:
                                        list_of_deleted_roles.append(roles_from_accounts)
                                else:
                                    list_of_roles_from_accounts.append(roles_from_accounts)

        except:
            print('Erro encontrado!!!')
            error = '{},{},Error: Without permission to assume the role at AWS Account'.format(account_id,
                                                                                               account_name)
            report_error.append(str(error))

    print('Building report...')
    raw = ['Action,Internal Account Id,Internal Account Name,Role Name,Role Created at,Effect of Role,External Account Id']

    for a in list_of_roles_from_accounts:
        internal_account_name = ''
        for account_name, account_id in orgs_from_accounts.items():
            if str(account_id) == str(a['Arn'][13:25]):
                internal_account_name = account_name

        role_name = a['RoleName']
        role_source_account_id = a['Arn'][13:25]
        role_date = a['CreateDate']

        for b in a['AssumeRolePolicyDocument']['Statement']:
            role_effect = b['Effect']
            role_external_account_id = b['Principal']['AWS'][13:25]
            if check_authorized(role_external_account_id) is False:
                raw.append('Manual Check, {},{},{},{},{},{}'.format(role_source_account_id,
                                                      internal_account_name,
                                                      role_name,
                                                      role_date,
                                                      role_effect,
                                                      role_external_account_id))

    for b in list_of_deleted_roles:
        internal_account_name = ''
        for account_name, account_id in orgs_from_accounts.items():
            if str(account_id) == str(b['Arn'][13:25]):
                internal_account_name = account_name

        role_source_account_id = b['Arn'][13:25]
        role_name = b['RoleName']
        role_date = b['CreateDate']

        for x in b['AssumeRolePolicyDocument']['Statement']:
            role_effect = x['Effect']
            role_external_account_id = x['Principal']['AWS'][13:25]

        raw.append('Auto Deleted, {},{},{},{},{},{}'.format(role_source_account_id,
                                                      internal_account_name,
                                                      role_name,
                                                      role_date,
                                                      role_effect,
                                                      role_external_account_id))

    for x in report_error:
        raw.append(x)

    print('Sending message...')
    send_msg('\n'.join(raw))


    return {
        'statusCode': 200,
        'body': json.dumps('')
    }
