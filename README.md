Random
------
[![ACR B1b](https://img.shields.io/badge/ACR-B1b-2140B5)](ACR.md)

## Demo

https://random.greg.ca

## Installation

- Clone the repository
- Run "docker-compose up -d"
- Load http://127.0.0.1:8088 in your web browser

By default the port only listens on 127.0.0.1, so the app can't be reached from other machines unless a reverse proxy on the same host forwards to it. To listen on another address, set `BIND_ADDRESS`, either in the shell or in a `.env` file next to `docker-compose.yml` (for example `BIND_ADDRESS=0.0.0.0` for every address).

## License

MIT License

Copyright (c) 2024-2026 Greg Chetcuti <greg@chetcuti.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
