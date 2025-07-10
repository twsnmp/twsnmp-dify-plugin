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
from twlib.time_util import unix_to_datetime_string

class DoPingTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからPINGを実施して結果をJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - target_ip (str): 対象のIPアドレス
                - size (number): PINGパケットのサイズ
                - ttl (number): PINGパケットのTTL

        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start do_ping")
        # 1. ランタイムから認証情報を取得
        try:
            url = self.runtime.credentials["twsnmp_url"]
            user = self.runtime.credentials["twsnmp_user"]
            password = self.runtime.credentials["twsnmp_password"]
        except KeyError:
            logger.error("Credentials not set")
            yield self.create_text_message("Credentials not set")
 
        # 2. ツールの入力パラメータを取得
        target = tool_parameters.get("target_ip", "") 
        size = tool_parameters.get("size",64) 
        ttl = tool_parameters.get("ttl", 64) 

        # 3. TWSNMP FCでpingを実施
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        r = api.post("/api/ping",{"IP":target,"Size": size,"TTL": ttl})
        if not r:
            logger.error("Failed to execute ping TWSNMP FC")
            yield self.create_text_message("Failed to execute ping from TWSNMP FC")
        
        # 4. 結果を返す
        r["TimeStamp"] =  unix_to_datetime_string(r.get("TimeStamp",0))
        r["Time"] = r.get("Time",0) / (1000 * 1000 * 1000.0)
        ping_stat = {
            1: "ok",
            2: "timeout",
            4: "time exceeded"
        }
        r["Stat"] = ping_stat.get(r.get("Stat",0),"error")        
        yield self.create_json_message(r)
        logger.info("end do_ping")
 