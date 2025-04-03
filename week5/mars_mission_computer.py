import random
import time


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
        self.set_env()
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        self.collected_data = []

    def get_time(self):
        t = time.localtime()
        return f'{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}'

    def average_env(self):
        if not self.collected_data:
            return

        avg = {}
        keys = self.collected_data[0].keys()

        for key in keys:
            # float으로 명시적 변환
            values = [float(data.get(key, 0)) for data in self.collected_data]
            total = sum(values)
            average = total / len(values)
            avg[key] = round(average, 3)

        print('\n[5분 평균 환경 데이터]')
        print('{')
        for idx, (key, value) in enumerate(avg.items()):
            comma = ',' if idx < len(avg) - 1 else ''
            print(f"    '{key}': {value}{comma}")
        print('}\n')

        with open('sensor_log.txt', 'a') as log_file:
            log_file.write('[5분 평균 환경 데이터]\n')
            for key, value in avg.items():
                log_file.write(f'{key}: {value}\n')
            log_file.write('\n')

        self.collected_data.clear()


    def get_sensor_data(self):
        count = 0
        try:
            while True:
                sensor_data = self.ds.get_env()
                self.env_values = sensor_data
                self.collected_data.append(sensor_data.copy())

                count += 1
                timestamp = self.get_time()

                print('{')
                for idx, (key, value) in enumerate(self.env_values.items()):
                    comma = ',' if idx < len(self.env_values) - 1 else ''
                    print(f"    '{key}': {repr(value)}{comma}")
                print('}')

                with open('sensor_log.txt', 'a') as log_file:
                    log_file.write(f'[Count {count}] {timestamp}\n')
                    for key, value in self.env_values.items():
                        log_file.write(f'{key}: {value}\n')
                    log_file.write('\n')

                if count % 60 == 0:
                    self.average_env()

                time.sleep(5)

        except KeyboardInterrupt:
            print('\nSystem stopped....')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
