import math
import random
import sys

from PyQt6.QtCore import Qt, QTimer, QObject
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
# TEXT_COLORS = ["#f1f1f1", "#e0e0e0", "#a8dadc", "#ffd166", "#c7f9cc", "#ffb4a2"]
TEXT_COLORS = ["#ffffff", "#222222", "#ffffff", "#222222", "#ffffff", "#222222"]

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
        # self._death = QTimer(self)
        # self._death.setSingleShot(True)
        # self._death.timeout.connect(self.close)
        # self._death.start(lifetime)

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
class WindowFactory(QObject):
    
    SAFE_LIMIT = 80
    def __init__(self,interval=120):
        super().__init__()
        self._all_generated=False
        self._dissolving = False
        self.counter = 0
        self.spawned = 0
        self.windows = set()
        self.paused = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spawn)
        self.timer.start(interval)

    def spawn(self):
        if self.paused:
            return
        if self.spawned >= self.SAFE_LIMIT:
            self.timer.stop()
            self.change_shape()
            return
        w = RainbowWindow(self.counter, _on_close=self._on_window_closed)
        self.counter += 1
        self.spawned += 1
        self.windows.add(w)

    def _on_window_closed(self, w):
        self.windows.discard(w)
        w.deleteLater()
        if self._dissolving and len(self.windows) == 0:
            QApplication.quit()


    def change_shape(self):
        wins = list(self.windows)
        n = len(wins)
        if n == 0:
            return

        for w in wins:
            w.set_compact(56, 36)

        # 爱心采样->平均点集
        points = []
        for i in range(n):
            t = 2 * math.pi * i / n
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            points.append((x, y))

        # 采样点后,将x,y分为两个列表,求中点,
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        # 屏幕像素点对应,取屏幕中点
        scr = QApplication.primaryScreen().availableGeometry()
        scale = min(scr.width() * 0.75 / (max_x - min_x),
                    scr.height() * 0.75 / (max_y - min_y))
        cx, cy = scr.center().x(), scr.center().y()

        # 只算目标，不直接 move
        # 目标坐标转换

        self._targets = []
        for win, (px, py) in zip(wins, points):
            tx = cx + (px - mid_x) * scale - win.width() / 2
            ty = cy - (py - mid_y) * scale - win.height() / 2
            self._targets.append((win, int(tx), int(ty)))

        if not hasattr(self, "_anim"):
            self._anim = QTimer(self)  # 加 parent，且只建一次
            self._anim.timeout.connect(self._step)
        self._anim.start(20)

    def _step(self):
        done = True
        for win, tx, ty in self._targets:
            x, y = win.x(), win.y()
            dx, dy = tx - x, ty - y
            if dx or dy:
                done = False
                sx = int(dx * 0.18) or (1 if dx > 0 else -1)
                sy = int(dy * 0.18) or (1 if dy > 0 else -1)
                if abs(sx) > abs(dx): sx = dx  # 防越过
                if abs(sy) > abs(dy): sy = dy
                win.move(x + sx, y + sy)
        if done:
            self._anim.stop()
            self.on_heart_done()  # ← 爱心拼好后的回调

    def on_heart_done(self):
        self._dissolving =True
        for i, w in enumerate(list(self.windows)):
            t = QTimer(self)
            t.setSingleShot(True)
            t.timeout.connect(w.close)
            t.start(random.randint(0, 2000) + i * 8)


def main():
    app =QApplication(sys.argv)
    # win = RainbowWindow(1)
    w = WindowFactory(interval=80)
    sys.exit(app.exec())





if __name__ == "__main__":
    main()