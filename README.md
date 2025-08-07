#  ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓████████▓▒░+ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░+░▒▓█▓▒░+++++ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░+░▒▓█▓▒░+++++ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░+░▒▓██████▓▒░░▒▓███████▓▒░++░▒▓█▓▒░+++++ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░++░▒▓█▓▒░+++░▒▓█▓▒░++++++++░▒▓█▓▒░+++++ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░++░▒▓█▓▒░+++░▒▓█▓▒░++++++++░▒▓█▓▒░+++++ #
#  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░++░▒▓█▓▒░+++░▒▓█▓▒░++++++++░▒▓█▓▒░+++++ #
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



Nkrypt is a very simple P2P messaging app with E2EE, written in python. 
The files include p2p_node.py, the main program, and p2p_launcher.py, the launcher. 
To start the program, execute p2p_launcher.py, press 2 for a demo or 1 for a direct chat. 

Syntax : 

connect <node_ID>@<host>:<port> == connect "name of target"@"name of host (localhost)":"number of port (8002 for demo)"
            EG : connect alice@localhost:8002

msg <node_ID> <message> == msg "name of target" "message"
            EG : msg bob Heyyy
            
quit : quits? 

credits to me, made this in a few hours, might still be laggy. 

Not licensed, please use with authorization and in good spirit :)
