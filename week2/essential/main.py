import csv

log_file = "essential/mission_computer_main.log"  # 경로 변경
error_file = "essential/critical_issues.log"  # 경로 변경

logs = []

with open(log_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        logs.append(row)

# 로그를 시간 역순으로 정렬
logs.sort(reverse=True, key=lambda x: x[0])

print("=== 로그 (시간 역순) ===")
for log in logs:
    print(",".join(log))

# 특정 키워드가 포함된 중요 로그 필터링
critical_logs = [log for log in logs if "Oxygen tank" in log[2] or "explosion" in log[2]]

# 필터링된 로그를 새로운 파일에 저장
with open(error_file, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "event", "message"])
    writer.writerows(critical_logs)

print(f"\n⚠️ 문제가 되는 로그가 '{error_file}' 파일에 저장되었습니다.")
