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

class GetMACAddressListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからLAN上デバイスのリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - name_filter (str): 名前フィルター
                - ip_filter (str): IPフィルター
                - vendor_filter (str): ベンダー名フィルター

        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_mac_address_list")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
        name = tool_parameters.get("name_filter", "") 
        ip = tool_parameters.get("ip_filter", "") 
        vendor = tool_parameters.get("vendor_filter", "") 

        # 3. TWSNMP FCからMAC addressリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        devices = api.get("/api/report/devices")
        if not devices:
            logger.error("Failed to retrieve MAC address from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve MAC address list from TWSNMP FC")
        
        # 4. 結果を返す
        for d  in devices:
            if name and name not in d.get("Name",""):
                continue
            if ip and ip not in d.get("IP",""):
                continue
            if vendor and vendor not in d.get("Vendor",""):
                continue
            d["MAC"] = d.get("ID","")
            d["FirstTime"] = nanosecond_unix_to_datetime_string(d.get("FirstTime",0))
            d["LastTime"] = nanosecond_unix_to_datetime_string(d.get("LastTime",0))
            d["UpdateTime"] = nanosecond_unix_to_datetime_string(d.get("UpdateTime",0))
            del d["ID"]
            del d["ValidScore"]
            yield self.create_json_message(d)
        logger.info("end get_mac_address_list")
 