# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.deps import CurrentUser
from app.core.config import get_settings
from app.services import k8s_client

settings = get_settings()
router = APIRouter()


@router.get("/pods")
async def get_pods(_: CurrentUser):
    return k8s_client.list_pods(namespace=settings.k8s_namespace)


@router.get("/events")
async def get_events(_: CurrentUser):
    return k8s_client.list_events(namespace=settings.k8s_namespace)


@router.get("/pvcs")
async def get_pvcs(_: CurrentUser):
    return k8s_client.list_pvcs(namespace=settings.k8s_namespace)
