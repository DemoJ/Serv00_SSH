import os
import paramiko
from notify import send

def ssh_connect(host, port, username, password, command):
    """
    自动通过SSH连接服务器并执行命令。

    :param host: 服务器IP地址或域名
    :param port: SSH端口号（默认22）
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
            print("连接serv00服务器成功，命令输出：")
            print(output)
            send("serv00保活","连接serv00服务器成功，命令输出：{}".format(output))
        if error:
            print("命令错误：")
            print(error)
            send("serv00保活","连接serv00服务器成功，命令错误：{}".format(output))

        return output if output else error
    except Exception as e:
        print(f"发生错误：{e}")
        send("serv00保活","连接serv00服务器失败：{}".format(e))
    finally:
        # 确保关闭连接
        client.close()
        print("连接已关闭")

if __name__ == "__main__":
    # 从环境变量中获取配置
    server_host = os.getenv("SSH_HOST")  # 服务器IP或域名
    server_port = int(os.getenv("SSH_PORT", 22))  # 默认SSH端口22
    username = os.getenv("SSH_USER")  # SSH用户名
    password = os.getenv("SSH_PASS")  # SSH密码
    command_to_execute = os.getenv("SSH_COMMAND", "ls -la")  # 默认命令

    # 检查必要的环境变量是否已设置
    if not all([server_host, username, password]):
        print("请确保已设置以下环境变量：SSH_HOST, SSH_USER, SSH_PASS")
    else:
        # 执行SSH连接
        ssh_connect(server_host, server_port, username, password, command_to_execute)
