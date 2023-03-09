import musicalbeeps
from melody import Melody

if __name__ == "__main__":
    player = musicalbeeps.Player()
    melody = Melody("birthday.txt")
    melody.play(player)
