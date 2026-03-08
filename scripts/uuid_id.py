import uuid

def uuid_to_long():
    """将UUID转换为64位长整数"""
    # 生成UUID
    uid = uuid.uuid4()
    # 将UUID的16字节转换为两个64位整数，取第一个
    uid_bytes = uid.bytes
    # 取前8字节转换为64位整数
    high = int.from_bytes(uid_bytes[:8], byteorder='big', signed=False)
    # 取后8字节转换为64位整数
    low = int.from_bytes(uid_bytes[8:], byteorder='big', signed=False)
    # 合并两个整数（使用异或）
    return (high ^ low) & 0x7FFFFFFFFFFFFFFF  # 确保是正数


if __name__ == '__main__':
    # 测试
    print("生成10个UUID长整数:")
    for i in range(10):
        id_val = uuid_to_long()
        print(f"  {id_val}")
    
    print("\n检查唯一性:")
    ids = [uuid_to_long() for _ in range(10000)]
    print(f"  生成10000个ID")
    print(f"  唯一数量: {len(set(ids))}")
    print(f"  是否全部唯一: {len(ids) == len(set(ids))}")
