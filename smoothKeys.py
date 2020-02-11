""" A script to simple smooth animation curves along the selected channels in maya

    Usage : Select the channel(s) along which to smooth the curve,
            make sure to select atleast 3 contolVertices or the script will not work,
            as we are not touching the first and the last frame while smoothening.

            run the script (source)
            and execute smoothKeys()

    Author : vivek-v
"""

import maya.cmds as cmds

def smoothKeys():
    """ Function to smooth the animation curve controlVertices
    """
    # Get the selected curves
    curves = cmds.keyframe(query = True, name = True)

    if len(curves) == 0:
        raise ValueError("Select at least 3 keys in the Graph Editor.")
    else:
        for curve in curves:
            keys = cmds.keyframe(curve, query = True, selected = True) # Frame Numbers
            sizeOfKeys = len(keys)

            # The first and last keys will not be changed, so atleast three should be selected
            if not sizeOfKeys < 3:
                # Duplicate the curve(s) to store the values
                dupCurve = cmds.duplicate(curve)

                # Starting the range with second frame
                for i in range(1, (sizeOfKeys-1)):
                    prevVal = cmds.keyframe(curve, vc = True ,time = (keys[i-1], keys[i-1]), query = True)
                    currVal = cmds.keyframe(curve, vc = True ,time = (keys[i], keys[i]), query = True)
                    nextVal = cmds.keyframe(curve, vc = True ,time = (keys[i+1], keys[i+1]), query = True)

                    # calculating Average of the frame value
                    average = (prevVal[0] + currVal[0] + nextVal[0])/3

                    # storing the values in the duplicate curve
                    cmds.keyframe(dupCurve[0], vc = average ,time = (keys[i], keys[i]), absolute = True)

                # applying the values
                for i in range(1, (sizeOfKeys-1)):
                    dupCurveVal = cmds.keyframe(dupCurve[0], vc = True ,time = (keys[i], keys[i]), query = True)
                    cmds.keyframe(curve, vc = dupCurveVal[0] ,time = (keys[i], keys[i]), absolute = True)

                # deleting the duplicate curve(s) created
                cmds.delete(dupCurve[0])

            else:
                raise ValueError("Select at least 3 keys in the Graph Editor.")

smoothKeys()
