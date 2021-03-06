#!/usr/bin/env python3 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import zencad.settings

class TableField(QWidget):
	def __init__(self, ltext, wdg, llen=150):
		super().__init__()
		self.label = QLabel(ltext)
		self.label.setFixedWidth(llen)
		self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.wdg = wdg
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.wdg)
		self.setLayout(self.layout)

		self.layout.setContentsMargins(0,0,0,0)
		self.layout.setSpacing(5)
		left, top, right, bottom = self.layout.getContentsMargins()
		spacing = self.layout.spacing()
		#self.setFixedWidth(llen + self.wdg.width() + right + spacing)

	def restore(self):
		pass

class TextFieldChanger(QWidget):
	def __init__(self, label, path, length=200):
		super().__init__()
		self.path=path
		self.layout = QHBoxLayout()
		self.layout.addWidget(QLabel(label))
		self.edit = QLineEdit()
		self.edit.setFixedWidth(length)
		self.edit.setText(str(zencad.settings.get(path)))
		self.layout.addWidget(self.edit)
		self.setLayout(self.layout)

	def apply(self):
		zencad.settings.set(self.path, self.edit.text())

	def restore(self):
		pass

class Checker(QWidget):
	def __init__(self, label, path):
		super().__init__()
		self.path=path
		self.layout = QHBoxLayout()
		self.layout.addWidget(QLabel(label))
		self.check = QCheckBox()
		self.layout.addWidget(self.check) 
		self.setLayout(self.layout)

	def apply(self):
		#zencad.settings.start_screen(self.check.checkState() == 0)
		zencad.settings.set(self.path, self.check.checkState() != 0)

	def restore(self):
		self.check.setCheckState(2 if zencad.settings.get(self.path)=="true" else 0)

class ColorChanger(QWidget):
	def __init__(self):
		super().__init__()
		values = zencad.settings.Settings.get_default_color()

		self.defbutton = QPushButton("Mech")
		self.defbutton.clicked.connect(self.set_default)

		labels = "RGBA"
		self.edits = [ QLineEdit() for i in range(4) ]
		for e in self.edits: e.setFixedWidth(30)

		self.layout = QHBoxLayout()
		for i in range(4):
			self.edits[i].setText(str(values[i]))
			self.layout.addWidget(TableField(ltext=labels[i], wdg=self.edits[i], llen=30))

		self.layout.addStretch()
		self.layout.addWidget(self.defbutton)

		self.layout.setContentsMargins(0,0,0,0)
		self.layout.addWidget(QWidget())
		self.setLayout(self.layout)

	def restore(self):
		pass

	def apply(self):

		values = tuple([ float(e.text()) for e in self.edits ])
		if values != zencad.settings.get_default_color():
			print("You should reevaluate script for color applying")
		values = zencad.settings.Settings.set_default_color(*values)

	def set_default(self):
		self.edits[0].setText(str(round(zencad.color.mech.r, 5)))
		self.edits[1].setText(str(round(zencad.color.mech.g, 5)))
		self.edits[2].setText(str(round(zencad.color.mech.b, 5)))
		self.edits[3].setText(str(round(zencad.color.mech.a, 5)))

class SettingsWidget(QDialog):
	"""Виджет настроек системы"""

	def __init__(self):
		super().__init__()

		settings = zencad.settings.Settings()
		zencad.settings.restore()

		self.ok_button = QPushButton("Ok")
		self.cancel_button = QPushButton("Cancel")
		self.hlayout = QHBoxLayout()
		self.hlayout.addWidget(self.ok_button)
		self.hlayout.addWidget(self.cancel_button)

		self.default_color_edit = ColorChanger()
		self.texteditor_edit = TextFieldChanger(path=["gui", "text_editor"], label="Text editor command:")
		self.not_start_widget = Checker("Показывать стартовый экран", path=["gui", "start_widget"])
		self.bind_widget = Checker("Линковать виджет", path=["gui", "bind_widget"])
		self.marker_size_edit = TextFieldChanger(path=["markers", "size"], label="Marker size:")
		
		self.appliers = []
		self.vlayout = QVBoxLayout()
		
		def append(obj):
			self.appliers.append(obj)
			self.vlayout.addWidget(obj)

		append(self.texteditor_edit)
		append(self.default_color_edit)
		append(self.not_start_widget)
		append(self.bind_widget)
		append(self.marker_size_edit)

		self.vlayout.addLayout(self.hlayout)

		for a in self.appliers:
			a.restore()

		self.ok_button.clicked.connect(self.ok_handle)
		self.cancel_button.clicked.connect(self.cancel_handle)

		self.setLayout(self.vlayout)

	def save_all(self):
		for a in self.appliers:
			a.apply()
		zencad.settings.store()

	def ok_handle(self):
		self.save_all()
		self.accept()

	def cancel_handle(self):
		self.reject()

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv[1:])
	wdg = SettingsWidget()
	wdg.exec()


