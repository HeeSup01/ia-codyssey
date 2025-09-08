import struct

# CSV 파일 읽기 함수
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

    # 인화성 기준으로 내림차순 정렬
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
                line = ",".join(row) + "\n" 
                file.write(line)
        print(f"CSV 파일로 저장 완료: {filename}")
    except Exception as e:
        print(f"Error: {e}")

# 이진 파일로 저장
def save_to_binary(filename, data):
    try:
        with open(filename, 'wb') as file:
            for row in data[1:]:  # 헤더를 제외한 실제 데이터만 저장
                # 각 항목을 이진 형식으로 변환
                name = row[0]
                density = row[1]
                specific_gravity = row[2]
                strength = row[3]
                flammability = float(row[4])  # 실수형으로 변환
                
                # 문자열을 바이트로 변환 (고정 크기 100 bytes로 설정)
                name_bytes = name.encode('utf-8')
                density_bytes = density.encode('utf-8')
                specific_gravity_bytes = specific_gravity.encode('utf-8')
                strength_bytes = strength.encode('utf-8')
                
                # 각 필드의 길이를 고정 크기 100 bytes로 맞추기
                name_bytes = name_bytes.ljust(100, b'\0')
                density_bytes = density_bytes.ljust(100, b'\0')
                specific_gravity_bytes = specific_gravity_bytes.ljust(100, b'\0')
                strength_bytes = strength_bytes.ljust(100, b'\0')
                
                # 인화성 지수는 실수형 (4 bytes)
                # 데이터를 struct로 패킹하여 이진 형식으로 저장
                data_to_write = struct.pack('100s100s100s100sf', name_bytes, density_bytes, specific_gravity_bytes, strength_bytes, flammability)
                
                # 이진 파일에 데이터 쓰기
                file.write(data_to_write)
                
        print(f"이진 파일로 저장 완료: {filename}")
    except Exception as e:
        print(f"Error: {e}")

# 이진 파일에서 읽어오기
def read_from_binary(filename):
    try:
        with open(filename, 'rb') as file:
            while True:
                # 한 항목의 크기 (100 bytes * 4개 문자열 + 4 bytes 실수형 데이터)
                data = file.read(100 * 4 + 4)
                
                if not data:
                    break  # 파일 끝에 도달하면 종료
                
                # unpack()을 사용하여 이진 데이터를 구조화된 데이터로 변환
                name, density, specific_gravity, strength, flammability = struct.unpack('100s100s100s100sf', data)
                
                # 바이트로 저장된 문자열을 디코딩
                name = name.decode('utf-8').rstrip('\0')
                density = density.decode('utf-8').rstrip('\0')
                specific_gravity = specific_gravity.decode('utf-8').rstrip('\0')
                strength = strength.decode('utf-8').rstrip('\0')
                
                print(f"물질: {name}, 인화성 지수: {flammability}")
    
    except FileNotFoundError:
        print(f"Error: {filename} 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"Error: {e}")


# 실행 코드
input_file = 'Mars_Base_Inventory_List.csv'
danger_file = 'Mars_Base_Inventory_danger.csv'
binary_file = 'Mars_Base_Inventory_List.bin'


# CSV 파일 읽기
csv_data = read_csv_file(input_file)
processed_data = process_inventory(csv_data)

if processed_data:
    # 인화성 지수가 0.7 이상인 항목 필터링
    dangerous_items = filter_dangerous_items(processed_data, 0.7)
    
    if dangerous_items:
        print("\n🔥 인화성 지수가 0.7 이상인 항목 🔥")
        for row in dangerous_items:
            print(f"물질: {row[0]}, 인화성 지수: {row[4]}")

        print("\n🔥 csv 🔥")
        for row in processed_data :
            print(f"물질: {row[0]}, 인화성 지수: {row[4]}")           

            
        
        # 인화성 지수가 0.7 이상인 항목을 CSV 파일로 저장
        save_to_csv(danger_file, [csv_data[0]] + dangerous_items)
        
        # 모든 항목을 이진 파일로 저장
        save_to_binary(binary_file, processed_data)

        # 이진 파일에서 데이터 다시 읽기
        print("\n📂 이진 파일에서 데이터 다시 읽기 📂")
        read_from_binary(binary_file)
    else:
        print("인화성 지수가 0.7 이상인 항목이 없습니다.")
