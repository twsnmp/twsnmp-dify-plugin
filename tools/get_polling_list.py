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

class GetPollingListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        TWSNMP FCからポーリングリストを取得してJSONで返す。

        Args:
            tool_parameters: ツールの入力パラメータを含む辞書:
                - name_filter (str): 名前フィルター
                - node_name_filter (str): ノード名フィルター
                - type_filter (str): ポーリング種別フィルター
                - state_filter (str): 状態フィルター

        Yields:
            ToolInvokeMessage: JSON
        """
        logger.info("start get_polling_list")
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
        node_name_filter = tool_parameters.get("node_name_filter", "") 
        type = tool_parameters.get("type_filter", "") 
        state = tool_parameters.get("state_filter", "") 

        # 3. TWSNMP FCからノードリストを取得
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            logger.error("Can not login to TWSNMP FC")
            yield self.create_text_message(f"Can not login to TWSNMP FC: {r}")
          
        resp = api.get("/api/pollings")
        if not resp:
            logger.error("Failed to retrieve pollings from TWSNMP FC")
            yield self.create_text_message("Failed to retrieve pollings from TWSNMP FC")
        pollings = resp.get("Pollings")
        if not pollings:
            logger.error("pollings not found in responce")
            yield self.create_text_message("pollings not found in responce")
        nodes = resp.get("NodeList")
        if not nodes:
            logger.error("node list not found in responce")
            yield self.create_text_message("node list not found in responce")
        node_map = {}
        for node in nodes:
            id = node.get("value","")
            node_name = node.get("text","")
            if id and node_name:
                node_map[id] = node_name
        
        # 4. 結果を返す
        for polling  in pollings:
            if name and name not in polling.get("Name",""):
                continue
            if type and type not in polling.get("Type",""):
                continue
            if state and state not in node.get("State",""):
                continue
            node_id = polling.get("NodeID","")
            if not node_id:
                logger.error("node id not found")
                continue                
            node_name = node_map.get(node_id,"")
            if not node_name:
                logger.error(f"node name not found {node_id}")
                continue
            if node_name_filter:
                if node_name_filter not in node_name:
                    continue
            polling["NodeName"] = node_name
            yield self.create_json_message(polling)
        logger.info("end get_polling_list")
 