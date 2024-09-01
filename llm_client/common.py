#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: common.py
Time: 2024/8/31
"""
import asyncio
import json
import os
import httpx
import ujson

from typing import Dict, Any


class LLMClient(object):
    """
    大模型连接客户端
    """
    def __init__(self, api_base: str, api_key: str, timeout: int, version: str = "v1"):
        if not api_base:
            api_base = "https://api.openai.com/v1/chat/completions"

        if not api_key:
            api_key = os.getenv("DBGPT_API_KEY")

        if api_base:
            self._api_url = api_base
        else:
            raise ValueError(f"api url {api_base} does not exist or is not accessible.")

        self._api_key = api_key
        self._version = version
        self._timeout = timeout
        headers = {"Authorization": f"Bearer {self._api_key}"} if self._api_key else {}
        self._http_client = httpx.AsyncClient(
            headers=headers, timeout=timeout if timeout else httpx.Timeout(None)
        )

    async def chat_stream(self,
                          model: str,
                          messages: list,
                          temperature: float,
                          max_tokens: int = 4096,
                          stream: bool = True,
        ):
        """
        流式接口
        :return:
        """
        data = {"model": model, "messages": messages, "temperature": temperature,
                "max_tokens": max_tokens, "stream": stream}

        async for chat_completion_response in self._chat_stream(data):
            yield chat_completion_response

    async def _chat_stream(
            self, data: Dict[str, Any]
    ):
        """Chat Stream Completion.

        Args:
            data: dict, The data to send to the API.
        Returns:
            AsyncGenerator[dict, None]: The chat completion response.
        """
        async with self._http_client.stream(
                method="POST",
                url=self._api_url + "/chat/completions",
                json=data,
                headers={},
        ) as response:
            if response.status_code == 200:
                async for line in response.aiter_lines():
                    if "[DONE]" in line:
                        continue

                    if line.startswith("data: "):
                        sse_data = line[len("data: "):]
                        try:
                            if sse_data:
                                json_data = ujson.loads(sse_data)
                                yield json_data
                            else:
                                continue

                        except json.decoder.JSONDecodeError as e:
                            raise Exception(
                                f"Failed to parse SSE data: {e}, sse_data: {sse_data}"
                            )

            else:
                try:
                    error = await response.aread()
                    yield ujson.loads(error)
                except Exception as e:
                    raise e

    def chat(self):
        """
        非流式接口
        :return:
        """
        pass

# async def main():
#     api_base = "https://api.xiaoai.plus/v1"
#     api_key = "sk-7BHG9QMubXRn3rVi108a4eDbE4384143989134311098B9E7"
#     llm_cli = LLMClient(api_base, api_key, timeout=60)
#
#     model = "gpt-3.5-turbo"
#     messages = [{"role": "user", "content": "Hello, how are you?"}]
#     temperature = 0.7
#     max_tokens = 1024
#
#
#     async for response in llm_cli.chat_stream(model, messages, temperature, max_tokens):
#         print(response)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
