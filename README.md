```
╔═╗╦ ╦╔═╗  ╔═╗╦═╗╔═╗╔═╗╔═╗  ╔═╗╔═╗╔═╗╔═╗╦ ╦╔╗╔╔╦╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
╠═╣║║║╚═╗  ║  ╠╦╝║ ║╚═╗╚═╗  ╠═╣║  ║  ║ ║║ ║║║║ ║   ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
╩ ╩╚╩╝╚═╝  ╚═╝╩╚═╚═╝╚═╝╚═╝  ╩ ╩╚═╝╚═╝╚═╝╚═╝╝╚╝ ╩   ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
                                                                          
```
Roles cross-accounts are roles used to delegate access to resources in different AWS accounts, ideally within the same organization. Roles cross-accounts enable organizations to allow other IAM Roles or Users from one AWS account; a Trusting Account to assume a role configured in one account, the Trusted Account. Particularly in large and multi-accounts environments, organizations may face the challenge of managing roles effectively; non-authorized cross-account roles may be unknowingly present in accounts they are not supposed to. In other words, your accounts may be trusting other accounts that are external to the organization. Roles can be interpreted as capabilities, and they are usually coupled with permissions policies, this may allow someone to bypass configured permissions, elevate privileges, or opening opportunities for the confused deputy problem, only by having the capability to assume a role configured in another account.
### Project Overview

This project was created as a way to help cloud security professionals to identify and protect their environments from unauthorized roles cross-account, mitigating the risks associated with unauthorized cross-account access. It requires a role to assume roles in other accounts, a Topic on SNS, a list of the organization's accounts, and switching AutoDelete "on" or "off". This last option makes this project work as a detective control, reporting potentially unauthorized roles cross-account, or a corrective control, by automatically eliminating potentially non-authorized roles cross-account. In other words, if you turn AutoDelete on, roles cross-account from accounts outside the organization will be automatically deleteted. 

<img alt="General" height="600" src="./imgs/project.svg" title="General Diagram" width="600"/>

### Environment Variables
To ensure the right execution of this code you must configure the environment variables below:

| Name                          | Value                                                        | Description                                                                             |
|-------------------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| OrganizationAccountAccessRole | OrganizationAccountAccessRole                                | Name of role used to assume role in other accounts                                      |
| TopicArn                      | arn:aws:sns:us-east-1:111111111111:aws-cross-account-checker | Arn of topic used to send e-mail notifications                                          |
| AuthorizedAccounts            | 111111111111,11111111112,11111111113,111111111114            | Authorized Accounts external to the org (separated by comma)                            |
| AutoDelete                    | "on" to enable AutoDelete, any other input will disable it   | If enabled, it will automatically delete potentially non-authorized roles cross-account |

