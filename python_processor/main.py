import asyncio
from dotenv import load_dotenv
import os
from pebble import ProcessPool
import signal

from repositories import RedisRepo
from video_processor.processor import process_video
from services import SummarizeService
from schemas import Task
from schemas import Result

MAX_CONCURRENT = 3

sem = asyncio.Semaphore(MAX_CONCURRENT)
executor = ProcessPool()


def load_dotenv_data():
    load_dotenv()
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")
    password = os.getenv("REDIS_PASSWORD")
    max_concurrent = int(os.getenv("MAX_CONCURRENT"))
    model_path = os.getenv("MODEL_PATH")
    return host, port, password, max_concurrent, model_path


redis_repo: RedisRepo | None = None
summarize_service: SummarizeService | None = None


async def process_task(task: Task) -> Result:
    try:
        res = await asyncio.get_running_loop().run_in_executor(
            executor, process_video, 0, task, summarize_service
        )
        return res
    except Exception as e:
        print(f"Error processing {task}: {e}")
    except asyncio.CancelledError:
        await redis_repo.set_result(
            Result(
                id=task.id,
                title="",
                preview_link="",
                status="error",
                summary="",
            )
        )
    finally:
        sem.release()


def sync_callback(future: asyncio.Future):
    try:
        result: Result = future.result()
        asyncio.create_task(redis_repo.set_result(result))
    except asyncio.CancelledError:
        print("Task was cancelled, skipping result update.")
    except Exception as e:
        print(f"Error in callback: {e}")


async def worker_loop():
    try:
        while True:
            await sem.acquire()
            task: Task = await redis_repo.get_task()
            if task:
                fut = asyncio.create_task(process_task(task))
                fut.add_done_callback(sync_callback)
            else:
                sem.release()
                await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("loop stopped")


async def graceful_shutdown():
    print("\nInitiating shutdown...")

    executor.stop()
    executor.join()

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for i in tasks:
        i.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    if redis_repo is not None:
        await redis_repo.close()
    print("Shutdown complete.")


def handle_signal():
    asyncio.create_task(graceful_shutdown())


async def main():
    global redis_repo, MAX_CONCURRENT, sem, summarize_service

    host, port, password, max_concurrent, model_path = load_dotenv_data()
    MAX_CONCURRENT = max_concurrent
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    redis_repo = RedisRepo(
        host=host,
        port=port,
        password=password,
        queue_key="queue",
        hash_key="hash",
        processing_key="processing",
        done_key="done",
    )
    summarize_service = SummarizeService(model_path)

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)
    await worker_loop()


if __name__ == "__main__":
    print("starting")
    asyncio.run(main())
