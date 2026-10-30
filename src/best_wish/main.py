import math
import random
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont


# 进行窗口创建，无数窗口不断创建
# 可以用pyQt，感觉，然后每个窗口属性不一样（设置上数组存储随机挑选吧）
# 使用函数工厂类进行制造管理,执行产生次数

# 随机属性
TITLES = ["开心", "向阳", "拾光", "星芒", "启航", "逐风", "晴川", "悦然",
          "清欢", "知暖", "星途", "沐光", "云舒", "朝晖", "颂安", "澄明"]

CONTENTS = [
    "常带欢颜，好运连连",
    "新程似锦，一路繁花",
    "暖阳相伴，岁岁欢喜",
    "乘风奔赴，万事可期",
    "星光熠熠，万事胜意",
    "甜序常伴，岁岁无忧",
    "平安愉乐，自在随心",
    "风和日暖，诸事顺意",
    "向阳向荣，好运不停",
    "熠熠生辉，前程坦荡",
    "云光熹微，好事将近",
    "嘉福常临，岁岁安康",
    "朗月相伴，喜乐无忧",
    "禾风舒扬，万事从容",
    "晴光满目，福运常来"
]
COLORS = [
    "#ff2b2b",   # 鲜红
    "#ff9500",   # 橙
    "#ffdd00",   # 亮黄
    "#39ff14",   # 亮绿
    "#00d4ff",   # 青蓝
    "#0066ff",   # 宝蓝
    "#8c00ff",   # 紫
    "#ff3da6",   # 玫红
    "#ff5500",   # 橘红
    "#c9ff00",   # 黄绿
    "#00ffaa",   # 薄荷青
    "#2277ff",   # 天蓝
    "#b244ff",   # 浅紫
    "#ff2277",   # 艳粉
    "#00bbff"    # 浅湖蓝
]
#
# COLORS = ["#1e1e2e", "#2d3436", "#2b2d42", "#264653", "#3d405b",
#           "#6c5ce7", "#0b3d91", "#3b3b58", "#232946", "#1b1b2f",
#           "#2e1f27", "#22333b", "#3a0ca3", "#14213d", "#432818"]

TEXT_COLORS = ["#ffffff", "#222222", "#ffffff", "#222222", "#ffffff", "#222222"]


# TEXT_COLORS = ["#f1f1f1", "#e0e0e0", "#a8dadc", "#ffd166", "#c7f9cc", "#ffb4a2"]

SIZES = [(180, 110), (220, 140), (260, 160), (300, 190), (340, 210), (400, 240)]

OPACITIES = [0.55, 0.65, 0.75, 0.85, 0.95, 1.0]

LIFETIMES = [1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000]   # 毫秒

STYLES = ["normal", "frameless", "tool"]      # 普通 / 无边框 / 工具窗（不进任务栏）

class RainbowWindow(QWidget):
    def __init__(self, idx, _on_close):
        super().__init__()
        self.idx= idx
        self._on_close = _on_close

        #     属性随机设置
        title = random.choice(TITLES)
        content = random.choice(CONTENTS)
        bg = random.choice(COLORS)
        fg = random.choice(TEXT_COLORS)
        w,h = random.choice(SIZES)
        opacity = random.choice(OPACITIES)
        lifetime = random.choice(LIFETIMES)

        # 设置边框
        self.setWindowTitle(title)
        self.resize(w,h)
        self.setWindowOpacity(opacity)
        # 想要效果，不用
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.Tool)
        # self.setWindowFlags(Qt.WindowType.Tool)

    #     位置

        scr = QApplication.primaryScreen().availableGeometry()
        x = random.randint(scr.left(), max(scr.left(), scr.right() - w))
        y = random.randint(scr.top(), max(scr.top(), scr.bottom() - h))
        self.move(x,y)

        self.setStyleSheet(f"background-color: {bg};")

        # 文字设置
        # 设置布局
        layout = QVBoxLayout(self)
        # 设置内容边距
        layout.setContentsMargins(6,6,6,6)

        self.info = QLabel(content)
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setFont(QFont("Microsoft YaHei", 15))
        self.info.setStyleSheet(f"color: {fg}; background: transparent;")
        layout.addWidget(self.info)

        # 取消定时消失特性
        self._death = QTimer(self)
        self._death.setSingleShot(True)
        self._death.timeout.connect(self.close)
        self._death.start(lifetime)

        self.show()

    def set_compact(self, w=56, h=36):
        """爱心排列前把窗口统一缩成小卡片"""
        self.resize(w, h)
        self.info.setFont(QFont("Microsoft YaHei", 7))
        self.info.setWordWrap(True)

    def closeEvent(self, event):
        cb, self._on_close=self._on_close,None
        if cb:
            cb(self)
        super().closeEvent(event)

# 窗口生成器
class WindowFactory:
    SAFE_LIMIT = 80
    def __init__(self,interval=120):
        self._all_generated=False
        self.counter = 0
        self.spawned = 0
        self.windows = set()
        self.paused = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.spawn)
        self.timer.start(interval)

    def spawn(self):

        if self.paused:
            return
        if len(self.windows) >= self.SAFE_LIMIT:
            return
        w = RainbowWindow(self.counter, _on_close=self._on_window_closed)
        self.counter += 1
        self.spawned += 1
        self.windows.add(w)

    def _on_window_closed(self, w):
        self.windows.discard(w)
        w.deleteLater()



def main():
    app =QApplication(sys.argv)
    # win = RainbowWindow(1)
    w = WindowFactory(interval=80)
    sys.exit(app.exec())





if __name__ == "__main__":
    main()