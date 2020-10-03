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
"""These nodes exist to preprocess the data in to a format that is more
suited for our modelling algos
"""

from typing import Any, Dict, List

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import numpy as np


def _last(vals):
    return vals[-1]


def split_data(data: pd.DataFrame, example_test_data_ratio: float) -> Dict[str, Any]:
    """Node for splitting the classical Iris data set into training and test
    sets, each split into features and labels.
    The split ratio parameter is taken from conf/project/parameters.yml.
    The data and the parameters will be loaded and provided to your function
    automatically when the pipeline is executed and it is time to run this node.
    """
    #     data.columns = [
    #         "sepal_length",
    #         "sepal_width",
    #         "petal_length",
    #         "petal_width",
    #         "target",
    #     ]
    #     classes = sorted(data["target"].unique())
    #     # One-hot encoding for the target variable
    #     data = pd.get_dummies(data, columns=["target"], prefix="", prefix_sep="")

    #     # Shuffle all the data
    #     data = data.sample(frac=1).reset_index(drop=True)

    #     # Split to training and testing data
    #     n = data.shape[0]
    #     n_test = int(n * example_test_data_ratio)
    #     training_data = data.iloc[n_test:, :].reset_index(drop=True)
    #     test_data = data.iloc[:n_test, :].reset_index(drop=True)

    #     # Split the data to features and labels
    #     train_data_x = training_data.loc[:, "sepal_length":"petal_width"]
    #     train_data_y = training_data[classes]
    #     test_data_x = test_data.loc[:, "sepal_length":"petal_width"]
    #     test_data_y = test_data[classes]

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    l_encoder = LabelEncoder()
    y = l_encoder.fit_transform(y)
    train_data_x, test_data_x, train_data_y, test_data_y = train_test_split(
        X, y, test_size=example_test_data_ratio, random_state=42
    )

    # When returning many variables, it is a good practice to give them names:
    return dict(
        train_x=train_data_x,
        train_y=train_data_y,
        test_x=test_data_x,
        test_y=test_data_y,
    )


def exp_weight_wig_data(df: pd.DataFrame) -> pd.DataFrame:
    df["exp_val"] = 10 / np.abs(2020 - df["year"])
    df["vae"] = df["vae"] * df["exp_val"]
    df["pve"] = df["pve"] * df["exp_val"]
    df["gee"] = df["gee"] * df["exp_val"]
    df["rqe"] = df["rqe"] * df["exp_val"]
    df["rle"] = df["rle"] * df["exp_val"]
    df["cce"] = df["cce"] * df["exp_val"]
    ret_df = (
        df.groupby(["code", "countryname"])
        .agg(
            {
                "vae": "sum",
                "pve": "sum",
                "gee": "sum",
                "rqe": "sum",
                "rle": "sum",
                "cce": "sum",
            }
        )
        .reset_index()
    )
    ret_df["country"] = ret_df.countryname.str.lower()
    # print(ret_df)
    return ret_df


def aggregate_excess_deaths(df: pd.DataFrame) -> pd.DataFrame:
    ret_df = (
        df.sort_values("week")
        .groupby("country")
        .agg(
            {
                "population": "last",
                "week": "last",
                "year": "last",
                "total_deaths": "sum",
                "covid_deaths": "sum",
                "expected_deaths": "sum",
                "excess_deaths": "sum",
                "non_covid_deaths": "sum",
                "covid_deaths_per_100k": "sum",
                "excess_deaths_per_100k": "sum",
                # "excess_deaths_pct_change": "sum""
            }
        )
        .reset_index()
    )
    return ret_df


def combine_data_sets(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return df1.merge(df2)


def pca_wig_data(df: pd.DataFrame):
    """
    This fits and transforms our data using PCA. 
    eda in jupyter suggests that we only need 1 compenent
    """
    pca = PCA()
    vals = pca.fit_transform(df.iloc[:, 2:-1])
    # print(pca.components_)
    return pd.DataFrame(
        {"country": df["country"], "govt_trust_index": vals[:, 0] * (-1)}
    )
