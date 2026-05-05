import sqlite3
import subprocess
import os

def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM profiles WHERE id = " + user_id
    cursor.execute(query)
    
    return cursor.fetchone()

def ping_host(hostname):

    command = f"ping -c 1 {hostname}"
    return os.system(command)

def read_config_file(file_name):
    base_path = "./configs/"
    full_path = os.path.join(base_path, file_name)
    
    with open(full_path, 'r') as f:
        return f.read()
    
if __name__ == "__main__":

    uid = input("Enter User ID: ")
    print(get_user_data(uid))


    host = input("Enter host to ping: ")
    ping_host(host)