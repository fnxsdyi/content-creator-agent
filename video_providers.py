# video_providers.py
"""
多平台视频生成服务统一接口
支持：即梦 (Jimeng)、可灵 (Kling)、智谱 (CogVideoX)
"""

import requests
import time
import base64
from abc import ABC, abstractmethod
from typing import Optional, List


class VideoProvider(ABC):
    """视频生成平台抽象基类"""

    @abstractmethod
    def text_to_video(self, prompt: str, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        """文字转视频，返回 task_id"""
        pass

    @abstractmethod
    def image_to_video(self, image_url: str, prompt: Optional[str] = None, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        """图片转视频，返回 task_id"""
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> dict:
        """查询任务状态"""
        pass

    def avatar_video(self, avatar_id: str, script: str, voice_id: Optional[str] = None) -> str:
        """数字分身视频生成（仅部分平台支持）"""
        raise NotImplementedError("This provider does not support avatar video generation")

    def get_avatars(self) -> list:
        """获取可用的数字分身列表（仅部分平台支持）"""
        raise NotImplementedError("This provider does not support avatar listing")

    def wait_for_video(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> dict:
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

    def wait_for_videos(self, task_ids: List[str], timeout: int = 600, poll_interval: int = 5) -> List[dict]:
        """等待多个视频生成完成"""
        results = []
        start_time = time.time()
        pending = set(task_ids)

        while pending and time.time() - start_time < timeout:
            for task_id in list(pending):
                try:
                    status = self.get_task_status(task_id)
                    if status.get("status") == "completed":
                        results.append(status)
                        pending.discard(task_id)
                    elif status.get("status") == "failed":
                        raise Exception(status.get("error", f"Video {task_id} failed"))
                except Exception:
                    pass
            if pending:
                time.sleep(poll_interval)

        if pending:
            raise TimeoutError(f"Timeout waiting for {len(pending)} videos")
        return results


# ── 即梦 (Jimeng) ─────────────────────────────────────────────────────────────

class JimengProvider(VideoProvider):
    """即梦 (Jimeng) - 字节跳动出品"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://jimeng.jianying.com/mweb/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def text_to_video(self, prompt: str, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(f"{self.base_url}/generate/video", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Jimeng API error"))
        return data.get("data", {}).get("task_id")

    def image_to_video(self, image_url: str, prompt: Optional[str] = None, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        payload = {
            "image_url": image_url,
            "prompt": prompt or "",
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(f"{self.base_url}/generate/video/image", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Jimeng API error"))
        return data.get("data", {}).get("task_id")

    def get_task_status(self, task_id: str) -> dict:
        response = requests.get(f"{self.base_url}/task/{task_id}", headers=self.headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Jimeng API error"))
        return data.get("data", {})


# ── 可灵 (Kling) ──────────────────────────────────────────────────────────────

class KlingProvider(VideoProvider):
    """可灵 (Kling) - 快手出品"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.klingai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def text_to_video(self, prompt: str, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        # 可灵使用负面提示词等参数
        duration_map = {3: "5", 5: "5", 10: "10"}
        payload = {
            "model_name": "kling-v1",
            "prompt": prompt,
            "negative_prompt": "",
            "cfg_scale": 0.5,
            "mode": "std",
            "duration": duration_map.get(duration, "5"),
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(f"{self.base_url}/videos/generations", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Kling API error"))
        return data.get("data", {}).get("id")

    def image_to_video(self, image_url: str, prompt: Optional[str] = None, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        duration_map = {3: "5", 5: "5", 10: "10"}
        payload = {
            "model_name": "kling-v1",
            "image": image_url,
            "prompt": prompt or "",
            "negative_prompt": "",
            "cfg_scale": 0.5,
            "mode": "std",
            "duration": duration_map.get(duration, "5"),
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(f"{self.base_url}/videos/generations", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Kling API error"))
        return data.get("data", {}).get("id")

    def get_task_status(self, task_id: str) -> dict:
        response = requests.get(f"{self.base_url}/videos/generations/{task_id}", headers=self.headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Kling API error"))
        task_data = data.get("data", {})
        # 映射状态
        status_map = {"succeed": "completed", "failed": "failed", "processing": "processing"}
        return {
            "status": status_map.get(task_data.get("task_status"), "processing"),
            "video_url": task_data.get("task_result", {}).get("videos", [{}])[0].get("url"),
            "error": task_data.get("task_status_msg")
        }

    def get_avatars(self) -> list:
        """获取可灵数字分身列表"""
        response = requests.get(f"{self.base_url}/digital-human/avatars", headers=self.headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            return []
        return data.get("data", {}).get("avatars", [])

    def avatar_video(
        self,
        avatar_id: str,
        script: str,
        voice_id: Optional[str] = None,
        aspect_ratio: str = "16:9"
    ) -> str:
        """数字分身视频生成"""
        payload = {
            "avatar_id": avatar_id,
            "script": script,
            "voice_id": voice_id or "default",
            "aspect_ratio": aspect_ratio
        }
        response = requests.post(
            f"{self.base_url}/digital-human/generations",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(data.get("message", "Kling digital human API error"))
        return data.get("data", {}).get("task_id")


# ── 智谱 CogVideoX ────────────────────────────────────────────────────────────

class CogVideoXProvider(VideoProvider):
    """智谱 CogVideoX - 智谱 AI 出品"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def text_to_video(self, prompt: str, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        payload = {
            "model": "cogvideox",
            "prompt": prompt,
        }
        response = requests.post(f"{self.base_url}/videos/generations", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("id")

    def image_to_video(self, image_url: str, prompt: Optional[str] = None, duration: int = 5, aspect_ratio: str = "16:9") -> str:
        # CogVideoX 图生视频使用不同的端点
        payload = {
            "model": "cogvideox",
            "prompt": prompt or "",
            "image_url": image_url
        }
        response = requests.post(f"{self.base_url}/videos/generations", headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("id")

    def get_task_status(self, task_id: str) -> dict:
        response = requests.get(f"{self.base_url}/videos/generations/{task_id}", headers=self.headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        status_map = {"SUCCESS": "completed", "FAIL": "failed", "PROCESSING": "processing"}
        return {
            "status": status_map.get(data.get("status"), "processing"),
            "video_url": data.get("video", {}).get("url"),
            "error": data.get("error")
        }


# ── 平台工厂 ──────────────────────────────────────────────────────────────────

VIDEO_PROVIDERS = {
    "jimeng": {
        "name": "即梦 (Jimeng)",
        "description": "字节跳动出品，中文支持最好",
        "class": JimengProvider,
    },
    "kling": {
        "name": "可灵 (Kling)",
        "description": "快手出品，质量高",
        "class": KlingProvider,
    },
    "cogvideox": {
        "name": "智谱 (CogVideoX)",
        "description": "智谱AI出品，可本地部署",
        "class": CogVideoXProvider,
    },
}


def get_provider(provider_name: str, api_key: str) -> VideoProvider:
    """获取视频生成平台实例"""
    provider_info = VIDEO_PROVIDERS.get(provider_name)
    if not provider_info:
        raise ValueError(f"Unknown provider: {provider_name}")
    return provider_info["class"](api_key)


def get_provider_names() -> List[str]:
    """获取所有可用平台名称"""
    return list(VIDEO_PROVIDERS.keys())