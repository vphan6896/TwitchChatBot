import socket

# Globals are bad!
credentials = open("secret", "r")
irc_token = credentials.readline()
client_id = credentials.readline()
nickname = credentials.readline()
prefix = "!"
channel = credentials.readline().rstrip('\n')
secret = credentials.readline()
credentials.close()
print(irc_token, client_id, nickname, channel)


def main():
    sock = openSocket(irc_token, nickname, channel)
    readbuffer = ""
    print(">>Socket is opened")
    joinRoom(sock)
    while True:
        print(">>reading")
        readbuffer = readbuffer + sock.recv(2048).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            print(line)
            if line.startswith('PING'):
                print(">>We got pinged!")
                sock.send("PONG\n".encode('utf-8'))
                print(">>We ponged back")
                # If we don't break, we get index out of range error with getmessage
                break
            user = getUser(line)
            message = getMessage(line)
            print(user + " typed: " + message)
            if "hi" in message:
                sendMessage(sock, "No you")
                break


def joinRoom(sock):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + sock.recv(2048).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            print(">>" + line)
            Loading = loadingComplete(line)
    sendMessage(sock, "Successfully joined chat")
    print(">>Finished loading")


def loadingComplete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True


def openSocket(p, n, c):
    # This is referring to the Python standard library
    s = socket.socket()
    s.connect(("irc.twitch.tv", 6667))
    s.send(("PASS " + p + "\r\n").encode('utf-8'))
    s.send(("NICK " + n + "\r\n").encode('utf-8'))
    s.send(("JOIN #" + c + "\r\n").encode('utf-8'))
    return s


def sendMessage(s, message):
    messageTemp = f"PRIVMSG #" + channel + " :" + message + "\r\n"
    s.send(messageTemp.encode('utf-8'))
    print(">>Sent: " + messageTemp)


def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def getMessage(line):
    separate = line.split(":", 2)
    message = separate[2]
    return message


if __name__ == '__main__':
    main()
