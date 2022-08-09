import boto3
import os


class ReportBuilder:
    def __init__(self, list_of_roles_from_accounts):
        self.list_of_deleted_roles = list_of_roles_from_accounts

    def build_report_to_sns(self):
        """
            Explanation: Method defined to build a msg to sns channel
            :params: N/A
            :return: True if the message was sent
        """
        msg = list()

        for line in self.list_of_deleted_roles:
            executed_action = line.split(',')[0]
            r_role_name = line.split(',')[1]
            r_account_id = line.split(',')[2]
            account_name = line.split(',')[3]

            if executed_action == 'Deleted':
                msg.append('No action is necessary! The role name "{}" was "{}". The role was allowing the '
                           'unauthorized account "{}" to access your account "{}"'.format(r_role_name, executed_action,
                                                                                          r_account_id, account_name))
            else:
                msg.append('"{}" action is necessary! The role name "{}" still allows the unauthorized '
                           'account "{}" to access your account "{}"'.format(executed_action, r_role_name, r_account_id,
                                                                             account_name))

        if AwsSnsSender().send_sns_msg('\n'.join(msg)) is True:
            return True
        else:
            return False


class AwsSnsSender:
    def __init__(self):
        self.topic = os.environ.get('TopicArn')
        self.sns_client = boto3.client('sns')

    def send_sns_msg(self, msg):
        """
            Explanation: Method defined to send the msg with the report
            :params: str with message to send
            :return: True if the message was sent
        """
        print('Sending message...')
        response = self.sns_client.publish(
            TopicArn=self.topic,
            Message=str(msg),
            Subject=' ** - REPORT - ** AWS Cross Account Checker'
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('msg sent at {}'.format(response['ResponseMetadata']['HTTPHeaders']['date']))
            return True
