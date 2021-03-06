# Интерактивный объект

Интерактивный объект - есть единица отображения стандартного визуализатора zencad.

В этом разделе перечислены типы интерактивных объектов и указаны методы соответствующего базового класса.

----------------------------------------------
## Геометрические интерактивные объекты.
Механизм интерактивных объектов используется для отображения геометрических форм, обрабатываемых zencad.

Пример 1 (Создание интерактивного объекта формы):
```python3
model = zencad.box(10)
scn = zencad.scene()

intobj = zencad.interactive_object(model) 
scn.add(intobj)

zencad.show(scn)
```

Пример 2 (Создание интерактивного объекта формы с помощью функции отображения disp):
```python3
model = zencad.box(10)

intobj = zencad.disp(model)
intobj.set_color(zencad.color.yellow)
```

---------------------------------------
## Графические интерактивные объекты.
Помимо интерактивных объектов геометрических форм существуют интерактивные объекты, которые могут использоваться для передачи дополненительной информации на рабочей сцене:

### Стрелка:
```python3
arrow(pnt, vec, clr=zencad.color.white, arrlen=5, width=1, scene=zencad.default_scene)
```
Отобразить стрелку, соответствующую вектору _vec_, ведущему из точки _pnt_, размер головы стрелки определяется параметром _arrlen_, толщина линии параметром _width_.
Если параметр scene не None, объект сразу добавляется в scene.

### Линия:
```python3
line(apnt, bpnt, clr=zencad.color.white, width=1, scene=zencad.default_scene)
```
Отобразить линию, между точками _apnt_ и _bpnt_, толщина линии параметром _width_.
Если параметр scene не None, объект сразу добавляется в scene.

----------------------------------
## Методы класса interactive_object:

### Переразмещение  
```python3
relocate(trans)
```
Переразмещает объект в положение _trans_ относительно исходного расположения. 

### Скрытие
```python3
hide(en=True/False)
```
Скрыть или же вновь отобразить объект. Скрытый объект не удаляется из памяти.

### Установка цвета
```python3
set_color(color)

# Examples:
# RGB:
intobj.set_color((0.2,0.3,0.6))
intobj.set_color(zencad.color(0.2,0.3,0.6))

# RGBA:
intobj.set_color((0.2,0.3,0.6,0.5))
intobj.set_color(zencad.color(0.2,0.3,0.6,0.5))
```
Изменить цвет интерактивного объекта. 
Параметр color представляет или кортеж или объект zencad.color.
