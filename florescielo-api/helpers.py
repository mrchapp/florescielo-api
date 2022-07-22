# Copyright © 2018, Encode OSS Ltd. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Derived from here:
#   https://github.com/encode/starlette/blob/master/starlette/responses.py

import typing

from fastapi.responses import JSONResponse


class CaseSensitiveHeadersResponse(JSONResponse):
    def init_headers(
        self, headers: typing.Optional[typing.Mapping[str, str]] = None
    ) -> None:
        if headers is None:
            raw_headers: typing.List[typing.Tuple[bytes, bytes]] = []
            populate_content_length = True
            populate_content_type = True
        else:
            raw_headers = [
                (k.encode("latin-1"), v.encode("latin-1")) for k, v in headers.items()
            ]
            keys = [h[0].lower() for h in raw_headers]
            populate_content_length = b"content-length" not in keys
            populate_content_type = b"content-type" not in keys

        body = getattr(self, "body", None)
        if (
            body is not None
            and populate_content_length
            and not (self.status_code < 200 or self.status_code in (204, 304))
        ):
            content_length = str(len(body))
            raw_headers.append((b"Content-Length", content_length.encode("latin-1")))

        content_type = self.media_type
        if content_type is not None and populate_content_type:
            if content_type.startswith("text/"):
                content_type += "; charset=" + self.charset
            raw_headers.append((b"Content-Type", content_type.encode("latin-1")))

        self.raw_headers = raw_headers
