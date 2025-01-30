from modules.port_scanner import port_scanner
from modules.brute_forcer import brute_force_ftp
from modules.banner_grabber import banner_grabber


def main():
    print("Welcome to Penetration Testing Toolkit!")
    print("1. Port Scanner")
    print("2. Brute-Forcer")
    print("3. Banner Grabber")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        host = input("Enter target host: ")
        ports = range(1, 1025)
        port_scanner(host, ports)
    elif choice == 2:
        host = input("Enter FTP host: ")
        username = input("Enter username: ")
        password_list = ["1234", "admin", "password"]  # Replace with file input
        brute_force_ftp(host, username, password_list)
    elif choice == 3:
        host = input("Enter host: ")
        port = int(input("Enter port: "))
        banner_grabber(host, port)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
