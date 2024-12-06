import os
import paramiko
from notify import send

def ssh_connect(host, port, username, password, command):
    """
    自动通过SSH连接服务器并执行命令。

    :param host: 服务器IP地址或域名
    :param port: SSH端口号
    :param username: SSH用户名
    :param password: SSH密码
    :param command: 要执行的命令
    :return: 命令执行的输出
    """
    try:
        # 创建SSH客户端
        client = paramiko.SSHClient()
        # 自动添加未知主机到known_hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        client.connect(hostname=host, port=port, username=username, password=password)
        print(f"成功连接到 {host}:{port}")

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            msg = "连接{}服务器成功，命令输出：{}".format(host,output)

        if error:
            msg = "连接{}服务器成功，命令错误：{}".format(host,error)

        print(msg)
        return msg

    except Exception as e:
        msg = "连接{}服务器失败：{}".format(host,e)
        print(msg)
        return msg
    finally:
        # 确保关闭连接
        client.close()
        print("{}连接已关闭".format(host))

if __name__ == "__main__":
    # 从环境变量中获取配置
    server_hosts = os.getenv("SSH_HOST").split("\n")  # 服务器IP或域名
    server_ports = os.getenv("SSH_PORT","\n".join(["22"] * len(server_hosts))).split("\n")  # SSH端口号,默认都为22
    usernames = os.getenv("SSH_USER").split("\n")  # SSH用户名
    passwords = os.getenv("SSH_PASS").split("\n")  # SSH密码
    command_to_executes = os.getenv("SSH_COMMAND","\n".join(["ls -la"] * len(server_hosts))).split("\n")  # 需执行的命令，默认都为ls -la

    # 确保每组信息的数量一致
    if not (len(server_hosts) == len(server_ports) == len(usernames) == len(passwords) == len(command_to_executes)):
        print("环境变量配置错误：每组服务器信息的数量不一致")
    else:
        msgs = "Serv00保号\n"
        # 遍历所有的服务器配置
        for server_host, server_port, username, password,command_to_execute in zip(server_hosts, server_ports, usernames, passwords,command_to_executes):
            msg=ssh_connect(server_host, server_port, username, password, command_to_execute)
            msgs += msg + "\n"
        send("Serv00保号信息",msgs)
