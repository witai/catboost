#!/usr/bin/env python

import os.path

import numpy as np

import config
import experiment_lib

import xgboost as xgb


class XGBoostExperimentGridSearchCV(experiment_lib.ExperimentGridSearchCV):

    def __init__(self, **kwargs):
        super(XGBoostExperimentGridSearchCV, self).__init__(**kwargs)

    def get_estimator(self, cat_cols):
        return xgb.XGBRegressor(
            n_jobs=16
        )

    def get_param_grid(self):
        return {
            'n_estimators' : [int(v) for v in np.geomspace(100, 15000, 10)],
            'max_depth' : np.arange(1, 17),
            'learning_rate' : [v for v in np.geomspace(0.01, 1.0, 10)]
        }


if __name__ == "__main__":
    XGBoostExperimentGridSearchCV(
        train_path=os.path.join(config.preprocessed_dataset_path, 'train'),
        test_path=os.path.join(config.preprocessed_dataset_path, 'test'),
        cd_path=os.path.join(config.preprocessed_dataset_path, 'cd'),
        output_folder_path=os.path.join(config.training_output_path, 'XGBoostExperimentGridSearchCV'),
        header_in_data=False
    ).run()
