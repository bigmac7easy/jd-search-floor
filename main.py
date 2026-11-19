from qgis.PyQt.QtWidgets import QAction, QSpinBox, QLabel
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import QgsProject, QgsVectorLayer


class JDSearchFloor:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):

        # 1. 전용 툴바 생성
        self.toolbar = self.iface.addToolBar("JD 층조회")
        self.toolbar.setObjectName("JDSearchFloorToolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)

        # 2. 층수 입력창 생성
        self.spinbox = QSpinBox()
        self.spinbox.setRange(-20, 200)
        self.spinbox.setValue(0)
        self.spinbox.setSuffix("층")
        self.spinbox.setKeyboardTracking(False)

        self.toolbar.addWidget(QLabel("JD 층조회: "))
        self.toolbar.addWidget(self.spinbox)

        # 3. 버튼 생성
        self.up_action = QAction("▲ UP", self.toolbar)
        self.down_action = QAction("▼ DOWN", self.toolbar)
        self.reset_action = QAction("초기화", self.toolbar)

        # 4. 이벤트 연결
        self.up_action.triggered.connect(self.up)
        self.down_action.triggered.connect(self.down)
        self.reset_action.triggered.connect(self.reset)

        # 5. 툴바에 버튼 등록
        self.toolbar.addAction(self.up_action)
        self.toolbar.addAction(self.down_action)
        self.toolbar.addAction(self.reset_action)

        # 6. 플러그인 메뉴 등록
        self.iface.addPluginToMenu("JD Search Floor", self.up_action)
        self.iface.addPluginToMenu("JD Search Floor", self.down_action)
        self.iface.addPluginToMenu("JD Search Floor", self.reset_action)

        # 7. 현재 조회 상태 표시
        self.status = QLabel("미조회")
        self.toolbar.addWidget(self.status)

        # 8. 층수 변경 이벤트 연결
        self.spinbox.valueChanged.connect(self.run)

    def up(self):
        self.spinbox.setValue(self.spinbox.value() + 1)

    def down(self):
        self.spinbox.setValue(self.spinbox.value() - 1)

    def reset(self):
        if self.spinbox.value() == 0:
            self.run(0)
        else:
            self.spinbox.setValue(0)

    def run(self, floor):

        layers = QgsProject.instance().mapLayers().values()

        for layer in layers:

            if not isinstance(layer, QgsVectorLayer):
                continue

            if "FLR_NO" not in layer.fields().names():
                continue

            if floor == 0:
                query = ""
            else:
                field = layer.fields()["FLR_NO"]

                if field.type() == QVariant.String:
                    query = f"FLR_NO = '{floor}'"
                else:
                    query = f"FLR_NO = {floor}"

            layer.setSubsetString(query)

        # 조회 상태 갱신
        if floor == 0:
            self.status.setText("전체 층")
        else:
            self.status.setText(f"조회: {floor}층")

        self.iface.mapCanvas().refresh()

    def unload(self):

        # 플러그인 메뉴 제거
        self.iface.removePluginMenu("JD Search Floor", self.up_action)
        self.iface.removePluginMenu("JD Search Floor", self.down_action)
        self.iface.removePluginMenu("JD Search Floor", self.reset_action)

        # 전용 툴바 제거
        self.iface.mainWindow().removeToolBar(self.toolbar)
        self.toolbar.deleteLater()