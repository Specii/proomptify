import psutil


class SystemUsage:
    @staticmethod
    def cpu():
        cpu_percentage = psutil.cpu_percent(interval=1)
        cpu_frequency = psutil.cpu_freq()

        return cpu_frequency.current, cpu_frequency.max, cpu_percentage

    @staticmethod
    def ram():
        ram = psutil.virtual_memory()

        ram_used = round(ram.used / (1024 ** 3), 2)
        ram_total = round(ram.total / (1024 ** 3), 2)
        ram_percentage = round(ram.percent, 2)

        return ram_used, ram_total, ram_percentage

    @staticmethod
    def storage():
        storage = psutil.disk_usage('/')

        storage_used = round(storage.used / (1024 ** 3), 2)
        storage_total = round(storage.total / (1024 ** 3), 2)
        storage_percentage = round(storage.percent, 2)

        return storage_used, storage_total, storage_percentage
