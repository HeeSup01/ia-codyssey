
def read_log_file(filename):
    try:
        with open(f"essential/{filename}", 'r', encoding='utf-8') as file:
            log_data = file.read()
            print(log_data)  # 전체 로그 내용 출력
    except FileNotFoundError:
        print(f"파일 '{filename}'을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    log_filename = "mission_computer_main.log"
    read_log_file(log_filename)
