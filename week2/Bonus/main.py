import csv

log_file = "Bonus/mission_computer_main.log"  # 경로 수정
error_file = "Bonus/critical_issues.log"  # 경로 수정

logs = []

with open(log_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        logs.append(row)

logs.sort(reverse=True, key=lambda x: x[0])

print("=== 로그 (시간 역순) ===")
for log in logs:
    print(",".join(log))

critical_logs = [log for log in logs if "Oxygen tank" in log[2] or "explosion" in log[2]]

with open(error_file, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "event", "message"])
    writer.writerows(critical_logs)

print(f"\n⚠️ 문제가 되는 로그가 '{error_file}' 파일에 저장되었습니다.")
