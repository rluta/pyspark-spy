import dataclasses
import logging

from pyspark_spy.util import get_java_values, from_optional

logger = logging.getLogger(__name__)


class JavaClass:
    @classmethod
    def from_java(cls, jobj):
        try:
            return cls.try_convert(jobj)
        except:
            logger.exception('Error converting from java object to "%s". Java object fields: %s', cls.__name__, dir(jobj))
            raise

    @classmethod
    def try_convert(cls, jobj):
        raise NotImplementedError()


@dataclasses.dataclass
class JobEndEvent(JavaClass):
    jobId: int
    time: int
    jobResult: int

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype:  JobEndEvent
        """
        return cls(
            jobId=jobj.jobId(),
            time=jobj.time(),
            jobResult=jobj.jobResult().toString()
        )


@dataclasses.dataclass
class OutputMetrics(JavaClass):
    bytesWritten: int
    recordsWritten: int

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: OutputMetrics
        """
        return cls(**get_java_values(jobj, fields=cls.__annotations__.keys()))


@dataclasses.dataclass
class InputMetrics(JavaClass):
    bytesRead: int
    recordsRead: int

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: InputMetrics
        """
        return cls(**get_java_values(jobj, fields=cls.__annotations__.keys()))


@dataclasses.dataclass
class ShuffleReadMetrics(JavaClass):
    fetchWaitTime: int
    localBlocksFetched: int
    localBytesRead: int
    recordsRead: int
    remoteBlocksFetched: int
    remoteBytesRead: int
    remoteBytesReadToDisk: int
    totalBlocksFetched: int
    totalBytesRead: int

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: ShuffleReadMetrics
        """
        return cls(**get_java_values(jobj, fields=cls.__annotations__.keys()))


@dataclasses.dataclass
class ShuffleWriteMetrics(JavaClass):
    bytesWritten: int
    recordsWritten: int
    writeTime: int

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: ShuffleWriteMetrics
        """
        return cls(**get_java_values(jobj, fields=cls.__annotations__.keys()))


@dataclasses.dataclass
class TaskMetrics(JavaClass):
    diskBytesSpilled: int
    executorCpuTime: int
    executorDeserializeCpuTime: int
    executorDeserializeTime: int
    executorRunTime: int
    jvmGCTime: int
    memoryBytesSpilled: int
    peakExecutionMemory: int
    resultSerializationTime: int
    resultSize: int
    outputMetrics: OutputMetrics
    inputMetrics: InputMetrics
    shuffleReadMetrics: ShuffleReadMetrics
    shuffleWriteMetrics: ShuffleWriteMetrics

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: TaskMetrics
        """
        return cls(
            **get_java_values(jobj, fields=cls.__annotations__.keys(), exclude=(
                'inputMetrics', 'outputMetrics', 'shuffleReadMetrics', 'shuffleWriteMetrics'
            )),
            inputMetrics=InputMetrics.from_java(jobj.inputMetrics()),
            outputMetrics=OutputMetrics.from_java(jobj.outputMetrics()),
            shuffleReadMetrics=ShuffleReadMetrics.from_java(jobj.shuffleReadMetrics()),
            shuffleWriteMetrics=ShuffleWriteMetrics.from_java(jobj.shuffleWriteMetrics())
        )


@dataclasses.dataclass
class StageInfo(JavaClass):
    name: str
    numTasks: int
    stageId: int
    attemptNumber: int
    submissionTime: int
    completionTime: int
    failureReason: str
    taskMetrics: TaskMetrics

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: StageInfo
        """
        return cls(
            **get_java_values(jobj, fields=('name', 'numTasks', 'stageId', 'attemptNumber')),
            submissionTime=from_optional(jobj.submissionTime()),
            completionTime=from_optional(jobj.completionTime()),
            failureReason=from_optional(jobj.failureReason()),
            taskMetrics=TaskMetrics.from_java(jobj.taskMetrics()),
        )


@dataclasses.dataclass
class StageCompletedEvent(JavaClass):
    stageInfo: StageInfo

    @classmethod
    def try_convert(cls, jobj):
        """
        :rtype: StageCompletedEvent
        """
        return cls(
            stageInfo=StageInfo.from_java(jobj.stageInfo())
        )
