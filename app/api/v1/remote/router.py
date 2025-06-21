"""API Router for remote control interface"""

import json

from api.v1.remote.service import build_message_json, format_time_string
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from time_manager import TimeManager

router = APIRouter()
time_manager = TimeManager.get_instance()


@router.get("/text")
async def get_display_text() -> JSONResponse:
    paused_status: bool = await time_manager.is_paused()
    remaining_time: tuple[int, int, int, int] = await time_manager.get_remaining_time()
    if remaining_time[0] <= 0:
        return build_message_json(" *Out of Time*", format_time_string(remaining_time))
    elif paused_status is True:
        return build_message_json(" *Time Paused*", format_time_string(remaining_time))
    else:
        return build_message_json("", format_time_string(await time_manager.get_remaining_time()))


@router.post("/set-seconds")
async def set_seconds(seconds: int) -> JSONResponse:
    await time_manager.set_remaining_time_seconds(seconds)
    return json.dumps(
        {
            "status": "success",
            "time_remaining": format_time_string(await time_manager.get_remaining_time()),
        }
    )


@router.post("/set-minutes")
async def set_minutes(minutes: int) -> JSONResponse:
    await time_manager.set_remaining_time_minutes(minutes)
    return json.dumps(
        {
            "status": "success",
            "time_remaining": format_time_string(await time_manager.get_remaining_time()),
        }
    )


@router.post("/set-hours")
async def set_hours(hours: int) -> JSONResponse:
    await time_manager.set_remaining_time_hours(hours)
    return {
        "status": "success",
        "time_remaining": format_time_string(await time_manager.get_remaining_time()),
    }


@router.post("/add-minutes")
async def add_minutes(minutes: int) -> JSONResponse:
    await time_manager.add_minutes(minutes)
    return json.dumps(
        {
            "status": "success",
            "time_remaining": format_time_string(await time_manager.get_remaining_time()),
        }
    )


@router.post("/add-hours")
async def add_hours(hours: int) -> JSONResponse:
    await time_manager.add_hours(hours)
    return json.dumps(
        {
            "status": "success",
            "time_remaining": format_time_string(await time_manager.get_remaining_time()),
        }
    )


@router.post("/toggle_pause")
async def toggle_pause() -> JSONResponse:
    paused_status = await time_manager.is_paused()
    if paused_status is True:
        await time_manager.resume()
    else:
        await time_manager.pause()
    return json.dumps(
        {
            "status": "success",
            "time_remaining": format_time_string(await time_manager.get_remaining_time()),
        }
    )
