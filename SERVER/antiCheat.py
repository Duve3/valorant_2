# SETTINGS
MAX_X_MOVEMENT_PF = 10
MAX_Y_MOVEMENT_PF = 10


def checkValues(playerData, playerList, pid):
    ACR = ""  # anticheat reason
    # movement check
    if abs(playerList[pid].x - playerData[0]) > MAX_X_MOVEMENT_PF:  # moved more than ~ units in 1 frame
        playerList[pid].x = playerList[pid].x
        ACR = "MAX_X_MOVEMENT_PF EXCEEDED"
    else:
        playerList[pid].x = playerData[0]  # x

    if abs(playerList[pid].y - playerData[1]) > MAX_Y_MOVEMENT_PF:
        playerList[pid].y = playerList[pid].y
        ACR = "MAX_Y_MOVEMENT_PF EXCEEDED"
    else:
        playerList[pid].y = playerData[1]  # y

    if ACR != "":
        print("ANTICHEAT: Triggered on player id:", pid, "with reason:\"", ACR, "\"")
