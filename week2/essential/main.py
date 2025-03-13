import csv

log_file = "essential/mission_computer_main.log" 
error_file = "essential/critical_issues.log" 

logs1 = []
logs2 = []

print("Hello Mars")

with open(log_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        logs1.append(row)

with open(log_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        logs2.append(row)

logs2.sort(reverse=True, key=lambda x: x[0])

print("=== 로그 (시간 정순) ===")
for log in logs1:
    print(",".join(log))
print("=== 로그 (시간 역순) ===")
for log in logs2:
    print(",".join(log))

critical_logs = [log for log in logs2 if "Oxygen tank" in log[2] or "explosion" in log[2] or "powered down" in log[2]]

with open(error_file, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "event", "message"])
    writer.writerows(critical_logs)

print(f"\n⚠️ 문제가 되는 로그가 '{error_file}' 파일에 저장되었습니다.")
