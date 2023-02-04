# hair-colorizing
Application to recolor hair with chosen color

### Key words:
Computer vision, convolutional neural networks, UNet, image processing

### Stack:
Python, Keras, OpenCV


### Описание
Данный проект демонстрирует прототип систевы распознавнания маски волос по фотографии/кдра из видеопоток и перекраске их в выбранный цвет с учетом изначального оттенка волос.

Для нахождения области волос на изображении за основу была взята обученная сеть DeeplabV3plus из репозитория https://github.com/digital-nomad-cheng/Hair_Segmentation_Keras

Для запуска использовать скрипт main_color_invertor.py. 

Примеры запуска скрипта:
main_color_invertor.py -t video -c ginger - запуск распознавания из видеопотока от вебкамеры (ключ -t video) и перекраски волос в рыжий оттенок (-c ginger)
или
main_color_invertor.py -t image -i Img_01.png -c ginger - запуск распознавания на отдельном изображении (ключ -t image и -i Img_01.png - путь к файлу изображения)  и перекраски волос в рыжий оттенок (-c ginger)

В качестве цветов для перекраски волос доступны:
- blonde
- ginger
- brunette
- purple
- red

Примеры работы:

Red coloring

<img src="/Examples/Img_01.png" width="300" height="200">   <img src="/Examples/Img_01_red.png" width="300" height="200">


Brunette coloring

<img src="/Examples/Img_02.png" width="250" height="250">   <img src="/Examples/Img_02_brunette.png" width="250" height="250">


Purple coloring

<img src="/Examples/Img_03.png" width="250" height="250">   <img src="/Examples/Img_03_purple.png" width="250" height="250">


Ginger coloring

<img src="/Examples/Img_04.png" width="250" height="250">   <img src="/Examples/Img_04_ginger.jpg" width="250" height="250">
