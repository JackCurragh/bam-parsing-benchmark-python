# bam-parsing-benchmark-python
Experiments in parsing Binary Alignment Maps (BAMs) in python 



## Setup 

Clone this repo and `cd` into it. Then:
```
python -m pip install -r requirements.txt
```

## Run
```
richbench benchmarks --profile --percentage --markdown
```


## Results
|                      Benchmark | Min     | Max     | Mean    | Min (+)         | Max (+)         | Mean (+)        |
|--------------------------------|---------|---------|---------|-----------------|-----------------|-----------------|
| Pysam: Dictionary vs DataFrame | 5.081   | 5.335   | 5.149   | 14.327 (-2.8x)  | 14.626 (-2.7x)  | 14.506 (-2.8x)  |
|     Pysam: Dictionary vs Numpy | 5.084   | 5.394   | 5.195   | 17.499 (-3.4x)  | 17.832 (-3.3x)  | 17.649 (-3.4x)  |
|      Pysam: DataFrame vs Numpy | 14.701  | 15.205  | 14.867  | 17.728 (-1.2x)  | 18.261 (-1.2x)  | 17.976 (-1.2x)  |
|  HTSeq Dictionary vs DataFrame | 39.958  | 42.405  | 41.281  | 43.567 (-1.1x)  | 45.721 (-1.1x)  | 44.403 (-1.1x)  |
|      HTSeq Dictionary vs Numpy | 40.534  | 41.164  | 40.849  | 41.439 (-1.0x)  | 42.869 (-1.0x)  | 42.214 (-1.0x)  |
|       HTSeq DataFrame vs Numpy | 43.169  | 48.133  | 45.265  | 40.646 (1.1x)   | 41.115 (1.2x)   | 40.828 (1.1x)   |
|     Dictionary: Pysam vs HTSeq | 5.130   | 5.245   | 5.164   | 40.354 (-7.9x)  | 42.809 (-8.2x)  | 41.764 (-8.1x)  |
|      DataFrame: Pysam vs HTSeq | 14.856  | 15.407  | 15.112  | 42.213 (-2.8x)  | 43.868 (-2.8x)  | 43.201 (-2.9x)  |
|          Numpy: Pysam vs HTSeq | 17.766  | 18.060  | 17.903  | 41.290 (-2.3x)  | 41.913 (-2.3x)  | 41.524 (-2.3x)  |