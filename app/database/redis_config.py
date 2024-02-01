import json

from redis import asyncio as aioredis

# from app.database.schema.global_config import GlobalConfig


class RedisConfig:
    """
    Redis 설정
    """

    def __init__(self, conf: dict):
        self.redis_expire_time = int(str(conf.get("REDIS_EXPIRE_TIME", 900)))
        self.client = aioredis.Redis(
            host=str(conf.get("REDIS_HOST", "")),
            port=int(str(conf.get("REDIS_PORT", 6379))),
            password=str(conf.get("REDIS_PASSWORD")),
        )

    async def get_user_cahce(self, user_id: str) -> str | None:
        """
        유저정보 캐시로 관리
        """
        if self.client is None:
            raise ValueError("Redis 인스턴스가 초기화되지 않았습니다.")
        cahce_user = await self.client.get(f"cahce_user_info_{user_id}")

        if cahce_user is None:
            await self.client.set(
                name=f"cahce_user_info_{user_id}",
                value=str(json.dumps(cahce_user)),
                ex=self.redis_expire_time,
            )
            cahce_user = await self.client.get(f"cahce_user_info_{user_id}")

        if isinstance(cahce_user, bytes):
            cahce_user = cahce_user.decode()
            return cahce_user
        else:
            return None
