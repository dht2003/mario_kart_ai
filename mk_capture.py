import screen_capture
import pygetwindow


class MKScreenCapture(screen_capture.ScreenCapture):
    def __init__(self):
        index = -1
        titles = pygetwindow.getAllTitles()
        for i in range(len(titles)):
            if titles[i].endswith("Mario Kart Wii (RMCE01)"):
                index = i
        if index == -1:
            raise Exception("[MKScreenCapture] Cannot find mario kart window")
        super(MKScreenCapture, self).__init__(titles[index])


