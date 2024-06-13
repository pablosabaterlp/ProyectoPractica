def read_line(path, line):
    with open(path, 'r') as file:
        lines = file.readlines()
        if 0 <= line < len(lines):
            return lines[line].strip()
        else:
            raise ValueError("Line Number out of Range")