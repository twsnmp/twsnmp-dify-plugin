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

class GetNodeListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからノードリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - name_filter (str): 名前フィルター
                - ip_filter (str): IPフィルター
                - state_filter (str): 状態フィルター

        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_node_list")
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
        state = tool_parameters.get("state_filter", "") 

        # 3. TWSNMP FCからノードリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        nodes = api.get("/api/nodes")
        if not nodes:
            logger.error("Failed to retrieve nodes from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve nodes from TWSNMP FC")
        
        # 4. 結果を返す
        for node  in nodes:
            if name and name not in node.get("Name",""):
                continue
            if ip and ip not in node.get("IP",""):
                continue
            if state and state not in node.get("State",""):
                continue
            del node["Password"]
            del node["GNMIPassword"]
            del node["Community"]
            logger.info(node)
            yield self.create_json_message(node)
        logger.info("end get_node_list")
 