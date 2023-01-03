readme.txt

Name: Pranav Pokhrel
x500: pokhr013
student id: 5558568
Instructor: David Du
Topic: Programming Project - Sockets and Servers

files included for submission:
    
    proj4211.py - server code file
    client.py - client code file

**IMPORTANT NOTE**
    Since input is being called inside a while loop some messages may not appear until enter is pressed twice due to .recv() being a blocking function and hence if client one publishes to topic and client 2 is subscribed to topic, please hit enter on the command line for client 2.

Server file:
    
    contains one function - main_client(client) - which is called in a start_new_thread in order for the server to host multiple clients

    main_client - 
        
        Allows for all of the communications between the server and the clilent. 
        Holds all the client actions and provides suitable responses based on their choice of action.
        Actions are as follows:

            "SUB" - Subscribe to a Topic
            "PUB" - Publish to a Topic
            "UNSUB" - Unsubscribe from Topic

            P.S. Actions are determined by the client and need to be input into client.py
        
        Holds the initialization of special characters based on writeup
    
    Instructions: 
        
        Run the python module proj4211.py in pyshell
        Allow for server to run initially
        Wait for messages from clients

Client file:
    
    Instructions:
        
        Run the python module client.py in pyshell
        Module requests input:
            
            Initially input "CONNECT" or "DISCONNECT" in order to either connect or disconnect to/from server.
            If input is anything other than "CONNECT" or "DISCONNECT", error pops up and client.py terminates.
            If server is not connected to client and "DISCONNECT" is called, shell gives back an error message and once again, program terminates. 
            Upon connection, client is allowed to pass messages to server
            When client finally chooses to disconnect, and sends "DISCONNECT" to the server, client waits for response from server, after which the server sends an ACK and disconnects the client bringing back the shell.
            
            Formats for action calls upon connection:
                
                "SUB" -> ("SUB","TOPICSTRING") 
                    eg input string: SUB, Topic1/Topic2/Topic3
                
                "PUB" -> ("PUB","TOPICSTRING",RETAIN FLAG = 0 OR 1, "INFORMATION STRING") 
                    eg input string: PUB,TOPIC/TOP,1,hello world
                
                "UNSUB" -> ("UNSUB","TOPICSTRING") 
                    eg input string: UNSUB,Topic
                
                "LIST" -> ("LIST")
                    eg input string: LIST
        
