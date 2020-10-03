# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Nodes which model data and produce predicitons
"""
# pylint: disable=invalid-name

# import logging
# from typing import Any, Dict

# import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# import matplotlib.pyplot as plt


def train_rf(X, y):
    """Wrapper which trains a random forest model with X,y
    """
    rf = RandomForestClassifier()
    rf.fit(X, y)
    return rf


def train_LinReg(df: pd.DataFrame, formula: str):
    "trains a stats_model linear_regression!"
    y, X = dmatrices(formula, data=df, return_type="dataframe")
    mod = sm.OLS(y, X)
    return mod.fit()


def predict_model(model, X):
    """Generic model.predict wrapper for sklearn/sklearn compatible model apis
    """
    df = pd.DataFrame(model.predict(X))
    # df.to_csv("test.csv")
    # print(df)
    return df


def report_accuracy(preds, y_test):
    """Outputs sklearn classificaition report to console
    """
    print(classification_report(y_test, preds))


def train_lr(X, y):
    """Wrapper which trains a logisitc regression model with X,y
    """
    lr = LogisticRegression()
    return lr.fit(X, y)


def stats_model_summary(model, regressor_no):
    """
    prints summary output for linear model
    """
    summary_string = model.summary()
    qq_plot = sm.qqplot(model.resid, line="45")
    # plt.show()
    reg_fit = sm.graphics.plot_fit(model, regressor_no, vlines=True)
    return [summary_string.as_text(), qq_plot, reg_fit]
