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

"""Pipeline for cleaning data -> explain what nodes do what sequentially
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    build_death_cases_count,
    clean_excess_deaths,
    clean_wig_data,
    get_latest_info_WB,
    merge_WB_datasets,
    merge_WB_health_systems,
    merge_WB_heath_corona,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(clean_wig_data, "params:wigi_data_setpath", "clean_wig_data"),
            node(clean_excess_deaths, "raw_excess_deaths", "cleaned_excess_deaths"),
            node(
                build_death_cases_count, "covid_19_data", "covid_19_data_cases_deaths"
            ),
            node(
                get_latest_info_WB,
                ["hospital_beds_raw", "params:hospital_beds_param"],
                "hospital_beds_agg",
                tags="WB DATA",
            ),
            node(
                get_latest_info_WB,
                ["specialist_doctors_raw", "params:specialist_doctors_param"],
                "specialist_doctors_agg",
                tags="WB DATA",
            ),
            node(
                get_latest_info_WB,
                ["health_workers_raw", "params:health_workers_param"],
                "health_workers_agg",
                tags="WB DATA",
            ),
            node(
                get_latest_info_WB,
                ["physicians_raw", "params:physicians_param"],
                "physicians_agg",
                tags="WB DATA",
            ),
            node(
                get_latest_info_WB,
                ["handwashing_raw", "params:handwashing_param"],
                "handwashing_agg",
                tags="WB DATA",
            ),
            node(
                get_latest_info_WB,
                ["glbl_population_raw", "params:glbl_population_param"],
                "glbl_population_agg",
                tags="WB DATA",
            ),
            node(
                merge_WB_datasets,
                [
                    "hospital_beds_agg",
                    "specialist_doctors_agg",
                    "health_workers_agg",
                    "physicians_agg",
                    "handwashing_agg",
                    "glbl_population_agg",
                ],
                "WB_data_full",
                tags="WB DATA",
            ),
            node(
                merge_WB_health_systems,
                ["WB_data_full", "health_system"],
                "WB_health",
                tags="WB DATA",
            ),
            node(
                merge_WB_heath_corona,
                ["WB_health", "covid_19_data_cases_deaths"],
                "WB_health_cases",
                tags="WB DATA",
            ),
        ]
    )
