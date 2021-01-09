<p align="center">
  <img width="236" height="220" src="https://i.imgur.com/bQ4E4m8.png">
</p>


AIDA
===================

AIDA (Aerial Imagery Downloader and Analyzer) is a simple to use tool to download aerial imagery of big regions. It works by first downloading larger aerial images which are to large for details, but ok to see if the image is useable or not. When the download of all large images is complete, the tool analyzes the images using a trained machine learning model. The model provided by the tool only checks if the image is nature or not. The image is discarded if it is nature, but kept if not. Then all images who are not nature are indexed and will be downloaded in the final size. Using this method it reduces the amount of images by 80% to 90%.




Install
---

To install AIDA, you have two options. You can either use the installer or run AIDA from the source code with python.

### Install from installer (recommended)

Step 1: Download the installer from here:
https://drive.google.com/file/d/1mvioDhkEoElOuLM0JHOHpGLhUjoL2m1d/view?usp=sharing

Step 2: Install the AIDA

Step 3: Add the main folder of AIDA to your environment path variable.



### Run source with python

Prerequisites:

- Python 3.8.5
- Tensorflow 2.3.1
- CUDA 10.1 (for GPU support)
- GDAL

After you downloaded the source code from Github you can run AIDA as follows:

```bash
python aida.py 
```



## Usage

To use AIDA you need to create a config file.

### Config
Create a `config.yml` specifying your setup like this:

```yaml
service:
  version: 1.1.1
  url: https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?
  srs: EPSG:28992
  format: jpeg
  transparent: false
  layer: 2019_ortho25

bbox:
  west: 201763.0000
  south: 500353.0000
  east: 205310.0000
  north: 504609.0000

image:
  tempsize: 600
  size: 200
  resolution: 600
  directory: C:\DIRECTORY\TO\STORE\IMAGES
  projection: EPSG:28992

analyzer:
  modelpath: C:\Program Files (x86)\AIDA\model4

timeout: 300
bandscount: 3
tmpdirectory: ./tmp
threads: 6
```



**Service:**
Describes the used WMS service.

| Setting     | Value                                                        |
| ----------- | ------------------------------------------------------------ |
| version     | The version of the WMS service. This version of AIDA does not support v1.3.0 or higher. |
| url         | The URL of the WMS service                                   |
| srs         | The Coordinate Systems used by the WMS service. **EPSG:28992 strongly recommend** |
| format      | The format of the image produces                             |
| transparant | If Transpartent or not                                       |
| layer       | The Layer of the WMS service                                 |

**Bbox:**
The bbox is the bounding box for the map you want to retrieve. Best is to use the EPSG:28992 coordinate system for retrieving images form The Netherlands. For images outside the Netherlands use a coordinate system where each digit equals one meter. To find the bbox you can use http://bboxfinder.com/. You can set the coordinate system to EPSG:28992 and create a bbox of the area you want to download the images of.

| Setting | Value                |
| ------- | -------------------- |
| west    | The west coordinate  |
| south   | The south coordinate |
| east    | The east coordinate  |
| north   | The north coordinate |

**Image:**
Settings for downloading the images.

| Setting    | Value                                                        |
| ---------- | ------------------------------------------------------------ |
| tempsize   | The temporally size of the images. This size must be larger then the final size and must be dividable by `size`. For example: A tempsize of 800 and a size of 200 is ok. They are dividable. A tempsize of 500 and a size of 200 is not ok. The measurement is in whole meters. |
| size       | The final size the images should be downloaded at. A size of 200 means it is 200 meters by 200 meters. |
| resolution | The resolution is the pixel dimension of an individual image |
| directory  | The directory where the downloaded images are stored         |
| projection | The projection to which the images are projected to when downloaded from the WMS service. In this version of AIDA, you can **only** use EPSG:28992 |

**Other:**
All other settings

| Setting      | Value                                                        |
| ------------ | ------------------------------------------------------------ |
| modelpath    | The path where the tensorflow model is stored. The provided model is called `model4` and is stored in the root directory of AIDA. |
| timeout      | The timeout for downloading the images                       |
| bandscount   | Bandscount for the images                                    |
| tmpdirectory | The directory where all temporarily files are stored. When AIDA is finished, the directory will be wiped. |
| threads      | Number of threads the tool can utilize to download the images. The more threads you allocate, the faster the tool can download, because it downloads them simultaneously. For a 4 core CPU 6 threads is recommended, for a 8 core CPU 12 threads in recommended. |



### Run

Then run the tool with `config.yml` as an argument:

```bash
aida config.yml
```



## Help

```bash
usage: AIDA [-h] [--version] [-v] config

Download and analyze arial imagery.

positional arguments:
  config         imports a configuration file

optional arguments:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
  -v, --verbose  run progam in verbose mode
```

If you run in to problems you can run the program in verbose mode with the `-v` flag. You can also look in `debug.log` or `gdal.error.log`.



## Note:

In this version of AIDA you may see the following warning while the tool is analyzing images:

> AutoGraph could not transform <function Model.make_predict_function.<locals>.predict_function at 0x000002D461F17820> and will run it as-is.
> Please report this to the TensorFlow team. When filing the bug, set the verbosity to 10 (on Linux, export AUTOGRAPH_VERBOSITY=10) and attach the full output.
> Cause: Unable to locate the source code of <function Model.make_predict_function.<locals>.predict_function at 0x000002D461F17820>. Note that functions defined in certain environments, like the interactive Python shell do not expose their source code. If that is the case, you should to define them in a .py source file. If you are certain the code is graph-compatible, wrap the call using @tf.autograph.do_not_convert. Original error: could not get source code
> To silence this warning, decorate the function with @tf.autograph.experimental.do_not_convert

You can safely ignore this warning.