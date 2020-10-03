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

import pandas as pd
import os


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
