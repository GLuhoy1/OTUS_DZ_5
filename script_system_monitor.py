import subprocess
from datetime import datetime

output = subprocess.check_output(['ps', 'aux']).decode('utf-8')

lines = output.split('\n')

users = set()
for line in lines[1:]:
    if line:
        user = line.split()[0]
        users.add(user)

total_processes = len(lines) - 2
user_processes = {user: 0 for user in users}
for line in lines[1:]:
    if line:
        user = line.split()[0]
        user_processes[user] += 1

memory_total = 0
cpu_total = 0
for line in lines[1:]:
    if line:
        parts = line.split()
        memory = float(parts[5])
        cpu = float(parts[2])
        memory_total += memory
        cpu_total += cpu

max_memory_process = ''
max_memory_usage = 0
for line in lines[1:]:
    if line:
        parts = line.split()
        memory = float(parts[5])
        command = parts[10]
        if memory > max_memory_usage:
            max_memory_usage = memory
            max_memory_process = command[:20] if len(command) > 20 else command

max_cpu_process = ''
max_cpu_usage = 0
for line in lines[1:]:
    if line:
        parts = line.split()
        cpu = float(parts[2])
        command = parts[10]
        if cpu > max_cpu_usage:
            max_cpu_usage = cpu
            max_cpu_process = command[:20] if len(command) > 20 else command

report = "Отчёт о состоянии системы:\n"
report += "Пользователи системы: '{}'\n".format("', '".join(users))
report += "Процессов запущено: {}\n".format(total_processes)
report += "Пользовательских процессов:\n"
for user, count in user_processes.items():
    report += "{}: {}\n".format(user, count)
report += "Всего памяти используется: {:.1f} mb\n".format(memory_total)
report += "Всего CPU используется: {:.1f}%\n".format(cpu_total)
report += "Больше всего памяти использует: {}\n".format(max_memory_process)
report += "Больше всего CPU использует: {}\n".format(max_cpu_process)

current_time = datetime.now().strftime("%d-%m-%Y-%H:%M")
filename = "{}-report.txt".format(current_time)

with open(filename, 'w') as f:
    f.write(report)

print(report)
