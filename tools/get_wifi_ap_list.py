from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import logging and custom handler
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

# Set up logging with the custom handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


from twlib.twsnmpapi import TwsnmpAPI
from twlib.time_util import nanosecond_unix_to_datetime_string

class GetWifiAPListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからWifiのアクセスポイントリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
   
        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_wifi_ap_list")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
 
        # 3. TWSNMP FCからWifi APのリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        aps  = api.get("/api/report/WifiAP")
        if not aps:
            logger.error("Failed to retrieve Wifi AP list from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve Wifi AP list from TWSNMP FC")
        
        # 4. 結果を返す
        for a  in aps:
            a["FirstTime"] = nanosecond_unix_to_datetime_string(a.get("FirstTime",0))
            a["LastTime"] = nanosecond_unix_to_datetime_string(a.get("LastTime",0))
            yield self.create_json_message(a)
        logger.info("end get_wifi_ap_list")
 