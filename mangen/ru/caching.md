# Кэширование и ленивые объекты.

Особенностью скриптового cad является необходимость перезапуска скрипта генерации геометрии при каждом обновлении модели. С ростом размера модели это приводит к значительному росту времени, требующегося на отрисовку геометрии. С целью решения этой проблемы вычислительно ёмкие операции ZenCad закешированы и ленифицированы силами библиотеки [evalcache](https://github.com/mirmik/evalcache). 

Вместо непосредственного расчета, evalcache строит дерево построения модели на основе хэшключей генерируемых объектов. Библиотека сохраняет в кэше на жестком диске все произведенные вычисления и в случае, если объект уже был расчитан ранее, достаёт его из кэша. evalcache отслеживает изменения параметров в дереве модели и на лету обновляет переставшие быть актуальными объекты вычисления.

Для отображения информации о том, как evalcache работает с данными можно активировать диагностический вывод:
```python
zencad.lazy.diag=True
```

Так как evalcache выполняет вычисления только в момент, когда объект в действительности запрошен, а не тогда, когда он объявлен, могут возникать проблемы с пониманием точки возникновения возможной ошибки.

В этом случае полезной может быть опция:
```python
zencad.lazy.fastdo=True
```
При активации этой опции evalcache будет производить вычисления непосредственно в момент объявления объекта.
