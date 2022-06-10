from typing import Any
from functools import partial

from darts import models
import numpy as np
import numpy.typing as npt
import optuna

from one.models.predictive.darts_simple import SimpleDartsModel


class LightGBMModel(SimpleDartsModel):
    def __init__(
        self, window: int = 10, n_steps: int = 1, lags: int = 1, val_split: float = 0.2
    ):

        model_cls = models.LightGBMModel

        super().__init__(model_cls, window, n_steps, lags, val_split)

    def _model_objective(self, trial, train_data: npt.NDArray[Any]):
        params = {
            "lambda_l1": trial.suggest_loguniform("lambda_l1", 1e-8, 10.0),
            "lambda_l2": trial.suggest_loguniform("lambda_l2", 1e-8, 10.0),
            "num_leaves": trial.suggest_int("num_leaves", 2, 256),
            "feature_fraction": trial.suggest_uniform("feature_fraction", 0.4, 1.0),
            "bagging_fraction": trial.suggest_uniform("bagging_fraction", 0.4, 1.0),
            "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
            "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        }

        return self._get_hyperopt_res(params, train_data)
