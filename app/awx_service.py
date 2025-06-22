"""Define the service for Ansible AWX"""

import logging

import httpx
from config import settings
from httpx import Response
from logger import CustomLogger
from service_base import ServiceBase

logger = CustomLogger()


class AWXService(ServiceBase):
    """AWX Service Class"""

    def __init__(self):
        self._awx_url: str = settings.awx_url
        self._awx_user: str = settings.awx_user
        self._awx_pass: str = settings.awx_password
        self._job_template_id: int = settings.awx_job_template_id
        self._job_var_switch: str = settings.awx_job_var_switch
        self._job_var_interface: str = settings.awx_job_var_interface

    async def stop(self):
        """Stop the AWX Service (Call the job with 'shut' action)"""
        logger.log(logging.INFO, f"Calling Playbook to shutdown port {self._job_var_interface} on {self._job_var_switch}")
        await self.launch_job("shut")

    async def start(self):
        """Stop the AWX Service (Call the job with 'no shut' action)"""
        logger.log(logging.INFO, f"Calling Playbook to shutdown port {self._job_var_interface} on {self._job_var_switch}")
        await self.launch_job("no shut")

    async def launch_job(self, port_status: str):
        """Launch the AWX job"""
        url: str = f"{self._awx_url}/api/v2/job_templates/{self._job_template_id}/launch/"
        payload = {"extra_vars": {"switch": self._job_var_switch, "interface": self._job_var_interface, "port_status": port_status}}
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response: Response = httpx.post(url, auth=(self._awx_user, self._awx_pass), json=payload, headers=headers)

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            logger.log(logging.ERROR, f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.log(logging.ERROR, f"An error occurred while requesting {e.request.url}: {e}")
