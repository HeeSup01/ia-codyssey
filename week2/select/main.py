import json

log_file = 'Select/mission_computer_main.log'
json_file = 'Select/mission_computer_main.json'

logs = []

try:
    with open(log_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                logs.append({'timestamp': parts[0], 'event': parts[1], 'message': parts[2]})

except FileNotFoundError:
    print(f'파일 "{log_file}"을 찾을 수 없습니다.')
except Exception as e:
    print(f'오류 발생: {e}')

# 로그를 시간 역순으로 정렬
logs.sort(reverse=True, key=lambda x: x['timestamp'])

# JSON 파일로 저장
try:
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(logs, file, ensure_ascii=False, indent=4)
    print(f'✅ 로그가 "{json_file}" 파일로 저장되었습니다.')
except Exception as e:
    print(f'JSON 저장 중 오류 발생: {e}')

# 보너스 과제: 특정 키워드 검색 기능
def search_logs(keyword):
    results = [log for log in logs if keyword.lower() in log['message'].lower()]
    
    if results:
        print(f'\n🔎 "{keyword}" 관련 로그:')
        for log in results:
            print(f"{log['timestamp']} - {log['event']} - {log['message']}")
    else:
        print(f'\n🔍 "{keyword}" 관련 로그가 없습니다.')

# 테스트 (예: 'Oxygen' 포함된 로그 검색)
search_logs('Oxygen')
