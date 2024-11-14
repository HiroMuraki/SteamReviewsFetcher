from concurrent.futures import ThreadPoolExecutor
import asyncio


class AsyncHelper:
    @staticmethod
    async def run(*functions):
        loop = asyncio.get_running_loop()

        with ThreadPoolExecutor() as executor:
            results = await asyncio.gather(*[loop.run_in_executor(executor, x) for x in functions])

        return results
