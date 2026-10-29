import random
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont

# 进行窗口创建，无数窗口不断创建
# 可以用pyQt，感觉，然后每个窗口属性不一样（设置上数组存储随机挑选吧）
# 使用函数工厂类进行制造管理,执行产生次数

# 随机属性
TITLES = ["数据流", "监控", "日志", "矩阵", "节点", "终端", "信号", "缓存",
          "队列", "索引", "堆栈", "渲染", "采样", "通道", "脉冲", "熵"]

COLORS = ["#1e1e2e", "#2d3436", "#2b2d42", "#264653", "#3d405b",
          "#6c5ce7", "#0b3d91", "#3b3b58", "#232946", "#1b1b2f",
          "#2e1f27", "#22333b", "#3a0ca3", "#14213d", "#432818"]

TEXT_COLORS = ["#f1f1f1", "#e0e0e0", "#a8dadc", "#ffd166", "#c7f9cc", "#ffb4a2"]

SIZES = [(180, 110), (220, 140), (260, 160), (300, 190), (340, 210), (400, 240)]

OPACITIES = [0.55, 0.65, 0.75, 0.85, 0.95, 1.0]

LIFETIMES = [1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000]   # 毫秒

STYLES = ["normal", "frameless", "tool"]      # 普通 / 无边框 / 工具窗（不进任务栏）

# 简化书写
FRAMELESS = Qt.WindowType.FramelessWindowHint
TOOL = Qt.WindowType.Tool
STAYS_ON_TOP = Qt.WindowType.WindowStaysOnTopHint
ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
K_ESC, K_SPACE, K_UP, K_DOWN = (Qt.Key.Key_Escape, Qt.Key.Key_Space,
                                Qt.Key.Key_Up, Qt.Key.Key_Down)

# 窗口类
class RandomWindow(QWidget):
    def __init__(self,idx,on_close=None):
        super().__init__()
        # 进行编号
        self.idx = idx
        self._on_close = on_close
        # 随机选择属性
        title    = random.choice(TITLES)
        bg       = random.choice(COLORS)
        fg       = random.choice(TEXT_COLORS)
        w, h     = random.choice(SIZES)
        opacity  = random.choice(OPACITIES)
        lifetime = random.choice(LIFETIMES)
        style    = random.choice(STYLES)
#        进行属性配置
        self.setWindowTitle(f"{title}")
#         窗口属性
        # 边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.Tool)
        self.resize(w,h)
        self.setWindowOpacity(opacity)
        scr = QApplication.primaryScreen().availableGeometry()
        x = random.randint(scr.left(), max(scr.left(), scr.right() - w))
        y = random.randint(scr.top(), max(scr.top(), scr.bottom() - h))
        self.move(x, y)
        # 背景颜色
        self.setStyleSheet(f"background-color: {bg};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6,6,6,6)
        info = QLabel(f"#{idx}  {title}\n"
                      f"{w}×{h}  α={opacity:.2f}\n"
                      f"{style}\n"
                      f"T-{lifetime}ms"
                      )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setFont(QFont("Consolas",9))
        info.setStyleSheet(f"color: {fg}; background: transparent;")
        layout.addWidget(info)
#         随即寿命
        self._death = QTimer(self)
        self._death.setSingleShot(True)
        self._death.timeout.connect(self.close)
        self._death.start(lifetime)
        self.show()
    def closeEvent(self, event):
        cb, self._on_close = self._on_close, None
        if cb:
            cb(self)
        super().closeEvent(event)

class WindowFactory:
    SAFE_LIMIT = 150
    def __init__(self,interval = 120):
        self.counter = 0
        self.spawned = 0
        self.windows = set()
        self.paused = False
        self.timer= QTimer()
        self.timer.timeout.connect(self.spawn)
        self.timer.start(interval)

    def spawn(self):
        if self.paused or len(self.windows) >= self.SAFE_LIMIT:
            return
        w = RandomWindow(self.counter, on_close=self._on_window_closed)
        self.counter += 1
        self.spawned += 1
        self.windows.add(w)

    def _on_window_closed(self, w):
        self.windows.discard(w)  # 从集合移除 → 引用计数归零
        w.deleteLater()


def main():
    # 循环构建窗口
    app = QApplication(sys.argv)
    factory = WindowFactory(120)
    sys.exit(app.exec())
    pass

if __name__ == "__main__":
    main()