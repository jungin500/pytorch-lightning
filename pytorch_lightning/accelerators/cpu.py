# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, Dict, List, Union

import torch

from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.utilities.exceptions import MisconfigurationException
from pytorch_lightning.utilities.rank_zero import rank_zero_warn
from pytorch_lightning.utilities.types import _DEVICE


class CPUAccelerator(Accelerator):
    """Accelerator for CPU devices."""

    def setup_environment(self, root_device: torch.device) -> None:
        """
        Raises:
            MisconfigurationException:
                If the selected device is not CPU.
        """
        super().setup_environment(root_device)
        if root_device.type != "cpu":
            raise MisconfigurationException(f"Device should be CPU, got {root_device} instead.")

    def get_device_stats(self, device: _DEVICE) -> Dict[str, Any]:
        """CPU device stats aren't supported yet."""
        return {}

    @staticmethod
    def parse_devices(devices: Union[int, str, List[int]]) -> Union[int, str, List[int]]:
        """Accelerator device parsing logic."""
        return devices

    @staticmethod
    def get_parallel_devices(devices: Union[int, str, List[int]]) -> List[torch.device]:
        """Gets parallel devices for the Accelerator."""
        if isinstance(devices, int):
            return [torch.device("cpu")] * devices
        rank_zero_warn(
            f"The flag `devices` must be an int with `accelerator='cpu'`, got `devices={devices!r}` instead."
        )
        return []

    @staticmethod
    def auto_device_count() -> int:
        """Get the devices when set to auto."""
        return 1

    @staticmethod
    def is_available() -> bool:
        """CPU is always available for execution."""
        return True

    @staticmethod
    def name() -> str:
        """Name of the Accelerator."""
        return "cpu"
