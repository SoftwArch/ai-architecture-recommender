import asyncio
from src.services.assistant_service import AssistantService

async def main():
    service = AssistantService()
    result = await service.process_request(
        "开发电商平台，需要支持秒杀活动和实时订单处理，预计日活用户百万级"
    )
    print(result)

    # 查询架构详情
    microservices_info = await service.get_architecture_details("微服务架构")
    print("架构详情:", microservices_info)

if __name__ == "__main__":
    asyncio.run(main())