import random

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 1)
    
    def get_env(self):
        current_time = self.get_time()
        log_data = f"{current_time}\n" + "\n".join([f"{key}: {value}" for key, value in self.env_values.items()]) + "\n"
        
        with open('sensor_log.txt', 'a') as log_file:
            log_file.write(log_data + "\n")
        
        return self.env_values
    
    def get_time(self):
        t = __import__('time').localtime()
        return f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"

# DummySensor 클래스 인스턴스 생성
ds = DummySensor()

# 환경 값 설정
ds.set_env()

# 환경 값 출력
sensor_info = {
    'mars_base_internal_temperature': '화성 기지 내부 온도 (18~30도)',
    'mars_base_external_temperature': '화성 기지 외부 온도 (0~21도)',
    'mars_base_internal_humidity': '화성 기지 내부 습도 (50~60%)',
    'mars_base_external_illuminance': '화성 기지 외부 광량 (500~715 W/m2)',
    'mars_base_internal_co2': '화성 기지 내부 이산화탄소 농도 (0.02~0.1%)',
    'mars_base_internal_oxygen': '화성 기지 내부 산소 농도 (4%~7%)'
}

print(ds.get_time())
for key, value in ds.get_env().items():
    print(f"{sensor_info.get(key, key)}: {value}")
