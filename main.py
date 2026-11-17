import argparse
import time
import urllib.request
import urllib.error
from urllib.parse import urlsplit, urlencode, urlunsplit, parse_qsl, urlparse

REQUEST_COUNT = 10


def with_cache_buster(url: str) -> str:
    parts = urlsplit(url)
    query = parse_qsl(parts.query)
    query.append(("_t", str(time.time_ns())))

    return urlunsplit((
        parts.scheme,
        parts.netloc,
        parts.path,
        urlencode(query),
        parts.fragment,
    ))


def download(url: str) -> tuple[float, int]:
    headers = {
        "Cache-Control": "no-cache, no-store",
        "Pragma": "no-cache"
    }

    request = urllib.request.Request(with_cache_buster(url), headers=headers)

    start_time = time.perf_counter()

    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()

    elapsed_time = time.perf_counter() - start_time

    return elapsed_time, len(data)


def validate_url(url: str) -> None:
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise ValueError("URL must start with http:// or https:// and contain a valid host")


def calculate_results(
        total_time: float,
        total_bytes: int,
        successful_requests: int) -> tuple[float, float]:
    average_time = total_time / successful_requests
    speed_mbps = (total_bytes * 8) / total_time / 1_000_000
    return average_time, speed_mbps


def print_request_result(
        request_number: int,
        elapsed_time: float,
        downloaded_bytes: int) -> None:
    speed_mbps = (downloaded_bytes * 8) / elapsed_time / 1_000_000

    print(
        f"Request {request_number}: {elapsed_time:.2f} s, "
        f"{downloaded_bytes / (1024 * 1024):.2f} MiB, "
        f"{speed_mbps:.2f} Mbps"
    )


def print_results(
        total_time: float,
        average_time: float,
        total_bytes: int,
        speed_mbps: float,
        request_count: int,
        successful_requests: int) -> None:
    print("\nResults:")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}/{request_count}")
    print(f"Average request time: {average_time:.2f} seconds")
    print(f"Total downloaded: {total_bytes / (1024 * 1024):.2f} MiB")
    print(f"Average download speed: {speed_mbps:.2f} Mbps")


def handle_error(error: Exception) -> None:
    if isinstance(error, TimeoutError):
        print(f"Request timed out: {error}")

    elif isinstance(error, urllib.error.HTTPError):
        print(f"HTTP error: {error.code} - {error.reason}")

    elif isinstance(error, urllib.error.URLError):
        if isinstance(error.reason, TimeoutError):
            print("Request timed out")
        else:
            print(f"Connection error: {error.reason}")

    elif isinstance(error, ValueError):
        print(f"Invalid URL: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Internet speed test"
    )

    parser.add_argument("url", help="URL of the resource to download")

    args = parser.parse_args()

    try:
        validate_url(args.url)
    except ValueError as error:
        handle_error(error)
        return

    total_time = 0
    total_bytes = 0
    successful_requests = 0

    for i in range(REQUEST_COUNT):
        try:
            elapsed_time, downloaded_bytes = download(args.url)

            total_time += elapsed_time
            total_bytes += downloaded_bytes
            successful_requests += 1

            print_request_result(i + 1, elapsed_time, downloaded_bytes)

        except (TimeoutError, urllib.error.URLError) as error:
            print(f"Request {i + 1} failed:")
            handle_error(error)

    if successful_requests == 0:
        print("No successful requests. Unable to calculate download speed.")
        return

    average_time, speed_mbps = calculate_results(
        total_time,
        total_bytes,
        successful_requests
    )

    print_results(
        total_time,
        average_time,
        total_bytes,
        speed_mbps,
        REQUEST_COUNT,
        successful_requests
    )


if __name__ == "__main__":
    main()
