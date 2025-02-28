# trajectory_base.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, overload

# 假设 scalar_t 已在 core/types.py 中定义为 float
scalar_t = float

# 定义泛型类型变量
Sample = TypeVar('Sample')
SampleDerivative = TypeVar('SampleDerivative')


class TrajectoryBase(Generic[Sample, SampleDerivative], ABC):
    """
    TrajectoryBase 是一个抽象基类，用于表示轨迹的基类。
    
    泛型参数:
        Sample: 轨迹在某个时间点的样本类型。
        SampleDerivative: 轨迹在某个时间点的导数样本类型。
    """

    def __init__(self):
        self._ts: scalar_t = 0.0
        self._tf: scalar_t = 0.0

    @overload
    @abstractmethod
    def evaluate(self, time: scalar_t) -> Sample:
        """
        在给定的时间点评估轨迹。
        
        Args:
            time (float): 时间点。
        
        Returns:
            Sample: 在该时间点的轨迹样本。
        """
        ...

    @overload
    @abstractmethod
    def evaluate(self, time_array: List[scalar_t]) -> List[Sample]:
        """
        在给定的时间数组中评估轨迹。
        
        Args:
            time_array (List[float]): 时间点数组。
        
        Returns:
            List[Sample]: 在每个时间点的轨迹样本列表。
        """
        ...

    @abstractmethod
    def evaluate(self, time):
        """
        抽象方法，用于在单个时间点或时间数组中评估轨迹。
        实现类需要根据输入参数的类型进行适当的处理。
        """
        pass

    @overload
    @abstractmethod
    def derivative(self, time: scalar_t, n: int) -> SampleDerivative:
        """
        在给定的时间点计算轨迹的第 n 阶导数。
        
        Args:
            time (float): 时间点。
            n (int): 导数的阶数。
        
        Returns:
            SampleDerivative: 在该时间点的第 n 阶导数样本。
        """
        ...

    @overload
    @abstractmethod
    def derivative(self, time_array: List[scalar_t], n: int) -> List[SampleDerivative]:
        """
        在给定的时间数组中计算轨迹的第 n 阶导数。
        
        Args:
            time_array (List[float]): 时间点数组。
            n (int): 导数的阶数。
        
        Returns:
            List[SampleDerivative]: 在每个时间点的第 n 阶导数样本列表。
        """
        ...

    @abstractmethod
    def derivative(self, time, n: int):
        """
        抽象方法，用于在单个时间点或时间数组中计算轨迹的第 n 阶导数。
        实现类需要根据输入参数的类型进行适当的处理。
        """
        pass

    def set_time_interval(self, ts: scalar_t, tf: scalar_t) -> None:
        """
        设置轨迹的时间区间。
        
        Args:
            ts (float): 起始时间。
            tf (float): 结束时间。如果 ts > tf，则 tf 被设置为 ts。
        """
        self._ts = ts
        self._tf = tf if ts <= tf else ts

    def ts(self) -> scalar_t:
        """
        获取轨迹的起始时间。
        
        Returns:
            float: 起始时间。
        """
        return self._ts

    def tf(self) -> scalar_t:
        """
        获取轨迹的结束时间。
        
        Returns:
            float: 结束时间。
        """
        return self._tf

    def duration(self) -> scalar_t:
        """
        计算轨迹的持续时间。
        
        Returns:
            float: 持续时间，非负。
        """
        return max(self._tf - self._ts, 0.0)


# 示例子类实现（可选）
class LinearTrajectory(TrajectoryBase[float, float]):
    """
    LinearTrajectory 是 TrajectoryBase 的一个具体实现，表示线性轨迹。
    
    轨迹定义为 y = a * t + b
    """
    def __init__(self, a: float, b: float):
        super().__init__()
        self.a = a
        self.b = b

    def evaluate(self, time) -> float:
        if isinstance(time, list):
            return [self.a * t + self.b for t in time]
        elif isinstance(time, float):
            return self.a * time + self.b
        else:
            raise TypeError("时间参数必须是 float 或 List[float]")

    def derivative(self, time, n: int) -> float:
        if n == 0:
            return self.evaluate(time)
        elif n == 1:
            if isinstance(time, list):
                return [self.a for _ in time]
            elif isinstance(time, float):
                return self.a
            else:
                raise TypeError("时间参数必须是 float 或 List[float]")
        else:
            if isinstance(time, list):
                return [0.0 for _ in time]
            elif isinstance(time, float):
                return 0.0
            else:
                raise TypeError("时间参数必须是 float 或 List[float]")
