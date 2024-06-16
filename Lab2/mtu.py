import argparse
import platform
import socket
import subprocess


header_size = 28


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find the minimum MTU value in the channel between hosts"
    )
    parser.add_argument("host", type=str, help="Destination host address")
    return parser.parse_args()


def ping(host, count=1, df=False, size=None):
    if platform.system().lower() == "windows":
        count_option = "-n"
        size_option = "-l"
        df_flag = ["-f"]
    elif platform.system().lower() == "darwin":
        count_option = "-c"
        size_option = "-s"
        df_flag = ["-D"]
    else:
        count_option = "-c"
        size_option = "-s"
        df_flag = ["-M", "do"]

    args = [
        "ping",
        count_option,
        str(count),
    ]
    if df:
        args.extend(df_flag)

    if size is not None:
        args.append(size_option)
        args.append(str(size))

    args.append(host)

    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return True
        else:
            return False
    except Exception as ex:
        print(f"Failed to send ping: {str(ex)}")
        return False


def check_address(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        try:
            ip = socket.gethostbyname(address)
        except socket.error:
            raise RuntimeError("Invalid address")

    if not ping(address, count=5):
        raise RuntimeError("Host is unreachable")


def get_mtu(host):
    left = 0
    right = 10000 # default MTU size is 1500

    try:
        while left <= right:
            mid = (left + right) // 2
            if ping(host, df=True, size=mid):
                left = mid + 1
            else:
                right = mid - 1

        print(f"Minimum MTU: {right + header_size} bytes")
    except Exception as ex:
            print(str(ex))


def main():
    args = parse_arguments()
    check_address(args.host)
    get_mtu(args.host)


if __name__ == '__main__':
    main()
