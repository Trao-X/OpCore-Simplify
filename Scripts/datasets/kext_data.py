from Scripts.datasets import os_data

class KextInfo:
    def __init__(self, name, description, category, required = False, min_darwin_version = (), max_darwin_version = (), requires_kexts = [], conflict_group_id = None, github_repo = {}, download_info = {}):
        self.name = name
        self.description = description
        self.category = category
        self.required = required
        self.min_darwin_version = min_darwin_version or os_data.get_lowest_darwin_version()
        self.max_darwin_version = max_darwin_version or os_data.get_latest_darwin_version()
        self.requires_kexts = requires_kexts
        self.conflict_group_id = conflict_group_id
        self.github_repo = github_repo
        self.download_info = download_info
        self.checked = required

kexts = [
    KextInfo(
        name = "Lilu", 
        description = "For arbitrary kext, library, and program patching",
        category = "Required",
        required = True,
        github_repo = {
            "owner": "acidanthera",
            "repo": "Lilu"
        }
    ),
    KextInfo(
        name = "VirtualSMC", 
        description = "Advanced Apple SMC emulator in the kernel",
        category = "Required",
        required = True,
        github_repo = {
            "owner": "acidanthera",
            "repo": "VirtualSMC"
        }
    ),
    KextInfo(
        name = "SMCBatteryManager", 
        description = "Manages, monitors, and reports on battery status",
        category = "VirtualSMC Plugins",
        requires_kexts = ["VirtualSMC"]
    ),
    KextInfo(
        name = "SMCDellSensors", 
        description = "Enables fan monitoring and control on Dell computers",
        category = "VirtualSMC Plugins",
        requires_kexts = ["VirtualSMC"]
    ),
    KextInfo(
        name = "SMCLightSensor", 
        description = "Allows system utilize ambient light sensor device",
        category = "VirtualSMC Plugins",
        requires_kexts = ["VirtualSMC"]
    ),
    KextInfo(
        name = "SMCProcessor", 
        description = "Manages Intel CPU temperature sensors",
        category = "VirtualSMC Plugins",
        requires_kexts = ["VirtualSMC"]
    ),
    KextInfo(
        name = "SMCRadeonSensors", 
        description = "Provides temperature readings for AMD GPUs",
        category = "VirtualSMC Plugins",
        min_darwin_version = (18, 0, 0),
        requires_kexts = ["VirtualSMC"],
        github_repo = {
            "owner": "ChefKissInc",
            "repo": "SMCRadeonSensors"
        }
    ),
    KextInfo(
        name = "SMCSuperIO", 
        description = "Monitoring hardware sensors and controlling fan speeds",
        category = "VirtualSMC Plugins",
        requires_kexts = ["VirtualSMC"]
    ),
    KextInfo(
        name = "NootRX", 
        description = "The rDNA 2 dGPU support patch kext",
        category = "Graphics",
        min_darwin_version = (20, 5, 0),
        conflict_group_id = "GPU",
        github_repo = {
            "owner": "ChefKissInc",
            "repo": "NootRX"
        }
    ),
    KextInfo(
        name = "NootedRed", 
        description = "The AMD Vega iGPU support kext",
        category = "Graphics",
        min_darwin_version = (19, 0, 0),
        conflict_group_id = "GPU",
        github_repo = {
            "owner": "ChefKissInc",
            "repo": "NootedRed"
        }
    ),
    KextInfo(
        name = "WhateverGreen", 
        description = "Various patches necessary for GPUs are pre-supported",
        category = "Graphics",
        conflict_group_id = "GPU",
        github_repo = {
            "owner": "acidanthera",
            "repo": "WhateverGreen"
        }
    ),
    KextInfo(
        name = "AppleALC", 
        description = "Native macOS HD audio for not officially supported codecs",
        category = "Audio",
        github_repo = {
            "owner": "acidanthera",
            "repo": "AppleALC"
        },
        download_info = {
            "id": 223994507, 
            "url": "https://github.com/lzhoang2801/lzhoang2801.github.io/raw/main/public/extra-files/AppleALC-1.9.2-RELEASE.zip"
        }
    ),
    KextInfo(
        name = "AirportBrcmFixup", 
        description = "Patches required for non-native Broadcom Wi-Fi cards",
        category = "Wi-Fi",
        github_repo = {
            "owner": "acidanthera",
            "repo": "AirportBrcmFixup"
        }
    ),
    KextInfo(
        name = "AirportItlwm", 
        description = "Intel Wi-Fi drivers support the native macOS Wi-Fi interface",
        category = "Wi-Fi",
        conflict_group_id = "IntelWiFi",
        github_repo = {
            "owner": "OpenIntelWireless",
            "repo": "itlwm"
        }
    ),
    KextInfo(
        name = "IO80211FamilyLegacy", 
        description = "Enable legacy native Apple Wireless adapters",
        category = "Wi-Fi",
        min_darwin_version = (23, 0, 0),
        requires_kexts = ["IOSkywalkFamily"],
        download_info = {
            "id": 817294638, 
            "url": "https://github.com/dortania/OpenCore-Legacy-Patcher/raw/main/payloads/Kexts/Wifi/IO80211FamilyLegacy-v1.0.0.zip"
        }
    ),
    KextInfo(
        name = "IOSkywalkFamily", 
        description = "Enable legacy native Apple Wireless adapters",
        category = "Wi-Fi",
        min_darwin_version = (23, 0, 0),
        requires_kexts = ["IO80211FamilyLegacy"],
        download_info = {
            "id": 926584761, 
            "url": "https://github.com/dortania/OpenCore-Legacy-Patcher/raw/main/payloads/Kexts/Wifi/IOSkywalkFamily-v1.2.0.zip"
        }
    ),
    KextInfo(
        name = "itlwm", 
        description = "Intel Wi-Fi drivers. Spoofs as Ethernet and connects to Wi-Fi via Heliport",
        category = "Wi-Fi",
        conflict_group_id = "IntelWiFi",
        github_repo = {
            "owner": "OpenIntelWireless",
            "repo": "itlwm"
        }
    ),
    KextInfo(
        name = "BlueToolFixup", 
        description = "Patches Bluetooth stack to support third-party cards",
        category = "Bluetooth",
        min_darwin_version = (21, 0, 0),
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrcmPatchRAM"
        }
    ),
    KextInfo(
        name = "BrcmBluetoothInjector", 
        description = "Enables the Broadcom Bluetooth on/off switch on older versions",
        category = "Bluetooth",
        max_darwin_version = (20, 99, 99),
        requires_kexts = ["BrcmBluetoothInjector", "BrcmFirmwareData", "BrcmPatchRAM2", "BrcmPatchRAM3"],
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrcmPatchRAM"
        }
    ),
    KextInfo(
        name = "BrcmFirmwareData", 
        description = "Applies PatchRAM updates for Broadcom RAMUSB based devices",
        category = "Bluetooth",
        requires_kexts = ["BlueToolFixup", "BrcmBluetoothInjector", "BrcmPatchRAM2", "BrcmPatchRAM3"],
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrcmPatchRAM"
        }
    ),
    KextInfo(
        name = "BrcmPatchRAM2", 
        description = "Applies PatchRAM updates for Broadcom RAMUSB based devices",
        category = "Bluetooth",
        max_darwin_version = (18, 99, 99),
        requires_kexts = ["BlueToolFixup", "BrcmBluetoothInjector", "BrcmFirmwareData", "BrcmPatchRAM3"],
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrcmPatchRAM"
        }
    ),
    KextInfo(
        name = "BrcmPatchRAM3", 
        description = "Applies PatchRAM updates for Broadcom RAMUSB based devices",
        category = "Bluetooth",
        min_darwin_version = (19, 0, 0),
        requires_kexts = ["BlueToolFixup", "BrcmBluetoothInjector", "BrcmFirmwareData", "BrcmPatchRAM2"],
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrcmPatchRAM"
        }
    ),
    KextInfo(
        name = "IntelBluetoothFirmware", 
        description = "Uploads firmware to enable Intel Bluetooth support",
        category = "Bluetooth",
        requires_kexts = ["BlueToolFixup", "IntelBTPatcher", "IntelBluetoothInjector"],
        github_repo = {
            "owner": "OpenIntelWireless",
            "repo": "IntelBluetoothFirmware"
        }
    ),
    KextInfo(
        name = "IntelBTPatcher", 
        description = "Fixes Intel Bluetooth bugs for better connectivity",
        category = "Bluetooth",
        requires_kexts = ["BlueToolFixup", "IntelBluetoothFirmware", "IntelBluetoothInjector"]
    ),
    KextInfo(
        name = "IntelBluetoothInjector", 
        description = "Enables the Intel Bluetooth on/off switch on older versions",
        category = "Bluetooth",
        max_darwin_version = (20, 99, 99),
        requires_kexts = ["BlueToolFixup", "IntelBluetoothFirmware", "IntelBTPatcher"]
    ),
    KextInfo(
        name = "AppleIGB", 
        description = "Provides support for Intel's IGB Ethernet controllers",
        category = "Ethernet",
        github_repo = {
            "owner": "donatengit",
            "repo": "AppleIGB"
        },
        download_info = {
            "id": 736194363, 
            "url": "https://github.com/lzhoang2801/lzhoang2801.github.io/raw/main/public/extra-files/AppleIGB-v5.11.4.zip"
        }
    ),
    KextInfo(
        name = "AppleIGC", 
        description = "Provides support for Intel 2.5G Ethernet(i225/i226)", 
        category = "Ethernet",
        github_repo = {
            "owner": "SongXiaoXi",
            "repo": "AppleIGC"
        },
        download_info = {
            "id": 138279923, 
            "url": "https://github.com/SongXiaoXi/AppleIGC/releases/download/v1.5/AppleIGC.kext.zip"
        }
    ),
    KextInfo(
        name = "AtherosE2200Ethernet", 
        description = "Provides support for Atheros E2200 family", 
        category = "Ethernet",
        github_repo = {
            "owner": "Mieze",
            "repo": "AtherosE2200Ethernet"
        },
        download_info = {
            "id": 9746382, 
            "url": "https://github.com/Mieze/AtherosE2200Ethernet/releases/download/2.2.2/AtherosE2200Ethernet-V2.2.2.zip"
        }
    ),
    KextInfo(
        name = "IntelMausi", 
        description = "Intel Ethernet LAN driver for macOS",
        category = "Ethernet",
        github_repo = {
            "owner": "acidanthera",
            "repo": "IntelMausi"
        }
    ),
    KextInfo(
        name = "LucyRTL8125Ethernet", 
        description = "Provides support for Realtek RTL8125 family", 
        category = "Ethernet",
        github_repo = {
            "owner": "Mieze",
            "repo": "LucyRTL8125Ethernet"
        },
        download_info = {
            "id": 159470181, 
            "url": "https://github.com/Mieze/LucyRTL8125Ethernet/releases/download/v1.2.0d5/LucyRTL8125Ethernet-V1.2.0d5.zip"
        }
    ),
    KextInfo(
        name = "NullEthernet", 
        description = "Creates a Null Ethernet when no supported network hardware is present", 
        category = "Ethernet",
        github_repo = {
            "owner": "RehabMan",
            "repo": "os-x-null-ethernet"
        },
        download_info = {
            "id": 182736492, 
            "url": "https://bitbucket.org/RehabMan/os-x-null-ethernet/downloads/RehabMan-NullEthernet-2016-1220.zip"
        }
    ),
    KextInfo(
        name = "RealtekRTL8100", 
        description = "Provides support for Realtek RTL8100 family", 
        category = "Ethernet",
        github_repo = {
            "owner": "Mieze",
            "repo": "RealtekRTL8100"
        },
        download_info = {
            "id": 10460478, 
            "url": "https://github.com/lzhoang2801/lzhoang2801.github.io/raw/main/public/extra-files/RealtekRTL8100-v2.0.1.zip"
        }
    ),
    KextInfo(
        name = "RealtekRTL8111", 
        description = "Provides support for Realtek RTL8111/8168 family", 
        category = "Ethernet",
        github_repo = {
            "owner": "Mieze",
            "repo": "RTL8111_driver_for_OS_X"
        }
    ),
    KextInfo(
        name = "GenericUSBXHCI", 
        description = "Fixes USB 3.0 issues found on some Ryzen APU-based",
        category = "USB",
        github_repo = {
            "owner": "RattletraPM",
            "repo": "GUX-RyzenXHCIFix"
        },
        download_info = {
            "id": 120325166, 
            "url": "https://github.com/RattletraPM/GUX-RyzenXHCIFix/releases/download/v1.3.0b1-ryzenxhcifix/GenericUSBXHCI.kext.zip"
        }
    ),
    KextInfo(
        name = "XHCI-unsupported", 
        description = "Enables USB 3.0 support for unsupported xHCI controllers",
        category = "USB",
        github_repo = {
            "owner": "daliansky",
            "repo": "OS-X-USB-Inject-All"
        },
        download_info = {
            "id": 185465401, 
            "url": "https://github.com/daliansky/OS-X-USB-Inject-All/releases/download/v0.8.0/XHCI-unsupported.kext.zip"
        }
    ),
    KextInfo(
        name = "AlpsHID", 
        description = "Brings native multitouch support to the Alps I2C touchpad",
        category = "Input",
        requires_kexts = ["VoodooI2C"],
        github_repo = {
            "owner": "blankmac",
            "repo": "AlpsHID"
        },
        download_info = {
            "id": 69228327, 
            "url": "https://github.com/blankmac/AlpsHID/releases/download/v1.2/AlpsHID1.2_release.zip"
        }
    ),
    KextInfo(
        name = "VoodooPS2", 
        description = "Provides support for PS/2 keyboards, trackpads, and mouse",
        category = "Input",
        github_repo = {
            "owner": "acidanthera",
            "repo": "VoodooPS2"
        }
    ),
    KextInfo(
        name = "VoodooRMI", 
        description = "Synaptic Trackpad kext over SMBus/I2C",
        category = "Input",
        github_repo = {
            "owner": "VoodooSMBus",
            "repo": "VoodooRMI"
        },
        download_info = {
            "id": 13190749, 
            "url": "https://github.com/VoodooSMBus/VoodooRMI/releases/download/1.3.5/VoodooRMI-1.3.5-Release.zip"
        }
    ),
    KextInfo(
        name = "VoodooSMBus", 
        description = "i2c-i801 + ELAN SMBus Touchpad kext",
        category = "Input",
        min_darwin_version = (18, 0, 0),
        github_repo = {
            "owner": "VoodooSMBus",
            "repo": "VoodooSMBus"
        }
    ),
    KextInfo(
        name = "VoodooI2C", 
        description = "Intel I2C controller and slave device drivers",
        category = "Input",
        github_repo = {
            "owner": "VoodooI2C",
            "repo": "VoodooI2C"
        }
    ),
    KextInfo(
        name = "VoodooI2CAtmelMXT", 
        description = "A satellite kext for Atmel MXT I2C touchscreen",
        category = "Input",
        requires_kexts = ["VoodooI2C"]
    ),
    KextInfo(
        name = "VoodooI2CELAN", 
        description = "A satellite kext for ELAN I2C touchpads",
        category = "Input",
        requires_kexts = ["VoodooI2C"]
    ),
    KextInfo(
        name = "VoodooI2CFTE", 
        description = "A satellite kext for FTE based touchpads",
        category = "Input",
        requires_kexts = ["VoodooI2C"]
    ),
    KextInfo(
        name = "VoodooI2CHID", 
        description = "A satellite kext for HID I2C or ELAN1200+ input devices",
        category = "Input",
        requires_kexts = ["VoodooI2C"]
    ),
    KextInfo(
        name = "VoodooI2CSynaptics", 
        description = "A satellite kext for Synaptics I2C touchpads",
        category = "Input",
        requires_kexts = ["VoodooI2C"]
    ),
    KextInfo(
        name = "AsusSMC", 
        description = "Supports ALS, keyboard backlight, and Fn keys on ASUS laptops",
        category = "Brand Specific",
        github_repo = {
            "owner": "hieplpvip",
            "repo": "AsusSMC"
        },
        download_info = {
            "id": 41898282, 
            "url": "https://github.com/hieplpvip/AsusSMC/releases/download/1.4.1/AsusSMC-1.4.1-RELEASE.zip"
        }
    ),
    KextInfo(
        name = "BigSurface", 
        description = "A fully intergrated kext for all Surface related hardwares",
        category = "Brand Specific",
        github_repo = {
            "owner": "Xiashangning",
            "repo": "BigSurface"
        },
        download_info = {
            "id": 18528518, 
            "url": "https://github.com/Xiashangning/BigSurface/releases/download/v6.5/BigSurface.zip"
        }
    ),
    KextInfo(
        name = "CtlnaAHCIPort", 
        description = "Improves support for certain SATA controllers", 
        category = "Storage",
        download_info = {
            "id": 10460478, 
            "url": "https://github.com/lzhoang2801/lzhoang2801.github.io/raw/main/public/extra-files/CtlnaAHCIPort-v3.4.1.zip"
        }
    ),
    KextInfo(
        name = "NVMeFix", 
        description = "Addresses compatibility and performance issues with NVMe SSDs", 
        category = "Storage",
        min_darwin_version = (18, 0, 0),
        github_repo = {
            "owner": "acidanthera",
            "repo": "NVMeFix"
        }
    ),
    KextInfo(
        name = "RealtekCardReader", 
        description = "Realtek PCIe/USB-based SD card reader driver", 
        category = "SD Controller",
        min_darwin_version = (18, 0, 0),
        requires_kexts = ["RealtekCardReaderFriend"],
        github_repo = {
            "owner": "0xFireWolf",
            "repo": "RealtekCardReader"
        },
        download_info = {
            "id": 10460478, 
            "url": "https://github.com/0xFireWolf/RealtekCardReader/releases/download/v0.9.7/RealtekCardReader_0.9.7_006a845_RELEASE.zip"
        }
    ),
    KextInfo(
        name = "RealtekCardReaderFriend", 
        description = "Makes System Information recognize your Realtek card reader",
        category = "SD Controller",
        min_darwin_version = (18, 0, 0),
        max_darwin_version = (22, 99, 99),
        requires_kexts = ["RealtekCardReader"],
        github_repo = {
            "owner": "0xFireWolf",
            "repo": "RealtekCardReaderFriend"
        },
        download_info = {
            "id": 10460478, 
            "url": "https://github.com/0xFireWolf/RealtekCardReaderFriend/releases/download/v1.0.4/RealtekCardReaderFriend_1.0.4_e1e3301_RELEASE.zip"
        }
    ), 
    KextInfo(
        name = "AMFIPass", 
        description = "A replacement for amfi=0x80 boot argument",
        category = "Extras",
        min_darwin_version = (20, 0, 0), 
        download_info = {
            "id": 926491527, 
            "url": "https://github.com/dortania/OpenCore-Legacy-Patcher/raw/main/payloads/Kexts/Acidanthera/AMFIPass-v1.4.1-RELEASE.zip"
        }
    ),
    KextInfo(
        name = "AppleMCEReporterDisabler", 
        description = "Disables AppleMCEReporter.kext to prevent kernel panics", 
        category = "Extras",
        download_info = {
            "id": 738162736, 
            "url": "https://github.com/acidanthera/bugtracker/files/3703498/AppleMCEReporterDisabler.kext.zip"
        }
    ),
    KextInfo(
        name = "BrightnessKeys", 
        description = "Handler for brightness keys without DSDT patches",
        category = "Extras",
        github_repo = {
            "owner": "acidanthera",
            "repo": "BrightnessKeys"
        }
    ),
    KextInfo(
        name = "CpuTopologyRebuild", 
        description = "Optimizes the core configuration of Intel Alder Lake CPUs+",
        category = "Extras",
        github_repo = {
            "owner": "b00t0x",
            "repo": "CpuTopologyRebuild"
        },
        download_info = {
            "id": 13190749, 
            "url": "https://github.com/b00t0x/CpuTopologyRebuild/releases/download/1.1.0/CpuTopologyRebuild-1.1.0-RELEASE.zip"
        }
    ),
    KextInfo(
        name = "CryptexFixup", 
        description = "Various patches to install Rosetta cryptex",
        category = "Extras",
        min_darwin_version = (22, 0, 0),
        github_repo = {
            "owner": "acidanthera",
            "repo": "CryptexFixup"
        }
    ),
    KextInfo(
        name = "ECEnabler", 
        description = "Allows reading Embedded Controller fields over 1 byte long",
        category = "Extras",
        github_repo = {
            "owner": "1Revenger1",
            "repo": "ECEnabler"
        }
    ),
    KextInfo(
        name = "ForgedInvariant", 
        description = "The plug & play kext for syncing the TSC on AMD & Intel",
        category = "Extras",
        github_repo = {
            "owner": "ChefKissInc",
            "repo": "ForgedInvariant"
        }
    ),
    KextInfo(
        name = "HibernationFixup", 
        description = "Fixes hibernation compatibility issues",
        category = "Extras",
        github_repo = {
            "owner": "acidanthera",
            "repo": "HibernationFixup"
        }
    ),
    KextInfo(
        name = "RestrictEvents", 
        description = "Blocking unwanted processes and unlocking features",
        category = "Extras",
        github_repo = {
            "owner": "acidanthera",
            "repo": "RestrictEvents"
        }
    ),
    KextInfo(
        name = "RTCMemoryFixup", 
        description = "Emulate some offsets in your CMOS (RTC) memory",
        category = "Extras",
        github_repo = {
            "owner": "acidanthera",
            "repo": "RTCMemoryFixup"
        }
    )
]