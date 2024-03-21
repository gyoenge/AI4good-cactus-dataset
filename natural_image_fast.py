import aiohttp
import asyncio
import os
import uuid


async def download_image(session, url, fileroot):
    async with session.get(url) as response:
        if response.status == 200:
            img_filename = fileroot + f"{uuid.uuid4()}.jpg"
            with open(img_filename, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
        else:
            print(f"Failed to get image: {response.status}")


async def download_images_by_id(fileroot, img_size, img_num, start_id, end_id):
    os.makedirs(fileroot, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for img_id in range(start_id, end_id + 1):
            url = f"https://picsum.photos/id/{img_id}/{img_size[0]}/{img_size[1]}"
            task = asyncio.ensure_future(
                download_image(session, url, fileroot))
            tasks.append(task)
            if len(tasks) >= img_num:
                await asyncio.gather(*tasks)
                tasks = []  # Reset tasks list for the next batch
        if tasks:  # In case there are any remaining tasks
            await asyncio.gather(*tasks)


async def download_random_images(fileroot, img_size, img_num):
    os.makedirs(fileroot, exist_ok=True)
    url = f"https://picsum.photos/{img_size[0]}/{img_size[1]}"
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(download_image(
            session, url, fileroot)) for _ in range(img_num)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    fileroot = "dataset/natural_image_500_200_500/"
    img_size = (500, 200)

    # id mode
    img_num = 1000  # Number of concurrent downloads
    start_id, end_id = 1, 1000
    asyncio.run(download_images_by_id(
        fileroot, img_size, img_num, start_id, end_id))

    # random mode
    # img_num = 500
    # asyncio.run(download_random_images(fileroot, img_size, img_num))
