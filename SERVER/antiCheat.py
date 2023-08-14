import logging
from constants import setupLogger
# SETTINGS
MAX_X_MOVEMENT_PF = 10
MAX_Y_MOVEMENT_PF = 10


def checkValues(playerData, playerList, pid):
    logger = logging.getLogger("server-AC")
    logger = setupLogger(logger)
    ACR = ""  # anticheat reason
    # movement check
    if abs(playerList[pid].x - playerData.x) > MAX_X_MOVEMENT_PF:  # moved more than ~ units in 1 frame
        playerList[pid].x = playerList[pid].x
        ACR = "MAX_X_MOVEMENT_PF EXCEEDED"
    else:
        playerList[pid].x = playerData.x  # x

    if abs(playerList[pid].y - playerData.y) > MAX_Y_MOVEMENT_PF:
        playerList[pid].y = playerList[pid].y
        ACR = "MAX_Y_MOVEMENT_PF EXCEEDED"
    else:
        playerList[pid].y = playerData.y  # y

    if ACR != "":
        logger.warning(f"Triggered on player id: {pid} with reason \"{ACR}\"")
