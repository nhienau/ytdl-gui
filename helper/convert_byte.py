def convert_byte(byte):
    unit = ["B", "KiB", "MiB", "GiB"]
    index = 0
    result = byte
    while result > 1024 and index < len(unit):
        result /= 1024
        index += 1
    return {
        "result": result,
        "unit": unit[index]
    }
