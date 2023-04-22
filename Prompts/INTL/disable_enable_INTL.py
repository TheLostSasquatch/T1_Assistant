import paramiko

trunk = "DEN70CCUN0002W80002"
status = "enable"

# Define the SSH connection details
hostname = '*******'   # Replace with the hostname or IP address of the remote server
port = 22                   # Replace with the SSH port of the remote server
username = 'a-*****' # Replace with your username on the remote server
password = '******' # Replace with your password on the remote server

# Create an SSH client object
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Enable INTL on trunk
if status == "enable":
    try:
        # Connect to the remote server
        client.connect(hostname, port, username, password)

        # Run a command on the remote server
        command = f'sendcmd host=********* command=enableIntlTG tg={trunk}' # Replace with the command you want to run
        stdin, stdout, stderr = client.exec_command(command)

        # Print the output of the command
        print(stdout.read().decode())

        # Close the SSH connection
        client.close()

    except Exception as e:
        print(f'Error: {e}')
        client.close()

# Disable INTL on trunk
if status == "disable":
    try:
        # Connect to the remote server
        client.connect(hostname, port, username, password)

        # Run a command on the remote server
        command = f'sendcmd host=******** command=enableIntlTG tg={trunk}' # Replace with the command you want to run
        stdin, stdout, stderr = client.exec_command(command)

        # Print the output of the command
        print(stdout.read().decode())

        # Close the SSH connection
        client.close()

    except Exception as e:
        print(f'Error: {e}')
        client.close()