# 파일 읽기 및 데이터 처리
def read_csv_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip().split(',') for line in lines]  # 쉼표로 분리
    except FileNotFoundError:
        print(f"Error: {filename} 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# 데이터를 정렬하고 필터링하는 함수
def process_inventory(data):
    if not data:
        return []
    
    header = data[0]  # 헤더 저장
    inventory = data[1:]  # 실제 데이터

    # 인화성(Flammability) 기준으로 내림차순 정렬
    try:
        inventory.sort(key=lambda x: float(x[4]), reverse=True)
    except ValueError:
        print("Error: Flammability 값을 숫자로 변환할 수 없습니다.")
        return []

    return [header] + inventory  # 헤더 포함하여 반환

# 인화성 지수가 0.7 이상인 항목을 필터링하는 함수
def filter_dangerous_items(data, threshold=0.7):
    return [row for row in data[1:] if float(row[4]) >= threshold]

# CSV 파일로 저장하는 함수
def save_to_csv(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for row in data:
                line = ",".join(row) + "\n"  # 쉼표로 구분하여 저장
                file.write(line)
        print(f"CSV 파일로 저장 완료: {filename}")
    except Exception as e:
        print(f"Error: {e}")

# 이진 파일로 저장 (struct 없이 구현)
def save_to_binary(filename, data):
    try:
        with open(filename, 'wb') as file:
            for row in data:
                line = ",".join(row) + "\n"  # 쉼표로 구분하여 저장
                file.write(line.encode('utf-8'))  # UTF-8로 인코딩하여 저장
        print(f"이진 파일로 저장 완료: {filename}")
    except Exception as e:
        print(f"Error: {e}")

# 이진 파일에서 읽어오기 (struct 없이 구현)
def read_from_binary(filename):
    try:
        with open(filename, 'rb') as file:
            lines = file.readlines()  # 모든 줄을 읽기
        return [line.decode('utf-8').strip().split(',') for line in lines]  # 쉼표로 분리하여 리스트로 변환
    except FileNotFoundError:
        print(f"Error: {filename} 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# 실행 코드
input_file = 'Mars_Base_Inventory_List.csv'
danger_file = 'Mars_Base_Inventory_danger.csv'
binary_file = 'Mars_Base_Inventory_List.bin'

# CSV 파일 읽기
csv_data = read_csv_file(input_file)
processed_data = process_inventory(csv_data)  # 데이터 정렬

if processed_data:
    # 인화성 지수가 0.7 이상인 항목 필터링
    dangerous_items = filter_dangerous_items(processed_data, 0.7)
    
    if dangerous_items:
        print("\n🔥 인화성 지수가 0.7 이상인 항목 🔥")
        for row in dangerous_items:
            print(f"물질: {row[0]}, 인화성 지수: {row[4]}")
        
        # 인화성 지수가 0.7 이상인 항목을 CSV 파일로 저장
        save_to_csv(danger_file, [csv_data[0]] + dangerous_items)
        
        # 모든 항목을 이진 파일로 저장
        save_to_binary(binary_file, processed_data)

        
        # 이진 파일에서 데이터 다시 읽기
        print("\n📂 이진 파일에서 데이터 다시 읽기 📂")
        binary_data = read_from_binary(binary_file)
        if binary_data:
            print("\n🔥 이진 파일에서 읽은 모든 항목 🔥")  # 모든 항목 출력
            for row in binary_data[1:]:  # 첫 번째 줄은 헤더이므로 제외
                print(f"물질: {row[0]}, 인화성 지수: {row[4]}")
    else:
        print("인화성 지수가 0.7 이상인 항목이 없습니다.")
