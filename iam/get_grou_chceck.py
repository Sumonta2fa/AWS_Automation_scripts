import boto3, json

group_name = "Admin"
inline_dict = {
		"admin-policy": '[{"Action": "*", "Resource": "*", "Effect": "Allow"}]',
		"policygen-Admin-202004021457": '[{"Action": ["appsync:*"], "Resource": ["*"], "Effect": "Allow", "Sid": "Stmt1585819630000"}, {"Action": ["acm:*"], "Resource": ["*"], "Effect": "Allow", "Sid": "Stmt1585819648000"}]',
		"testAdmin": '[{"Action": "*", "Resource": "*", "Effect": "Allow"}]'
	}

managed_dict = {
					"arn:aws:iam::aws:policy/AmazonEC2FullAccess": "2018-11-27 02:16:56+00:00",
					"arn:aws:iam::xx:policy/UsersReadOnlyAccesstoIAMConsole-08042020": "2020-04-08 09:54:39+00:00"
					}
output = "Compliance"



if __name__ == '__main__':
	session = boto3.Session(profile_name='priv')

	iam = session.client('iam')

	# Get attached Inline policy 
	inlinePolies = iam.list_group_policies(GroupName=group_name)

	print "List of Inline Policies: ", inlinePolies['PolicyNames']
	for inline_policy in inlinePolies['PolicyNames']:
		print inline_policy
		#Get Inline policy details
		get_inline_policy = iam.get_group_policy(
							    GroupName=group_name,
							    PolicyName=inline_policy)
		policy_document = json.dumps(get_inline_policy["PolicyDocument"]["Statement"])
		print policy_document
		#+Policy Name Check"
		try:
			inline_dict[inline_policy]
			print("key exist")
		except KeyError:
			print("key not exist")
			output = "Non-Compliance"
			print "Policy name not matched: ", output
			exit(1)

		#+Policy Content Check"
		if policy_document != inline_dict[inline_policy]:
			output = "Non-Compliance"
			print "Policy document not matched: ",output
			exit(1)

	# Get attached Managed policy 
	ManagedPolicies = iam.list_attached_group_policies(GroupName='Admin')

	for MP in ManagedPolicies['AttachedPolicies']:
		# print "=========="
		policy_arn = MP['PolicyArn']
		print policy_arn

				#+Policy Name Check"
		try:
			managed_dict[policy_arn]
			print("Manage policy exist")
		except KeyError:
			print("Manage  policy not exist")
			output = "Non-Compliance"
			print "Manage Policy name not matched: ", output
			exit(1)
		
		#+Policy Content Check"

		updateDate = iam.get_policy(PolicyArn=policy_arn)['Policy']["UpdateDate"]
		print updateDate
		
		if str(updateDate) != managed_dict[policy_arn]:
			output = "Non-Compliance"
			print "managePolicy date not matched: ",output
			exit(1)


    	# get_policy_response = iam.get_policy(PolicyArn=policy_arn)['Policy']
    	# print get_policy_response
    	# print "Managed policy update date: " , get_policy_response['UpdateDate']
    	# default_version = get_policy_response["DefaultVersionId"]


