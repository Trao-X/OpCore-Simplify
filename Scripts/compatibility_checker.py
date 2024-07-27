from Scripts.datasets import chipset_data
from Scripts.datasets import cpu_data
from Scripts.datasets import pci_data
from Scripts import utils

class CompatibilityChecker:
    def __init__(self):
        self.utils = utils.Utils()
        self.latest_macos_version = 24

    def is_low_end_intel_cpu(self, processor_name):
        return any(brand in processor_name for brand in ["Celeron", "Pentium"])

    def check_cpu_compatibility(self, processor_name, instruction_set):
        if "x86-64" not in instruction_set or "SSE4" not in instruction_set:
            self.max_supported_macos_version = self.min_supported_macos_version = -1
            self.unsupported_devices.append(f"CPU: {processor_name}")
            return
        
        if "SSE4.2" not in instruction_set:
            self.min_supported_macos_version = 18
            if "SSE4.1" in instruction_set:
                self.max_supported_macos_version = 21

    def check_gpu_compatibility(self, motherboard_chipset, processor_name, instruction_set, gpu_info):
        supported_gpus = {}
        is_supported_discrete_gpu = False

        for gpu_name, gpu_props in gpu_info.items():
            gpu_manufacturer = gpu_props.get("Manufacturer")
            gpu_codename = gpu_props.get("GPU Codename")
            device_type = gpu_props.get("Device Type")
            is_supported_gpu = True

            if "Integrated GPU" in device_type:
                if "Intel" in gpu_manufacturer:
                    if self.utils.contains_any(cpu_data.IntelCPUGenerations, gpu_codename, end=12) and \
                        not self.is_low_end_intel_cpu(processor_name) and \
                        not "2000" in gpu_name and not "2500" in gpu_name:
                        self.min_supported_macos_version = max(17, self.min_supported_macos_version)
                        if "Sandy Bridge" in gpu_codename:
                            self.max_supported_macos_version = max(17, self.max_supported_macos_version if is_supported_discrete_gpu else -1)
                        elif "Ivy Bridge" in gpu_codename:
                            self.max_supported_macos_version = max(20, self.max_supported_macos_version if is_supported_discrete_gpu else -1)
                        elif "Haswell" in gpu_codename or "Broadwell" in gpu_codename:
                            self.max_supported_macos_version = max(21, self.max_supported_macos_version if is_supported_discrete_gpu else -1)
                        elif "Skylake" in gpu_codename or "Kaby Lake" in gpu_codename and not "-r" in gpu_codename.lower():
                            self.max_supported_macos_version = max(22, self.max_supported_macos_version if is_supported_discrete_gpu else -1)
                        elif "Amber Lake" in gpu_codename or "Whiskey Lake" in gpu_codename:
                            self.min_supported_macos_version = max(17, self.min_supported_macos_version if is_supported_discrete_gpu else -1)
                            self.max_supported_macos_version = self.latest_macos_version
                        elif not is_supported_discrete_gpu and "Comet Lake" in gpu_codename and self.utils.contains_any(chipset_data.IntelChipsets, motherboard_chipset, start=110, end=122):
                            self.max_supported_macos_version = self.min_supported_macos_version = -1
                        elif "Ice Lake" in gpu_codename:
                            self.min_supported_macos_version = max(19, self.min_supported_macos_version)
                            self.max_supported_macos_version = self.latest_macos_version
                        else:
                            self.max_supported_macos_version = self.latest_macos_version
                    else:
                        is_supported_gpu = False
                        if not is_supported_discrete_gpu:
                            self.max_supported_macos_version = self.min_supported_macos_version = -1
                elif "AMD" in gpu_manufacturer:
                    is_supported_gpu = gpu_props.get("Device ID") in pci_data.AMDGPUIDs
                    if is_supported_gpu:
                        self.max_supported_macos_version = self.latest_macos_version
                        self.min_supported_macos_version = max(19, self.min_supported_macos_version)
            elif "Discrete GPU" in device_type:
                if "AMD" in gpu_manufacturer:
                    is_supported_discrete_gpu = True

                    if "Navi 2" in gpu_codename:
                        if not "AVX2" in instruction_set:
                            self.max_supported_macos_version = min(21, self.max_supported_macos_version)
                        else:
                            if "Navi 23" in gpu_codename or "Navi 22" in gpu_codename:
                                self.min_supported_macos_version = max(21, self.min_supported_macos_version)
                            elif "Navi 21" in gpu_codename:
                                self.min_supported_macos_version = max(20, self.min_supported_macos_version)
                            else:
                                self.max_supported_macos_version = self.min_supported_macos_version = -1
                                is_supported_discrete_gpu = is_supported_gpu = False
                    elif "Navi 10" in gpu_codename:
                        self.min_supported_macos_version = max(19, self.min_supported_macos_version)
                    elif "Vega 20" in gpu_codename:
                        self.min_supported_macos_version = max(17, self.min_supported_macos_version)
                    elif "Vega 10" in gpu_codename or "Polaris" in gpu_codename or "550" in gpu_name:
                        self.min_supported_macos_version = max(17, self.min_supported_macos_version)
                    else:
                        self.max_supported_macos_version = self.min_supported_macos_version = -1
                        is_supported_discrete_gpu = is_supported_gpu = False
                elif "NVIDIA" in gpu_manufacturer:
                    is_supported_discrete_gpu = True

                    if "GK" in gpu_codename:
                        self.max_supported_macos_version = 20
                    elif "GP" in gpu_codename or "GM" in gpu_codename or "GF" in gpu_codename or "GT" in gpu_codename or gpu_codename.startswith("C"):
                        self.max_supported_macos_version = self.min_supported_macos_version = 17
                    else:
                        self.max_supported_macos_version = self.min_supported_macos_version = -1
                        is_supported_discrete_gpu = is_supported_gpu = False

            if not is_supported_gpu:
                self.unsupported_devices.append(f"{device_type}: {gpu_name}")
            else:
                supported_gpus[gpu_name] = gpu_props

        return supported_gpus

    def check_audio_compatibility(self, audio_info):
        supported_audio = {}
        audio_endpoint = None
        
        for audio_device, audio_props in audio_info.items():
            codec_id = audio_props.get("Codec ID")
            if "USB" in audio_props.get("Bus Type") or \
                codec_id.startswith("8086") or \
                codec_id.startswith("1002") or \
                codec_id in pci_data.CodecIDs:
                if codec_id in pci_data.CodecIDs:
                    supported_audio = {**{audio_device: audio_props}, **supported_audio}
                else:
                    supported_audio[audio_device] = audio_props
            else:
                if "Audio Endpoints" in audio_props:
                    audio_endpoint = ",".join(audio_props.get("Audio Endpoints"))
                self.unsupported_devices.append("Audio: {}{}".format(audio_device, "" if not audio_endpoint else f" ({audio_endpoint})"))
        
        return supported_audio

    def check_biometric_compatibility(self, hardware):
        biometric = hardware.get("Biometric", {})
        if biometric:
            for biometric_device, biometric_props in biometric.items():
                self.unsupported_devices.append(f"Biometric: {biometric_device}")
            
            del hardware["Biometric"]

    def check_network_compatibility(self, network_info):
        supported_network = {}
        
        for device_name, device_props in network_info.items():
            connection_name = device_props.get("Connection Name")
            bus_type = device_props.get("Bus Type")
            device_id = device_props.get("Device ID")
            is_device_supported = device_id in pci_data.NetworkIDs

            if bus_type.startswith("PCI"):
                if device_id in ["8086-125B", "8086-125C", "8086-125D", "8086-3102"]:
                    self.min_supported_macos_version = 19

            if not is_device_supported:
                self.unsupported_devices.append(f"{connection_name}: {device_name}")
            else:
                supported_network[device_name] = device_props

        return supported_network

    def check_storage_compatibility(self, storage_controller_info):
        supported_storage = {}

        for controller_name, controller_props in storage_controller_info.items():
            if "PCI" in controller_props.get("Bus Type"):
                device_id = controller_props.get("Device ID")
                if device_id in pci_data.IntelVMDIDs or device_id in pci_data.UnsupportedNVMeSSDIDs:
                    self.unsupported_devices.append("Storage: {}".format(pci_data.UnsupportedNVMeSSDIDs[device_id]))
                else:
                    supported_storage[controller_name] = controller_props
        
        return supported_storage

    def check_sd_controller_compatibility(self, hardware):
        sd_controller_props = hardware.get("SD Controller", {})

        if sd_controller_props:
            if sd_controller_props.get("Device ID") not in pci_data.RealtekCardReaderIDs:
                self.unsupported_devices.append("SD Controller: {}".format(sd_controller_props.get("Device Description")))
                hardware["SD Controller"] = {}

    def check_compatibility(self, hardware):
        self.max_supported_macos_version = self.latest_macos_version
        self.min_supported_macos_version = 17
        self.unsupported_devices = []

        self.check_cpu_compatibility(
            hardware.get("CPU").get("Processor Name"),
            hardware.get("CPU").get("Instruction Set")
        )

        if self.max_supported_macos_version != -1:
            hardware["GPU"] = self.check_gpu_compatibility(
                hardware.get("Motherboard").get("Motherboard Chipset"), 
                hardware.get("CPU").get("Processor Name"),
                hardware.get("CPU").get("Instruction Set"), 
                hardware.get("GPU")
            )
            if hardware.get("GPU"):
                hardware["Audio"] = self.check_audio_compatibility(hardware.get("Audio"))
                self.check_biometric_compatibility(hardware)
                hardware["Network"] = self.check_network_compatibility(hardware.get("Network"))
                hardware["Storage"]["Storage Controllers"] = self.check_storage_compatibility(hardware.get("Storage").get("Storage Controllers"))
                self.check_sd_controller_compatibility(hardware)

        hardware["Compatibility"] = {
            "macOS Version": {
                "Max Version": self.max_supported_macos_version,
                "Min Version": self.min_supported_macos_version
            },
            "Unsupported Devices": self.unsupported_devices
        }

        return hardware