# buffer.py

from threading import Lock
from typing import Generic, TypeVar, Optional

# 定义一个类型变量，表示Buffer可以存储的任意类型
T = TypeVar('T')

class Buffer(Generic[T]):
    """
    线程安全的缓冲区类，可以存储任意类型的数据。
    """

    def __init__(self) -> None:
        """
        初始化Buffer实例，设置初始数据为None，并创建一个锁用于线程同步。
        """
        self._data: Optional[T] = None
        self._lock = Lock()

    def push(self, data: T) -> None:
        """
        将数据存入缓冲区。线程安全的操作。

        Args:
            data (T): 要存入缓冲区的数据。
        """
        with self._lock:
            self._data = data
            # print(f"[Buffer] Pushed data: {data}")

    def get(self) -> Optional[T]:
        """
        从缓冲区获取当前存储的数据。线程安全的操作。

        Returns:
            Optional[T]: 当前存储的数据，如果缓冲区为空，则返回None。
        """
        with self._lock:
            # print(f"[Buffer] Retrieved data: {self._data}")
            return self._data

    def clear(self) -> None:
        """
        清空缓冲区中的数据。线程安全的操作。
        """
        with self._lock:
            # print(f"[Buffer] Clearing data. Previous data: {self._data}")
            self._data = None

    def __str__(self) -> str:
        """
        返回缓冲区当前状态的字符串表示。

        Returns:
            str: 缓冲区的字符串表示。
        """
        with self._lock:
            return f"Buffer(data={self._data})"

# 示例用法（可选）
if __name__ == "__main__":
    import threading
    import time

    # 创建Buffer实例，用于存储整数
    int_buffer = Buffer[int]()

    def producer(buffer: Buffer[int], data: int):
        buffer.push(data)
        time.sleep(0.1)

    def consumer(buffer: Buffer[int]):
        data = buffer.get()
        time.sleep(0.1)
        buffer.clear()

    # 创建生产者和消费者线程
    threads = []
    for i in range(5):
        t_prod = threading.Thread(target=producer, args=(int_buffer, i))
        t_cons = threading.Thread(target=consumer, args=(int_buffer,))
        threads.extend([t_prod, t_cons])

    # 启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

