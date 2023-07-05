from qfluentwidgets import SplashScreen


class SplashScreenWithFadeOut(SplashScreen):

    def finish(self):
        # TODO: 开屏页渐出动画

        # self.opacityAni = QPropertyAnimation(self, b"windowOpacity")
        # self.opacityAni.setDuration(187)
        #
        # self.opacityAni.setStartValue(0)
        # self.opacityAni.setEndValue(1)
        #
        # self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.close()
