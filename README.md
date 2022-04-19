# aws-cross-account-checker
AWS Cross-Account Checker

![General](/imgs/projeto.svg)

### Environment Variables
To right execution of this code you must configure the variables below:

| Name                          | Value                                                                 | Description                                        |
|-------------------------------|-----------------------------------------------------------------------|----------------------------------------------------|
| OrganizationAccountAccessRole | OrganizationAccountAccessRole                                         | Name of role used to assume role in others account |
| TopicArn                      | arn:aws:sns:us-east-1:111111111111:aws-cross-account-checker | Arn of topic used to send e-mails notification     |


### Backlog

1 - Send the report as csv attached: Here it's necessary to change the service sns;

2 - Environment list of allowed account's id;

3 - Automatic removal of roles with external accounts;

4 - The Open Source license.

5 - The new diagram.

6 - Text of this project proposal