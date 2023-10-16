import asyncio

from app.utils.azure_util import AzureUtil


async def main():
    sutil = AzureUtil()
    await sutil.azure_long_s2t("X:\\Programming\\Web\\lc2_ambispeech\\backend_fastapi\\test.wav")


if __name__ == '__main__':
    asyncio.run(main())
