import socket
import os
import select
from _thread import *

host = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((host,port))
except socket.error as e:
    print(str(e))
print("socket is listening")
server.listen(5)

topic = {}
retain = {}
msg = []
client_list = []

def multi_client(connection):
    print("1")
    connection.send('connected'.encode())
    client_list.append(connection)
    while True:
        data = connection.recv(2048)
        if not data : 
            continue
        else:
            msg = data.decode('utf-8').split(',')

            if msg[0] == "DISCONNECT":
                connection.send("ACK".encode())
                break

            selected_topics = []
            if msg[0] == "SUB" or msg[0] == "PUB" or msg[0] == "UNSUB":
                x = msg[1]
                y = x.split("/")
                print("num levels = " + str(len(y)) + " levels")
                for i,signs in enumerate(y):
                    if signs == "#":
                        for key in topic.keys():
                            z = key.split('/')
                            t_check = True
                            for j in range(i):
                                if z[j] != y[j]:
                                    t_check = False
                            if t_check:
                                selected_topics.append(key)
                        
                    elif signs == "+":
                        for key in topic.keys():
                            z = key.split('/')
                            if len(y) == len(z):
                                t_check = True
                                for j in range(len(y)):
                                    if i == j:
                                        continue
                                    if z[j] != y[j]:
                                        t_check = False
                                if t_check == True:
                                    selected_topics.append(key)

                if not selected_topics:
                    selected_topics.append(msg[1])

            #listed = []
            if msg[0] == "SUB":
                for i in range(len(client_list)):
                    if client_list[i] == connection:
                        for selected_topic in selected_topics:
                            if selected_topic not in topic.keys():        
                                topic[selected_topic] = []
                            else:
                                try:
                                    retainmsg = retain[selected_topic]
                                    connection.send(retainmsg.encode())
                                except KeyError:
                                    pass
                            if i not in topic[selected_topic]:            
                                topic[selected_topic].append(i)
                            
                print(selected_topics)            
                connection.send("subscribed!".encode())
            
            elif msg[0] == "PUB":
                for i in range(len(client_list)):
                    if client_list[i] == connection: 
                        for selected_topic in selected_topics:
                            if selected_topic not in topic.keys(): 
                                topic[selected_topic] = []
                            response = msg[3]
                            if msg[2] == "1":
                                retain[selected_topic] = response
                            for j in topic[selected_topic]:
                                client_list[j].send(response.encode())
                connection.send("message published".encode()) 

            elif msg[0] == "UNSUB":
                for i in range(len(client_list)):
                    if client_list[i] == connection:
                        check = False
                        for selected_topic in selected_topics:
                            if selected_topic not in topic.keys() or i not in topic[selected_topic]:
                                connection.send("error (subscription not found)".encode())
                                check = True
                        if not check:
                            for selected_topic in selected_topics:
                                for j in topic[selected_topic]:
                                    if j == i:
                                        topic[selected_topic].remove(j)
                                        connection.send("UNSUBSCRIBED".encode())

            
            elif msg[0] == "LIST":
                sub_list = "" #list for topics subscribed by each client for msg = "LIST"
                for i in range(len(client_list)):
                    if client_list[i] == connection:
                        count = 0
                        for subs in topic.keys():
                            for j in topic[subs]: 
                                if j == i:    
                                    count += 1
                                    sub_list += "," + subs
                        final_string = str(count) + sub_list
                        connection.send(final_string.encode())
            else:
                connection.send("value not defined".encode())
    
while True:
    Client, address = server.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_client, (Client, ))



