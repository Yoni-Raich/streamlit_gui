"""
Copyright (C) 2019 - 2024 Intel Corporation
This software and the related documents are Intel copyrighted materials, and
your use of them is governed by the express license under which they were
provided to you ("License"). Unless the License provides otherwise, you may not
use, modify, copy, publish, distribute, disclose or transmit this software or
the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or
implied warranties, other than those that are expressly stated in the License.
-------------------------------------------------------------------------------

:Authors :
    Eric Koay [eng.keong.koay@intel.com]

:Description :
    This is a demo script to demonstrate the usage of the IntelWikiAPI.

:Last Modified by :
    Eric Koay [eng.keong.koay@intel.com]

:Last Modified Date : 8 Aug 2024
"""

from intel_wiki_lib.intel_wiki_api import IntelWikiAPI

wiki_app = IntelWikiAPI()
wiki_app.set_cookies(
    "detected_bandwidth=HIGH; ... confluence.list.pages.cookie...."  # Add your cookies here
)

results = wiki_app.search_by_keyword("tsn", result_limit=5, save_results=True)

print("Total results:", len(results))
for idx, result in enumerate(results):
    print(f"Result {idx + 1}")
    print("Title:", result.title)
    print("URL:", result.url_link)
    print("")

print("Completed")