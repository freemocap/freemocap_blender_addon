from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic, get_type_hints




PipelineStageInput = TypeVar('PipelineStageInput')
PipelineStageOutput = TypeVar('PipelineStageOutput')


@dataclass
class BaseInputDataABC(TypeSafeDataclass, ABC, Generic[PipelineStageInput]):
    pass

@dataclass
class BaseOutputDataABC(TypeSafeDataclass, ABC, Generic[PipelineStageOutput]):
    pass


class AbstractPipelineStage(ABC, Generic[PipelineStageInput, PipelineStageOutput]):
    @abstractmethod
    def process(self, data: PipelineStageInput) -> PipelineStageOutput:
        pass


class AbstractPipeline(ABC):
    @abstractmethod
    def run(self) -> None:
        pass




@dataclass
class LoadDataOutput(BaseOutputDataABC):
    data: str


@dataclass
class PreprocessDataInput(BaseInputDataABC):
    data: str


@dataclass
class PreprocessDataOutput(BaseOutputDataABC):
    data: str


@dataclass
class AnalyzeDataInput(BaseInputDataABC):
    data: str


@dataclass
class AnalyzeDataOutput(BaseOutputDataABC):
    data: str
    analysis: str


class LoadDataStage(AbstractPipelineStage[None, LoadDataOutput]):
    def process(self, data: None = None) -> LoadDataOutput:
        return LoadDataOutput(data="raw data")


class PreprocessDataStage(AbstractPipelineStage[PreprocessDataInput, PreprocessDataOutput]):
    def process(self, data: PreprocessDataInput) -> PreprocessDataOutput:
        data.data = data.data.upper()
        return PreprocessDataOutput(data=data.data)


class AnalyzeDataStage(AbstractPipelineStage[AnalyzeDataInput, AnalyzeDataOutput]):
    def process(self, data: AnalyzeDataInput) -> AnalyzeDataOutput:
        analysis = f"Length of data: {len(data.data)}"
        return AnalyzeDataOutput(data=data.data, analysis=analysis)


class SaveResultsStage(AbstractPipelineStage[AnalyzeDataOutput, None]):
    def process(self, data: AnalyzeDataOutput) -> None:
        print("Results saved:", data.analysis)
        return None


class PipelineStage(Enum):
    LOAD_DATA = LoadDataStage()
    PREPROCESS_DATA = PreprocessDataStage()
    ANALYZE_DATA = AnalyzeDataStage()
    SAVE_RESULTS = SaveResultsStage()


class SimplePipeline(AbstractPipeline):
    def __init__(self):
        self.stages = PipelineStage

    def run(self) -> None:
        data = None
        for stage in self.stages:
            stage_instance = stage.value
            if isinstance(stage_instance, LoadDataStage):
                data = stage_instance.process()
            else:
                data = stage_instance.process(data)


if __name__ == "__main__":
    pipeline = SimplePipeline()
    pipeline.run()
