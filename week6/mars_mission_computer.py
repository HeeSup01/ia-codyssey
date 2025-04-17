
import random
import time
import platform
import os

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
        self.info_fields = []
        self.load_fields = []
        self._memory_mode = 'size'
        self._load_settings()

    def _load_settings(self):
        try:
            with open('setting.txt', 'r') as f:
                for line in f:
                    if line.startswith('info:'):
                        self.info_fields = [key.strip() for key in line.split(':')[1].split(',')]
                    elif line.startswith('load:'):
                        self.load_fields = [key.strip() for key in line.split(':')[1].split(',')]
        except Exception as e:
            print(f'setting.txt 읽기 실패: {e}')

    def get_time(self):
        t = time.localtime()
        return f'{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}'

    def average_env(self):
        if not self.collected_data:
            return

        avg = {}
        keys = self.collected_data[0].keys()

        for key in keys:
            values = [float(data.get(key, 0)) for data in self.collected_data]
            total = sum(values)
            average = total / len(values)
            avg[key] = round(average, 3)

        print('\n[5분 평균 환경 데이터]')
        print('{')
        for idx, (key, value) in enumerate(avg.items()):
            comma = ',' if idx < len(avg) - 1 else ''
            print(f"    '{key}': {repr(value)}{comma}")
        print('}')

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

    def get_mission_computer_info(self):
        try:
            self._memory_mode = 'size'
            full_info = {
                'operating_system': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_size': self._get_memory_info()
            }
            info = {k: full_info[k] for k in self.info_fields if k in full_info}

            print('[미션 컴퓨터 정보]')
            print('{')
            for idx, (key, value) in enumerate(info.items()):
                comma = ',' if idx < len(info) - 1 else ''
                print(f"    '{key}': '{value}'{comma}")
            print('}')
            return info
        except Exception as e:
            print(f'Error getting system info: {e}')
            return {}

    def get_mission_computer_load(self):
        try:
            self._memory_mode = 'usage'
            full_load = {
                'cpu_load': os.getloadavg()[0],
                'memory_usage': self._get_memory_usage()
            }
            load = {k: full_load[k] for k in self.load_fields if k in full_load}

            print('[미션 컴퓨터 부하]')
            print('{')
            for idx, (key, value) in enumerate(load.items()):
                comma = ',' if idx < len(load) - 1 else ''
                if isinstance(value, str):
                    print(f"    '{key}': '{value}'{comma}")
                else:
                    print(f"    '{key}': {value}{comma}")
            print('}')
            return load
        except Exception as e:
            print(f'Error getting system load: {e}')
            return {}

    def _get_memory_info(self):
        if platform.system() == 'Linux':
            try:
                with open('/proc/meminfo', 'r') as mem:
                    total_line = mem.readline()
                    total_kb = int(total_line.split()[1])
                    return f'{total_kb // 1024} MB'
            except Exception:
                return 'Unknown'
        elif platform.system() == 'Darwin':
            try:
                mem_bytes = int(os.popen('sysctl -n hw.memsize').read().strip())
                mem_mb = mem_bytes // 1024 // 1024
                return f'{mem_mb} MB'
            except Exception:
                return 'Unknown'
        return 'Unknown'

    def _get_memory_usage(self):
        if platform.system() == 'Linux':
            try:
                with open('/proc/meminfo', 'r') as mem:
                    lines = mem.readlines()
                    total = int(lines[0].split()[1])
                    available = int(lines[2].split()[1])
                    used = total - available
                    return f'{used // 1024} MB used / {total // 1024} MB total'
            except Exception:
                return 'Unknown'
        elif platform.system() == 'Darwin':
            return self._get_memory_usage_mac()
        return 'Unknown'

    def _get_memory_usage_mac(self):
        try:
            with os.popen('vm_stat') as f:
                lines = f.readlines()

            page_size = 4096
            stats = {}
            for line in lines:
                if ':' not in line:
                    continue
                try:
                    key, value = line.split(':')
                    value = value.strip().split(' ')[0].replace('.', '')
                    stats[key.strip()] = int(value)
                except ValueError:
                    continue

            used = (
                stats.get('Pages active', 0)
                + stats.get('Pages inactive', 0)
                + stats.get('Pages speculative', 0)
                + stats.get('Pages wired down', 0)
            )
            used_mb = used * page_size // 1024 // 1024

            # 정확한 고정 total 가져오기
            mem_bytes = int(os.popen('sysctl -n hw.memsize').read().strip())
            total_mb = mem_bytes // 1024 // 1024

            return f'{used_mb} MB used / {total_mb} MB total'
        except Exception as e:
            print(f'vm_stat 분석 오류: {e}')
            return 'Unknown'


if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
    # runComputer.get_sensor_data()
