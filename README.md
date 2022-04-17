# aws-cross-account-checker
AWS Cross-Account Checker

![General](/imgs/projeto.svg)

### Environment Variables
To right execution of this code you must configure the variables below:

| Name                          | Value                                                                 | Description                                        |
|-------------------------------|-----------------------------------------------------------------------|----------------------------------------------------|
| OrganizationAccountAccessRole | OrganizationAccountAccessRole                                         | Name of role used to assume role in others account |
| TopicArn                      | arn:aws:sns:us-east-1:111111111111:aws-cross-account-checker | Arn of topic used to send e-mails notification     |
