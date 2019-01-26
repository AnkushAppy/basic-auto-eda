# basic-auto-eda
Basic Exploratory data analysis on a dataset. 

### Steps to run code

#### Clone repo

```bash
git clone https://github.com/AnkushAppy/basic-auto-eda.git
cd basic-auto-eda
```

#### Install requirement 
use virtualenv
```bash
virtualenv venv
. venv/bin/activate
```

install requirement
```bash
pip install -r requirements.txt
```

#### Run
Add a csv file to data folder.
Make necessary changes in settings.py file like :
    
* FILE_NAME: dataset name which you added in data folder
* REPORT_FILE_NAME: name of report you want
  
If done, run summerieser file  
```python
python code/summerieser.py
```

It will generate a folder with name same as report name inside report folder. 
It will contain png files and one md file. 
Open md file in some editor where you can see preview.


### TO-DO
* timedate capability
* numerical target enhancement
* other charts 
* deatailed analysis
* impact chart
