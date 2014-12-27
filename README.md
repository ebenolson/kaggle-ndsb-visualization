kaggle-ndsb-visualization
=========================
This is a collection of scripts for visualizing plankton images from the [Kaggle National Data Science Bowl](http://www.kaggle.com/c/datasciencebowl) competition. Images within each training class are compiled into a single mosaic image, and a bubble plot is created which groups mosaics according to the provided taxonomy. Due to the large size of this image it is saved as a tile pyramid which can be viewed with the included [Polymaps](http://polymaps.org/ex/) viewer.
### Dependencies
These scripts require `numpy`, `scipy`, `PIL` and `matplotlib`. Executing `machine_setup.sh` on a fresh Ubuntu 14.04 installation will install all necessary packages.

### Data Preparation
Clone this repository into a directory adjecent to your data directory, containing the training images in `data/train`.
```
.
├── data
│   └── train
└── visualization
```

### Usage
1. `python make_mosaics.py` will generate mosaic images in the `mosaics` subdirectory. 
2. `python make_bubbleplot.py` will generate the bubbleplot and write tile images into the `pyramid` subdirectory.
3. After generation, the bubble plot can be viewed by opening the file `viewer/index.html` in a web browser.

### System Requirements
Memory usage is currently very unoptimized, and at least 16GB of RAM is required to render the bubble plot. Use of an Amazon EC2 `m3.2xlarge` instance is recommended. Numpy `memmap` can be used to reduce this, but computation time is greatly increased. Mosaic creation (`make_mosaics.py`) is much less memory intensive.

### Screenshots
[Zoomed out completely](http://i.imgur.com/VDO7Ilp.png)
[Single mosaic](http://i.imgur.com/C5nFvzM.png)
[Zooming in on one group](http://i.imgur.com/brizfzs.png)