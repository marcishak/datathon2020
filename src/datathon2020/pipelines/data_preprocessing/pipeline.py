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

"""Pipeline for preprocessing the data for modelling -> explain what nodes do
what sequentially
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    aggregate_excess_deaths,
    exp_weight_wig_data,
    naive_combine_data_sets,
    pca_wig_data,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(exp_weight_wig_data, "clean_wig_data", "exp_wig_data_pre_pca"),
            node(pca_wig_data, "exp_wig_data_pre_pca", ["exp_wig_data", "pca_wig"]),
            node(
                aggregate_excess_deaths,
                "cleaned_excess_deaths",
                "agg_cleaned_excess_deaths",
            ),
            node(
                naive_combine_data_sets,
                ["agg_cleaned_excess_deaths", "exp_wig_data"],
                "merged_data_wig_excess",
            ),
        ]
    )
