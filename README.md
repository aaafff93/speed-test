# Internet Speed Test

A command-line tool written in Python for measuring download speed from a specified URL.

## Features

- Performs 10 sequential HTTP/HTTPS requests.
- Waits for each response to be fully downloaded.
- Measures the duration of each request.
- Calculates the total amount of downloaded data.
- Calculates the average request time and download speed.
- Prints individual request results and overall statistics.
- Handles HTTP errors, connection errors, and timeouts.

## Requirements

- Python 3.9+.

## Usage

Clone the repository:

```bash
git clone https://github.com/aaafff93/speed-test.git
cd speed-test
```

Run the script with a URL as an argument:

```bash
python main.py https://samplefile.com/samples/download/image/png/png_sample_file_10MB.png
```

## Units of Measurement

- **s(seconds)** — time measurement.
- **MiB** — mebibyte, where 1 MiB = 1,048,576 bytes.
- **Mbps** — megabits per second, where 1 Mbps = 1,000,000 bits per second.
