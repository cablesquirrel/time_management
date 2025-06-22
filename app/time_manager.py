"""Time Manager"""

import asyncio
from typing import Self

from awx_service import AWXService
from config import settings
from service_base import ServiceBase


class TimeManager:
    """Time Manager instance"""

    _instance: Self = None

    def __init__(self) -> None:
        """Class initialization."""
        self._shutdown: bool = False
        self._balance_seconds: int = settings.default_balance_minutes * 60
        self._timer_paused: bool = True
        self._lock = asyncio.Lock()
        self._services: list[ServiceBase] = [AWXService()]

    def __new__(cls) -> None:
        """Class constructor."""
        raise RuntimeError("Use get_instance() to get the singleton instance")

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the class."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    async def run(self):
        """Start the process loop for the timer."""
        if settings.begin_stopped:
            # Start with all services stopped
            await self.stop_services()

        while not self._shutdown:
            # Acquire the lock
            async with self._lock:
                # Decrement the balance if timer not paused
                if not self._timer_paused:
                    self._balance_seconds -= 1
                    # Handle out-of-time
                    if self._balance_seconds <= 0:
                        self._timer_paused = True
                        await self.stop_services()
            # Tick every second
            await asyncio.sleep(1)

    async def shutdown(self):
        """Stop the process loop."""
        self._shutdown = True

    async def pause(self):
        """Pause the process loop."""
        async with self._lock:
            self._timer_paused = True
            await self.stop_services()

    async def resume(self):
        """Pause the process loop."""
        async with self._lock:
            self._timer_paused = False
            if self._balance_seconds > 0:
                await self.start_services()

    async def is_paused(self) -> bool:
        """Get the current paused status."""
        return self._timer_paused

    async def get_remaining_time(self) -> tuple[int, int, int, int]:
        """Get the amount of time remaining on the balance

        Returns:
            tuple: (time remaining in seconds, time remaining in minutes, seconds remaining after minutes )
        """
        hours_remaining = (self._balance_seconds // 60) // 60
        minutes_remaining = (self._balance_seconds - (hours_remaining * 60 * 60)) // 60
        leftover_seconds_remaining = self._balance_seconds % 60
        return (
            self._balance_seconds,
            hours_remaining,
            minutes_remaining,
            leftover_seconds_remaining,
        )

    async def set_remaining_time_seconds(self, seconds: int):
        """Set the amount of time remaining in seconds

        Args:
            seconds (int): Desired number of seconds to set as remaining
        """
        async with self._lock:
            self._balance_seconds = seconds

    async def set_remaining_time_minutes(self, minutes: int):
        """Set the amount of time remaining in minutes

        Args:
            minutes (int): Desired number of minutes to set as remaining
        """
        async with self._lock:
            self._balance_seconds = minutes * 60

    async def set_remaining_time_hours(self, hours: int):
        """Set the amount of time remaining in hours

        Args:
            hours (int): Desired number of hours to set as remaining
        """
        async with self._lock:
            self._balance_seconds = hours * 60 * 60

    async def add_minutes(self, minutes: int):
        """Add the specified amount of minutes to the balance

        Args:
            minutes (int): Desired amount of minutes to add
        """
        async with self._lock:
            self._balance_seconds += minutes * 60

    async def add_hours(self, hours: int):
        """Add the specified amount of hours to the balance

        Args:
            hours (int): Desired amount of hours to add
        """
        async with self._lock:
            self._balance_seconds += hours * 60 * 60

    async def stop_services(self):
        for service in self._services:
            await service.stop()

    async def start_services(self):
        for service in self._services:
            await service.start()
