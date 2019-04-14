import maya.cmds as cmds

source = cmds.listConnections('pCube1', destination = False, plugs = True)
destination = cmds.listConnections('pCube1', destination = True)


cmds.disconnectAttr('pCube1_translateX.output', 'pCube1_translateX')


connections = cmds.listConnections('pCube1', connections = True, plugs = True)

source = []
destination = []

for con in connections:
    if con.endswith('.output'):
        destination.append(con)
    else:
        source.append(con)
        

for i in range(len(source)):
    cmds.disconnectAttr(destination[i], source[i])
    
for i in range(len(source)):
    cmds.connectAttr(destination[i], source[i])