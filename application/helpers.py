# Formats seconds to HH:MM:SS
def seconds_to_readable(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"


# Converts bytes to human-readable format
def bytes_to_readable(num: int) -> str:
    step_unit = 1000.0
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
    return "%3.1f %s" % (num, "PB")