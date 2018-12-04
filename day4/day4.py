from collections import namedtuple, defaultdict

Date = namedtuple('Date', ['year', 'month', 'day'])
Time = namedtuple('Time', ['hour', 'minute'])

def read_input():
    f = open("input.txt")
    lines = []
    for line in f:
        str_date, str_time, desc = line.split(" ", 2)
        d = Date(int(str_date[1:5]), int(str_date[6:8]), int(str_date[9:11]))
        t = Time(int(str_time[0:2]), int(str_time[3:5]))
        lines.append((d, t, desc.strip()))
    return lines

def process(input_):
    result = defaultdict(lambda : [0] * 60)
    guard = None
    last_time = None

    for d,t,desc in input_:
        if desc.startswith('Guard'):
            guard = int(desc.split(" ")[1][1:])
            last_time = None
        if desc.startswith('falls'):
            last_time = t
        if desc.startswith('wakes'):
            for m in range(last_time.minute, t.minute):
                result[guard][m] += 1
    return result

def find_guard1(result):
    m = 0
    g = None

    for guard_id in result:
        t = sum(result[guard_id])
        if t > m:
            m = t
            g = guard_id

    m = 0
    minute = None
    for i, count in enumerate(result[g]):
        if count > m:
            m = count
            minute = i

    return g,minute

def find_guard2(result):
    g = 0
    m = 0
    minute = None
    for g_id, minutes in result.items():
        for i, count in enumerate(minutes):
            if count > m:
                m = count
                minute = i
                g = g_id

    return g,minute

def run():
    input_ = read_input()
    input_.sort()
    result = process(input_)
    guard, minute = find_guard1(result)
    print(guard * minute)
    guard, minute = find_guard2(result)
    print(guard * minute)

if __name__ == '__main__':
    run()
