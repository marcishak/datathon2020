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
"""These nodes aim to remove imperfections and inconsistancies that exist when
the data is initally collected.
"""

# from typing import Any, Dict

import os

import pandas as pd


def clean_wig_data(file_path: str) -> pd.DataFrame:
    """Cleans wig data from Stat file - This function is a crutch which relies on R!
    this takes the file path in from parameters! please set to the appropriate
    one for you!
    Instead of using the complecated xlsx file this uses a varity of R packages
    to load and clean the stata version.
    Make sure that your PATH includes Rscript!
    For required R packages see requirments.R
    """
    print(os.getcwd())
    os.system(
        f"Rscript src/datathon2020/pipelines/data_cleanup/clean_wigi.R {file_path}"
    )
    return pd.read_csv("data/01_raw/wgidataset_stata/wgidataset.csv")


def clean_excess_deaths(df):
    """
    cleans excess deaths data ->
    gets rid of regions, converts countries to lower case and
    makes britain the uk
    """
    df = df.loc[df["region"] == df["country"]]
    df["country"] = df["country"].str.lower()
    df.loc[df["country"] == "britain", "country"] = "united kingdom"
    return df


def build_death_cases_count(df: pd.DataFrame) -> pd.DataFrame:
    """builds out cases and deaths for each country
    """
    df1 = df.groupby(["Country/Region"]).Confirmed.sum().to_frame()
    df2 = df.groupby(["Country/Region"]).Deaths.sum().to_frame()
    return_df = pd.merge(df1, df2, on=["Country/Region"]).reset_index()
    # print(return_df.head())
    return_df["Country/Region"] = return_df["Country/Region"].replace(
        ["Congo (Kinshasa)"], "Congo, Rep."
    )
    return_df["Country/Region"] = return_df["Country/Region"].replace(
        ["Ivory Coast"], "Cote d'Ivoire"
    )
    return_df["Country/Region"] = return_df["Country/Region"].replace(
        ["Macau"], "Macao SAR, China"
    )
    return_df["Country/Region"] = return_df["Country/Region"].replace(
        ["Iran"], "Iran, Islamic Rep."
    )
    return_df["Country/Region"] = return_df["Country/Region"].replace(
        ["Venezuela"], "Venezuela, RB"
    )
    return return_df


def get_latest_info_WB(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df2 = pd.melt(
        df, ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    )
    df3 = (
        df2[df2["variable"] != "Unnamed: 64"]
        .dropna()
        .sort_values("variable")
        .groupby(["Country Name", "Country Code"])
        .agg({"variable": "last", "value": "last"})
        .reset_index()
    )
    df3.columns = ["Country Name", "Country Code", "year", col]
    return df3


def merge_WB_datasets(
    df1: pd.DataFrame,
    df3: pd.DataFrame,
    df2: pd.DataFrame,
    df4: pd.DataFrame,
    df5: pd.DataFrame,
    df6: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merges the 6 WB data sets into  a single megatable
    """
    health_factors = pd.merge(df1, df2, on=["Country Name", "Country Code"], how="outer")
    health_factors = pd.merge(health_factors, df3, on=["Country Name", "Country Code"], how="outer")
    health_factors = pd.merge(health_factors, df4, on=["Country Name", "Country Code"], how="outer")
    health_factors = pd.merge(health_factors, df5, on=["Country Name", "Country Code"], how="outer")
    health_factors = pd.merge(health_factors, df6, on=["Country Name", "Country Code"], how="outer")
    return health_factors


def merge_WB_health_systems(
    WB: pd.DataFrame, health_systems: pd.DataFrame
) -> pd.DataFrame:
    print(WB.head())
    print(health_systems.head())
    return pd.merge(
        WB, health_systems, left_on="Country Name", right_on="World_Bank_Name"
    )


def merge_WB_heath_corona(WB: pd.DataFrame, corona: pd.DataFrame) -> pd.DataFrame:
    # print(WB.head())
    # print(corona.head())
    df = pd.merge(WB, corona, left_on="Country Name", right_on="Country/Region")
    return df
