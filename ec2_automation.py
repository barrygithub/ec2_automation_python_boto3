import boto3

'''
#Create session, using profile credential
aws_session = boto3.session.Session(profile_name="barry")
client = aws_session.client("ec2")
'''

#default credential with client class
ec2_client = boto3.client('ec2',region_name="us-west-1")

#default credential with service resource class
ec2_resource = boto3.resource('ec2',region_name="us-west-1")


while True:

    print("Select options to perform on EC2 instance")

    print("""
            1. Create
            2. Start
            3. Stop
            4. Terminate
            5. List all Instances
            6. Exit
        """)
    opt = int(input("Enter your option: "))
    if opt == 1:

        #Create EC2 with service resource
        instances = ec2_resource.create_instances(
            ImageId='ami-06fcc1f0bc2c8943f',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1
        )

        print("Please wait...creating EC2 Instance...")

        #Get Instance Id
        instance_id = (str(instances).split("'"))[1].split("'")[0]

        #Wait until instance is running
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        print("Your EC2 Instance is up and running")
        print("Your EC2 Instance Id is: " + instance_id)
        print(" ")

    elif opt == 2:
        instance_id = input('Enter your EC2 Instance Id: ')
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

        #Start EC2 with client
        ec2_client.start_instances(InstanceIds=[instance_id])

        print("Please wait...Starting your EC2 Instance")
        print(" ")

        #Wait until running status to display result
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        print("Your EC2 Instance is up and running")
        print(" ")

    elif opt == 3:
        instance_id = input('Enter your EC2 Instance Id: ')
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

        #Stop EC2 with client
        ec2_client.stop_instances(InstanceIds=[instance_id])

        print("Please wait...Stopping your EC2 Instance")
        print(" ")

        #Wait until stopped status to display result
        waiter = ec2_client.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])

        print("Your EC2 Instance has stopped")
        print(" ")

    elif opt == 4:
        instance_id = input('Enter your EC2 Instance Id: ')
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

        #Terminate EC2 with client
        ec2_client.terminate_instances(InstanceIds=[instance_id])

        print("Please wait...terminating your EC2 Instance")
        print(" ")

        #Wait until terminated status to display result
        waiter = ec2_client.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[instance_id])

        print("Your EC2 Instance has been terminated")
        print(" ")

    elif opt == 5:
        #describe instance with client
        response = ec2_client.describe_instances()['Reservations']

        #Loop through each item in list and dictionary
        for each_item in response:
            for each in each_item["Instances"]:
                print(' ')
                print("The Instance Id is: {} \nThe Image Id is: {} \nThe Instance Launch Time is: {} \nInstance Type is: {} \nInstance State is: {}".format(each['InstanceId'], each['ImageId'], each['LaunchTime'], each['InstanceType'], each['State']['Name']))
                print("******")
                print(' ')
    else:
        break
