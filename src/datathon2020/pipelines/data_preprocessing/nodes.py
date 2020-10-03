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

from typing import Any, List

import numpy as np
import pandas as pd

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA


def _last(vals):
    return vals[-1]


def exp_weight_wig_data(df: pd.DataFrame) -> pd.DataFrame:
    """Applies exponential weighting to wig data
    -> we want to focus on people's confidance in govt going in into the pandemic,
    not nessciarly thier long term notions
    """
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
    """Aggregates Excess deaths to sum time series data
    List of aggregations:

                "population": "last",
                "week": "last",
                "year": "last",
                "total_deaths": "sum",
                "covid_deaths": "sum",
                "expected_deaths": "sum",
                "excess_deaths": "sum",
                "non_covid_deaths": "sum",
                "covid_deaths_per_100k": "sum",
                "excess_deaths_per_100k": "sum"
    """
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


def naive_combine_data_sets(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """just a wrapper for df1.merge(df2)
    """
    return df1.merge(df2)


def pca_wig_data(df: pd.DataFrame) -> List[Any]:
    """
    This fits and transforms our data using PCA.
    eda in jupyter suggests that we only need 1 compenent
    """
    pca = PCA()
    vals = pca.fit_transform(df.iloc[:, 2:-1])
    # print(pca.components_)
    return [
        pd.DataFrame({"country": df["country"], "govt_trust_index": vals[:, 0] * (-1)}),
        pca,
    ]
