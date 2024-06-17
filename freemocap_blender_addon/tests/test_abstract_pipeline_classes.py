from dataclasses import dataclass

from freemocap_blender_addon.pipelines.abstract_base_classes import BasePipelineIOABC, AbstractPipelineStage, \
    AbstractPipeline


@dataclass
class SampleInput1(BasePipelineIOABC):
    value: int


@dataclass
class SampleOutput1(BasePipelineIOABC):
    value: int


@dataclass
class SampleOutput2(BasePipelineIOABC):
    result: int


@dataclass
class SamplePipelineStage1(AbstractPipelineStage[SampleInput1, SampleOutput1]):
    def process(self, data: SampleInput1) -> SampleOutput1:
        return SampleOutput1(value=data.value + 1)


@dataclass
class SamplePipelineStage2(AbstractPipelineStage[SampleOutput1, SampleOutput2]):
    def process(self, data: SampleOutput1) -> SampleOutput2:
        return SampleOutput2(result=data.value + 2)


@dataclass
class OneStageSamplePipeline(AbstractPipeline):
    stages = [SamplePipelineStage1()]

    def run(self, data: SampleInput1) -> SampleOutput1:
        for stage in self.stages:
            data = stage.process(data)
        return data


@dataclass
class TwoStageSamplePipeline(AbstractPipeline):
    stages = [SamplePipelineStage1(), SamplePipelineStage2()]

    def run(self, data: SampleInput1) -> SampleOutput2:
        for stage in self.stages:
            data = stage.process(data)
        return data


# Tests

def test_sample_input_data_initialization() -> None:
    """Test initialization of SampleInputData"""
    data: SampleInput1 = SampleInput1(value=10)
    assert data.value == 10


def test_sample_output_data_initialization() -> None:
    """Test initialization of SampleOutputData"""
    data: SampleOutput1 = SampleOutput1(value=20)
    assert data.value == 20


def test_sample_pipeline_stage_process() -> None:
    """Test processing in SamplePipelineStage"""
    stage: SamplePipelineStage1 = SamplePipelineStage1()
    input_data: SampleInput1 = SampleInput1(value=5)
    output_data: SampleOutput1 = stage.process(input_data)
    assert output_data.value == 6


def test_one_stage_pipeline_run() -> None:
    """Test running the SamplePipeline with one stage"""
    pipeline = OneStageSamplePipeline()
    result: SampleOutput1 = pipeline.run(data=SampleInput1(value=0))
    assert isinstance(result, SampleOutput1)
    assert result.value == 1


def test_two_stage_pipeline_run() -> None:
    """Test running the SamplePipeline with multiple stages"""
    stage1: SamplePipelineStage1 = SamplePipelineStage1()
    stage2: SamplePipelineStage2 = SamplePipelineStage2()
    pipeline: TwoStageSamplePipeline = TwoStageSamplePipeline()
    result: SampleOutput2 = pipeline.run(data=SampleInput1(value=0))
    assert isinstance(result, SampleOutput2)
    assert result.result == 3
