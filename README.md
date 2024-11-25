# Ассемблер и интерпретатор для учебной виртуальной машины
## Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт

### Поддерживаемый синтаксис
```
LOAD_CONST <value>
LOAD_MEM <address>
STORE_MEM <address>
BINARY_OP ==
```
### Запуск программы
```
На вход принимает файл с командами

python assembler.py input_file output_file log_file
python interpreter.py binary_file result_file memory_range
```

### Клонирование
```
git clone https://github.com/Avinar16/Asembler
cd <директория проекта>
```
### Создание виртуального окружения python
```
python -m venv venv
venv/Scripts/activate
```

### Тестирование:
    python tests.py
