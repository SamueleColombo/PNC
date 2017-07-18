# Proposal for PhysioNet/Computing in Cardiology Challenge 2017
A modest proposal for the PhysioNet/Computing in Cardiology Challenge 2017 using deep learning techniques.

## Introduction
The 2017 PhysioNet/CinC Challenge aims to encourage the development of algorithms to classify, from a single short ECG lead recording (between 30 s and 60 s in length), whether the recording shows normal sinus rhythm, atrial fibrillation (AF), an alternative rhythm, or is too noisy to be classified.

# Data
It's not required to download any data, but if you want try to extract new features or rebuild the `train.csv` and `eval.csv` files, you need to download the original PhysioNet data using this command:
```
wget -r --no-parent https://physionet.org/physiobank/database/challenge/2017/training/
```

## Single Node Training
There are several ways to run this code and it supports both local environment and cloud ones.

The basic configuration files are in the `PNC-configs` directory, where each `.cfg` file contains the default arguments to feed the training task. You can override the arguments just write them in the command line.
More information about the arguments can be found in the configuration page.
```
export CONFIG_FILE=PNC-configs/config.cfg
```

### Using local python
Run the code on your local machine:
```
python pnc --config $CONFIG_FILE
```


### Using gcloud local
Run the code on a local gloud instance.
```
gloud ml-engine local train --package-path pnc \
                            --module-name pnc \
                            -- \
                            --config $CONFIG_FILE
```


### Using Cloud ML Engine
Run the code on the Google Cloud ML Engine.
```
export JOB_NAME=pnc
```

```
gloud ml-engine jobs submit $JOB_NAME \
                            --stream-logs \
                            --runtime-version 1.2 \
                            --job-dir $GCS_JOB_DIR
                            --package-path pnc \
                            --module-name pnc \
                            --region europe_west1 \
                            -- \
                            --config $CONFIG_FILE
```

## References
> [1] Clifford GD, Liu CY, Moody B, Lehman L, Silva I, Li Q, Johnson AEW, Mark RG. AF classification from a short single lead ECG recording: The Physionet Computing in Cardiology Challenge 2017. Computing in Cardiology, 2017.