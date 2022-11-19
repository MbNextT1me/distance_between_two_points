import matplotlib.pyplot as plt
import numpy as np
import socket

host = "84.237.21.36"
port = 5152
packet_size = 40002

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n-len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def find_distance(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

def find_max(img):
    max = []
    for i in range(1, len(img) - 1):
        for j in range(1, len(img[i] - 1)):
            if img[i - 1][j] < img[i][j] and img[i + 1][j] < img[i][j] and img[i][j - 1] < img[i][j] and img[i][j + 1] < img[i][j]:
                max.append((i, j))
    return max

plt.ion()
plt.figure()
yeps = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    while yeps < 10:
        sock.send(b"get")
        bts = recvall(sock, packet_size)
        rows, cols = bts[:2]
        im = np.frombuffer(bts[2:rows * cols + 2], dtype="uint8").reshape(rows, cols)

        pos1 = np.unravel_index(np.argmax(im), im.shape)
        plt.clf()

        points = find_max(im)
        
        dist = 0
        if len(points) >= 2:
            dist = round(find_distance(points[0], points[1]), 1)

        plt.imshow(im)
        plt.pause(1)

        sock.send(str(dist).encode())
        beat = sock.recv(20)

        if beat == b'yep':
            yeps += 1
        
        print(f"Distance: {dist}\nBeat: {beat}\nYeps: {yeps}\n")

print("Done!")