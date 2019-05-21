import paramiko


paramiko.util.log_to_file("ssh.log")

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy())

client.connect(
    hostname=localhost,
    username=root,
    gss_auth=paramiko.GSS_AUTH_AVAILABLE,
    gss_kex=paramiko.GSS_AUTH_AVAILABLE,
)
