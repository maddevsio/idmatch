# ID card templates

Each id card template must have:
- Preprocessing file (preprocessing.py)
- Processing file (processing.py)
- Data maping file (data_map.py)


## Preprocessing file
Содержит в себе действия для подготовки изображения к OCR.
Не содержит логики, только вызывает логику из core.preprocessing.*
Функционал контирбьютится в core.preprocessing и имеет обобщенную реализацию