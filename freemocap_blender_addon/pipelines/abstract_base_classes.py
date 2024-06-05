from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List

from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


class BasePipelineIOABC(TypeSafeDataclass, ABC):
    pass


class AbstractPipelineStage(TypeSafeDataclass, ABC, Generic[InputType, OutputType]):
    @abstractmethod
    def process(self, data: InputType) -> OutputType:
        pass



class AbstractPipeline(TypeSafeDataclass, ABC):
    stages: List[AbstractPipelineStage] = field(default_factory=list)

    @abstractmethod
    def run(self, data: InputType):
        pass