import math
import json
import asyncio
import aiohttp
import threading

API_URL = "https://api.insee.fr/entreprises/sirene/V3.11/siren"
SECRETS_JSON = "services/public_apis/insee/secrets.insee.sirene_data_provider.json"

RESPONSE_SIZE = 1000


def print_thread_count():
    print(f"Active Threads: {len(threading.enumerate())}")
    print(f"Threads: {[thread.name for thread in threading.enumerate()]}")


async def fetch_data_chunk(
    session: aiohttp.ClientSession,
    headers: dict,
    begin_at: int = 0,
    response_size: int = RESPONSE_SIZE,
):

    url = f"{API_URL}?debut={begin_at}&nombre={response_size}"

    async with session.get(url=url, headers=headers) as response:

        return await response.text()


async def main():
    with open(SECRETS_JSON) as secrets_file:
        token = json.load(secrets_file)["token"]

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=API_URL, headers=headers) as response:
            print(f"Status: {response.status}")

            total_number_of_rows = int(response.headers["X-Total-Count"])
            nb_of_chunks = math.ceil(total_number_of_rows / RESPONSE_SIZE)

            # TEMP limiter of queries
            if nb_of_chunks > 10:
                nb_of_chunks = 10

        print_thread_count()

        tasks = [
            fetch_data_chunk(session=session, headers=headers, begin_at=chunk * RESPONSE_SIZE)
            for chunk in range(nb_of_chunks)
        ]

        print_thread_count()

        responses = await asyncio.gather(*tasks)

        print_thread_count()

        print(f"Number of responses : {len(responses)}")

        # for payload in responses:
        #     print(payload)
        print("END")


print_thread_count()
asyncio.run(main())
