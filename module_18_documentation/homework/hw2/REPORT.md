## Результаты испытаний

| Обозначение | Описание                          |
|-------------|-----------------------------------|
| -O          | Без дополнительной настройки      |
| +O          | С дополнительной настройкой       |
| -S          | Без использования сессии          |
| +S          | С использованием сессии           |
| -T          | Без использования многопоточности |
| +T          | С использованием многопоточности  |

```text
+----------------+-------------------------------------------+---------------------------------------------+
| Число запросов |                     -O                    |                      +O                     |
|                +---------------------+---------------------+---------------------+-----------------------+
|                |          -S         |          +S         |          -S         |           +S          |
|                +----------+----------+----------+----------+----------+----------+-----------+-----------+
|                |    -T    |    +T    |    -T    |    +T    |    -T    |    +T    |     -T    |     +T    |
+----------------+----------+----------+----------+----------+----------+----------+-----------+-----------+
|      10        |0.05437   |0.00181   |0.04082   |0.00143   |0.03913   |0.00143   |0.0345     |0.00136    |
+----------------+----------+----------+----------+----------+----------+----------+-----------+-----------+ 
|      100       |0.49329   |0.00473   |0.38912   |0.00435   |0.4812    |0.00457   |0.42973    |0.00546    |
+----------------+----------+----------+----------+----------+----------+----------+-----------+-----------+
|      1000      |4.39287   |0.01959   |3.95117   |0.01604   |4.29028   |0.018     |3.80071    |0.0147     |
+----------------+----------+----------+----------+----------+----------+----------+-----------+-----------+
```