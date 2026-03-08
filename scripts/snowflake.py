#!/usr/bin/env python3
"""
雪花算法 ID 生成器
生成趋势递增的唯一ID
"""

import time
import threading


class Snowflake:
    """
    雪花算法 ID 生成器
    
    结构: 0(1bit) | 时间戳(41bit) | 机器ID(10bit) | 序列号(12bit)
    
    支持:
    - 每秒生成约 4096 * 1024 = 419万个ID
    - 时间戳可用约 69 年
    """
    
    # 起始时间戳 (2024-01-01)
    EPOCH = 1704067200000
    
    # 各部分的位数
    WORKER_ID_BITS = 10
    SEQUENCE_BITS = 12
    
    # 最大值
    MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1  # 1023
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1    # 4095
    
    # 位移
    WORKER_ID_SHIFT = SEQUENCE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    
    def __init__(self, worker_id: int = 0):
        """
        初始化
        
        Args:
            worker_id: 机器ID (0-1023)
        """
        if not (0 <= worker_id <= self.MAX_WORKER_ID):
            raise ValueError(f"worker_id must be between 0 and {self.MAX_WORKER_ID}")
        
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
    
    def _current_timestamp(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待下一毫秒"""
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp
    
    def generate(self) -> int:
        """
        生成唯一ID
        
        Returns:
            64位整数ID
        """
        with self.lock:
            timestamp = self._current_timestamp()
            
            # 时钟回拨检查
            if timestamp < self.last_timestamp:
                raise Exception(f"Clock moved backwards. Refusing to generate ID for {self.last_timestamp - timestamp} milliseconds")
            
            # 同一毫秒内
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 不同毫秒，序列号重置
                self.sequence = 0
            
            self.last_timestamp = timestamp
            
            # 组合ID
            id_value = ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
                       (self.worker_id << self.WORKER_ID_SHIFT) | \
                       self.sequence
            
            return id_value
    
    def generate_str(self) -> str:
        """生成字符串格式的ID"""
        return str(self.generate())


# 全局单例
def get_snowflake(worker_id: int = 0) -> Snowflake:
    """获取雪花算法实例"""
    if not hasattr(get_snowflake, '_instance'):
        get_snowflake._instance = Snowflake(worker_id)
    return get_snowflake._instance


if __name__ == '__main__':
    # 测试
    sf = Snowflake(worker_id=1)
    
    print("生成10个ID:")
    for i in range(10):
        id_val = sf.generate()
        print(f"  {id_val}")
    
    print("\n生成10000个ID耗时:")
    import time
    start = time.time()
    ids = [sf.generate() for _ in range(10000)]
    elapsed = time.time() - start
    print(f"  耗时: {elapsed:.3f}秒")
    print(f"  每秒: {10000/elapsed:.0f}个")
    print(f"  是否唯一: {len(ids) == len(set(ids))}")
