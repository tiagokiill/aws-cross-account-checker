"""
    __authors__ = "Tiago kiill and Teogenes Panella"
    __emails__ = "tiago@kiill.net and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import boto3
import json
import os
from remotesession import Session
from awsorg import AwsOrg
from awsorg import AuthourizedAccount
from iamroles import AwsIamRemote


def send_msg(accounts_from_roles):
    """
        Explanation: Method defined to send the msg with the report
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


def remove_policies(rolename, org_account, session):
    """
        Explanation: Method defined to detach policies from roles
        :params: str session
        :params: bol or_account
        :params: session to STS
        :return: without return
    """
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

        return response


def del_role(rolename, org_account, session):
    """
        Explanation: Method defined to delete potentially non-authorized role
        :params: str session
        :params: bol org_account
        :params: session to STS
        :return: bol True or False
    """
    try:
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
    except:
        return False


def lambda_handler(event, context):
    print('Params...')
    print('Using role name {} to STS'.format(os.environ.get('OrganizationAccountAccessRole')))
    print('Authorized accounts: {}'.format(os.environ.get('AuthorizedAccounts')))
    print('Sending message on Topic: {}'.format(os.environ.get('TopicArn')))
    if os.environ.get('AutoDelete').lower() == 'on':
        print('Auto Delete "on"')
    else:
        print('Auto Delete "off"')
    print('-------------------------------------------------------------------\n')
    print('Starting JOB...')

    list_of_roles_from_accounts = list()
    list_of_deleted_roles = list()
    report_error = list()
    print('Getting org Details')
    awsorg = AwsOrg()
    authorized_account = AuthourizedAccount()

    print('Getting accounts from organization')
    accounts_from_org = awsorg.get_org_account_list_name_and_id()

    for account_name, account_id in accounts_from_org.items():
        try:
            is_org = False
            if str(awsorg.get_org_master_account_id()) == str(account_id):
                is_org = True
            else:
                print('Getting Session to check Account {}'.format(account_name))
                session = Session(account_name, account_id)
                session_token = session.get_remote_session_token()
                remote_role_name = AwsIamRemote(session_token)

            for r_role_name, \
                r_account_id in remote_role_name.get_list_of_role_names_and_ids_from_remote_account().items():
                print('Analyzing role {} at account {} '.format(r_role_name, account_name))
                if awsorg.get_org_master_account_id() != r_account_id:
                    if account_id not in r_account_id:
                        if authorized_account.check_authorized(r_account_id) is False:
                            print('Role {} with account not authorized {}'.format(r_role_name,
                                                                                  account_id
                                                                                  ))
                            if os.environ.get('AutoDelete').lower() == 'on':
                                if del_role(r_role_name, is_org, session_token) is True:
                                    list_of_deleted_roles.append(r_role_name)
                            else:
                                list_of_roles_from_accounts.append(r_role_name)

        except:
            print('Error Found: at Account {}'.format(account_name))
            error = '{},{},Error: Without permission to assume the role at AWS Account'.format(account_id,
                                                                                               account_name)
            report_error.append(str(error))

    print('Building report...')
    header = '| {:<14} | {:<21} | {:<17} | {:<52} | {:<17} | {:<21} | {:<25} |'.format('Action',
                                                                                       'Internal Account Id',
                                                                                       'Account Name',
                                                                                       'Role Name',
                                                                                       'Effect of Role',
                                                                                       'External Account Id',
                                                                                       'Role Created at')
    raw = [header]

    for a in list_of_roles_from_accounts:
        internal_account_name = ''
        for account_name, account_id in accounts_from_org.items():
            if str(account_id) == str(a['Arn'][13:25]):
                internal_account_name = account_name

        role_name = a['RoleName']
        role_source_account_id = a['Arn'][13:25]
        role_date = a['CreateDate']

        for b in a['AssumeRolePolicyDocument']['Statement']:
            role_effect = b['Effect']
            role_external_account_id = b['Principal']['AWS'][13:25]
            if authorized_account.check_authorized(r_account_id) is False:
                raw.append('| {:<14} | {:<21} | {:<17} | {:<52} | {:<17} | {:<21} | {} |'.format('Manual Check',
                                                                                                 role_source_account_id,
                                                                                                 internal_account_name,
                                                                                                 role_name,
                                                                                                 role_effect,
                                                                                                 role_external_account_id,
                                                                                                 role_date))

    for b in list_of_deleted_roles:
        internal_account_name = ''
        for account_name, account_id in accounts_from_org.items():
            if str(account_id) == str(b['Arn'][13:25]):
                internal_account_name = account_name

        role_source_account_id = b['Arn'][13:25]
        role_name = b['RoleName']
        role_date = b['CreateDate']
        role_effect = ''
        role_external_account_id = ''
        for x in b['AssumeRolePolicyDocument']['Statement']:
            role_effect = x['Effect']
            role_external_account_id = x['Principal']['AWS'][13:25]

        raw.append('| {:<14} | {:<21} | {:<17} | {:<52} | {:<17} | {:<21} | {} |'.format('Auto Deleted',
                                                                                         role_source_account_id,
                                                                                         internal_account_name,
                                                                                         role_name,
                                                                                         role_effect,
                                                                                         role_external_account_id,
                                                                                         role_date))
    for x in report_error:
        raw.append(x)

    print('Sending message...')
    send_msg('\n'.join(raw))
    print('\n'.join(raw))

    return {
        'statusCode': 200,
        'body': json.dumps('Job executed with success')
    }
