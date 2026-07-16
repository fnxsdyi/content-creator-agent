# jimeng_client.py
import requests
import time
import base64
from typing import Optional, List

class JimengClient:
    """即梦 (Jimeng) API 客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://jimeng.jianying.com/mweb/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def text_to_video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9"
    ) -> str:
        """文字转视频"""
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(
            f"{self.base_url}/generate/video",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Unknown error"))
        return data.get("data", {}).get("task_id")

    def image_to_video(
        self,
        image_url: str,
        prompt: Optional[str] = None,
        duration: int = 5,
        aspect_ratio: str = "16:9"
    ) -> str:
        """图片转视频"""
        payload = {
            "image_url": image_url,
            "prompt": prompt or "",
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(
            f"{self.base_url}/generate/video/image",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Unknown error"))
        return data.get("data", {}).get("task_id")

    def script_to_video(
        self,
        segments: List[dict],
        duration: int = 5,
        aspect_ratio: str = "16:9"
    ) -> List[str]:
        """脚本转视频 - 逐段生成"""
        task_ids = []
        for segment in segments:
            if "image_url" in segment and segment["image_url"]:
                task_id = self.image_to_video(
                    segment["image_url"],
                    segment.get("prompt"),
                    duration,
                    aspect_ratio
                )
            else:
                task_id = self.text_to_video(
                    segment["prompt"],
                    duration,
                    aspect_ratio
                )
            task_ids.append(task_id)
        return task_ids

    def get_task_status(self, task_id: str) -> dict:
        """查询任务状态"""
        response = requests.get(
            f"{self.base_url}/task/{task_id}",
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Unknown error"))
        return data.get("data", {})

    def wait_for_video(
        self,
        task_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> dict:
        """等待视频生成完成"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            if status.get("status") == "completed":
                return status
            elif status.get("status") == "failed":
                raise Exception(status.get("error", "Video generation failed"))
            time.sleep(poll_interval)
        raise TimeoutError("Video generation timed out")

    def wait_for_videos(
        self,
        task_ids: List[str],
        timeout: int = 600,
        poll_interval: int = 5
    ) -> List[dict]:
        """等待多个视频生成完成"""
        results = []
        start_time = time.time()
        pending = set(task_ids)

        while pending and time.time() - start_time < timeout:
            for task_id in list(pending):
                status = self.get_task_status(task_id)
                if status.get("status") == "completed":
                    results.append(status)
                    pending.discard(task_id)
                elif status.get("status") == "failed":
                    raise Exception(status.get("error", f"Video {task_id} failed"))
            if pending:
                time.sleep(poll_interval)

        if pending:
            raise TimeoutError(f"Timeout waiting for {len(pending)} videos")
        return results