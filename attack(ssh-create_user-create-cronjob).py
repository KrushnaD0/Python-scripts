import paramiko
import sys

def ssh_connect_and_create_user(host, username, password, new_user, cron_job):
    try:
        # Create an SSH client instance
        client = paramiko.SSHClient()

        # Load system host keys (optional, for verifying remote servers)
        client.load_system_host_keys()

        # Automatically add missing host keys (optional)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        client.connect(hostname=host, username=username, password=password)

        # Step 1: Create a new user using the 'useradd' command (may need sudo privileges)
        create_user_cmd = f"sudo useradd {new_user}"

        stdin, stdout, stderr = client.exec_command(create_user_cmd)
        stdin.write(password + '\n')  # If sudo requires password
        stdin.flush()

        # Print the output and error (if any)
        print("User Creation Output:", stdout.read().decode())
        print("User Creation Error:", stderr.read().decode())

        # Step 2: Add a cron job for periodic tasks
        # Example cron job (run a command every 5 minutes):
        # This adds the cron job to the crontab for the new user
        cron_cmd = f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -'

        stdin, stdout, stderr = client.exec_command(f"sudo -u {new_user} bash -c '{cron_cmd}'")
        stdin.flush()

        # Print the output and error (if any)
        print("Cron Job Addition Output:", stdout.read().decode())
        print("Cron Job Addition Error:", stderr.read().decode())

        # Close the SSH connection
        client.close()

    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
    except paramiko.SSHException as sshException:
        print(f"Failed to connect to the SSH Server: {sshException}")
    except Exception as e:
        print(f"Error: {e}")


# Usage example
if __name__ == "__main__":
    host = "192.168.9.55"  # Replace with your server IP
    username = "qhuser"  # Replace with your SSH username
    password = "C@nTr0L@12#"  # Replace with your SSH password
    new_user = "quickheal"  # Replace with the new username you want to create

    # Cron job command, format: <minute> <hour> <day of month> <month> <day of week> <command>
    cron_job = "*/5 * * * * echo 'Hello World' > /home/quickheal/hello.txt"

    ssh_connect_and_create_user(host, username, password, new_user, cron_job)
