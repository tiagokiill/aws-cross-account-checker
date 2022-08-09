"""
    __authors__ = "Tiago kiill and Teogenes Panella"
    __emails__ = "tiago@kiill.net and teo.panella@gmail.com"
    __credits__ = "Tiago Kiill and Teogenes Panella"
"""

import json
import os
from remotesession import Session
from awsorg import AwsOrg
from awsorg import AuthorizedAccounts
from iamroles import AwsIamRemote
from iamroles import AwsIamLocal
from report import ReportBuilder
from report import AwsSnsSender


def lambda_handler(event, context):
    awsorg = AwsOrg()
    authorized_account = AuthorizedAccounts()
    accounts_from_org = awsorg.get_org_account_list_name_and_id()
    list_of_roles_from_accounts = list()

    print('Params...')
    print('Using role name {} to STS'.format(os.environ.get('OrganizationAccountAccessRole')))
    print('Authorized accounts: {}'.format(os.environ.get('AuthorizedAccounts')))
    print('Sending message on Topic: {}'.format(os.environ.get('TopicArn')))
    if os.environ.get('AutoDelete').lower() == 'on':
        print('Auto Delete "on"')
    else:
        print('Auto Delete "off"')
    print('Starting JOB...')
    print('-------------------------------------------------------------------\n')

    for i_account_name, i_account_id in accounts_from_org.items():
        if i_account_id == awsorg.get_org_master_account_id():
            for role_name, r_account_id in AwsIamLocal().get_list_of_role_names_and_ids_from_local_account().items():
                if authorized_account.check_authorized(r_account_id) is False:
                    if os.environ.get('AutoDelete').lower() == 'on':
                        if AwsIamLocal().remove_policies_from_local_account(role_name) is True:
                            if AwsIamLocal().delete_role_from_local_account(role_name) is True:
                                list_of_roles_from_accounts.append('{},{},{},{}'.format('Deleted', role_name,
                                                                                        r_account_id, i_account_name))
                            else:
                                list_of_roles_from_accounts.append('{},{},{},{}'.format('Error to delete', role_name,
                                                                                        r_account_id, i_account_name))
                    else:
                        list_of_roles_from_accounts.append('{},{},{},{}'.format('Manual', role_name,
                                                                                r_account_id, i_account_name))
        else:
            session = Session(i_account_name, i_account_id).get_remote_session_token()
            for role_name, r_account_id in \
                    AwsIamRemote(session).get_list_of_role_names_and_ids_from_remote_account().items():
                if authorized_account.check_authorized(r_account_id) is False:
                    if os.environ.get('AutoDelete').lower() == 'on':
                        if AwsIamRemote(session).remove_policies_from_remote_account(role_name) is True:
                            if AwsIamRemote(session).delete_role_from_remote_account(role_name) is True:
                                list_of_roles_from_accounts.append('{},{},{},{}'.format('Deleted', role_name,
                                                                                        r_account_id, i_account_name))
                        else:
                            list_of_roles_from_accounts.append('{},{},{},{}'.format('Error to delete', role_name,
                                                                                    r_account_id, i_account_name))
                    else:
                        list_of_roles_from_accounts.append('{},{},{},{}'.format('Manual', role_name,
                                                                                r_account_id, i_account_name))

    if not list_of_roles_from_accounts:
        AwsSnsSender().send_sns_msg('There aren´t unauthorized accounts')
    else:
        ReportBuilder(list_of_roles_from_accounts).build_report_to_sns

    return {
        'statusCode': 200,
        'body': json.dumps('Job executed with success')
    }
