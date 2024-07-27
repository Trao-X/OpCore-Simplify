from Scripts import github
from Scripts import resource_fetcher
from Scripts import utils
import os

class CodecLayouts:
    def __init__(self):
        self.github = github.Github()
        self.fetcher = resource_fetcher.ResourceFetcher(self.github.headers)
        self.utils = utils.Utils()
        self.vendors = {
            "11D4": ["AD", "AnalogDevices"],
            "10EC": ["ALC", "Realtek"],
            "1102": ["CA", "Creative"],
            "1013": ["CS", "CirrusLogic"],
            "14F1": ["CX", "Conexant"],
            "111D": ["IDT"],
            "8384": ["STAC", "SigmaTel"],
            "1106": ["VT", "VIA"]
        }
        
    def get_layout_ids_from_applealc_repo(self):
        # Define the GitHub API URL for the AppleALC repository contents
        url = "https://api.github.com/repos/acidanthera/AppleALC/contents/Resources"

        self.github.check_ratelimit()
        
        # Dictionary to store sound codec information
        sound_codec_info = {}
        
        # Retrieve content information from the GitHub repository
        content = self.fetcher.fetch_and_parse_content(url, "json")
        
        # Iterate through folders in the content
        for folder in content:
            codec_folder_name = folder["name"]
            
            if "." in codec_folder_name:
                continue
            
            # Identify vendor based on the vendor information
            vendor_id = next((id for id, vendor in self.vendors.items() if vendor[0] in codec_folder_name), None)
            
            if not vendor_id:
                # Skip if vendor ID is not found
                print(f"Unknown vendor for codec: {codec_folder_name}")
                continue
            
            # Extract vendor name from vendor information
            vendor_name = self.vendors[vendor_id][-1]
            
            # Build the raw URL for the Info.plist file
            raw_url = f"https://raw.githubusercontent.com/acidanthera/AppleALC/master/Resources/{codec_folder_name}/Info.plist"
            
            # Retrieve content from the Info.plist file and parse as plist
            info = self.fetcher.fetch_and_parse_content(raw_url, "json")
            
            # Extract relevant information from the Info.plist
            codec_id_hex = self.utils.int_to_hex(info["CodecID"]).zfill(4)
            formatted_codec_name = "{} {}".format(vendor_name, info["CodecName"])
            layout_ids = sorted([int(layouts["Id"]) for layouts in info["Files"]["Layouts"]])
            pci_id = f"{vendor_id}-{codec_id_hex}".upper()

            sound_codec_info[pci_id] = layout_ids
        
        # Sort sound codec information by name
        sorted_sound_codec_info = dict(sorted(sound_codec_info.items(), key=lambda item: item[1]["Name"]))
        
        return sorted_sound_codec_info
    
    def get_layout_ids_from_applealc_kext(self, applealc_path):
        if not os.path.exists(applealc_path):
            return {}

        plist_path = os.path.join(applealc_path, "Contents", "Info.plist")
        plist_data = self.utils.read_file(plist_path)

        if not plist_data:
            return {}

        codec_layouts = {}

        hda_config_defaults = plist_data.get("IOKitPersonalities", {}).get("as.vit9696.AppleALC", {}).get("HDAConfigDefault", [])
        for layout in hda_config_defaults:
            codec_id_hex = self.utils.int_to_hex(layout.get("CodecID", 0)).zfill(8)
            formatted_codec_id = f"{codec_id_hex[:4]}-{codec_id_hex[-4:]}"
            layout_id = layout.get("LayoutID")
            if layout_id is not None:
                if formatted_codec_id not in codec_layouts:
                    codec_layouts[formatted_codec_id] = []
                codec_layouts[formatted_codec_id].append(layout_id)
        
        # Sort the layout IDs for each codec
        for codec_id in codec_layouts:
            codec_layouts[codec_id] = sorted(codec_layouts[codec_id])

        return codec_layouts

data = {
    "10EC-0295": [
        1,
        3,
        11,
        13,
        14,
        15,
        21,
        22,
        23,
        24,
        28,
        33,
        69,
        75,
        77
    ],
    "10EC-0298": [
        3,
        11,
        13,
        15,
        16,
        21,
        22,
        25,
        28,
        29,
        30,
        32,
        33,
        47,
        66,
        72,
        94,
        99
    ],
    "10EC-1168": [
        1,
        2,
        3,
        5,
        7,
        8,
        11,
        13,
        15,
        20,
        21,
        99
    ],
    "10EC-0256": [
        5,
        11,
        12,
        13,
        14,
        16,
        17,
        19,
        20,
        21,
        22,
        23,
        24,
        28,
        33,
        38,
        56,
        57,
        66,
        67,
        68,
        69,
        70,
        76,
        77,
        88,
        95,
        97,
        99
    ],
    "10EC-0282": [
        3,
        4,
        13,
        21,
        22,
        27,
        28,
        29,
        30,
        41,
        43,
        51,
        69,
        76,
        86,
        127
    ],
    "10EC-0269": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        44,
        45,
        47,
        55,
        58,
        66,
        69,
        76,
        77,
        88,
        91,
        93,
        99,
        100,
        111,
        127,
        128,
        138,
        188
    ],
    "111D-7695": [
        11,
        12,
        14
    ],
    "14F1-5098": [
        20,
        21,
        23,
        28
    ],
    "1102-0011": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        9,
        10,
        11,
        12,
        99
    ],
    "1013-4210": [
        13
    ],
    "1013-4213": [
        28
    ],
    "11D4-1884": [
        11
    ],
    "11D4-1984": [
        11
    ],
    "11D4-194A": [
        11,
        13,
        44
    ],
    "11D4-1988": [
        12
    ],
    "11D4-198B": [
        5,
        7,
        12
    ],
    "11D4-989B": [
        5,
        7
    ],
    "10EC-0215": [
        18
    ],
    "10EC-0221": [
        11,
        15,
        88
    ],
    "10EC-0222": [
        11,
        12
    ],
    "10EC-0225": [
        28,
        30,
        33,
        90
    ],
    "10EC-0230": [
        13,
        20
    ],
    "10EC-0233": [
        3,
        4,
        5,
        11,
        13,
        21,
        27,
        28,
        29,
        32,
        33
    ],
    "10EC-0236": [
        3,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        23,
        36,
        54,
        55,
        68,
        69,
        99
    ],
    "10EC-0235": [
        3,
        8,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        21,
        22,
        24,
        28,
        29,
        33,
        35,
        36,
        37,
        72,
        88,
        99
    ],
    "10EC-0245": [
        11,
        12,
        13
    ],
    "10EC-0255": [
        3,
        11,
        12,
        13,
        15,
        17,
        18,
        20,
        21,
        22,
        23,
        27,
        28,
        29,
        30,
        31,
        37,
        66,
        69,
        71,
        80,
        82,
        86,
        96,
        99,
        100,
        255
    ],
    "10EC-0257": [
        11,
        18,
        86,
        96,
        97,
        99,
        100,
        101
    ],
    "10EC-0260": [
        11,
        12
    ],
    "10EC-0262": [
        7,
        11,
        12,
        13,
        14,
        28,
        66
    ],
    "10EC-0268": [
        3,
        11
    ],
    "10EC-0270": [
        3,
        4,
        21,
        27,
        28
    ],
    "10EC-0272": [
        3,
        11,
        12,
        18,
        21
    ],
    "10EC-0274": [
        21,
        28,
        35,
        39
    ],
    "10EC-0275": [
        3,
        13,
        15,
        28
    ],
    "10EC-0280": [
        3,
        4,
        11,
        13,
        15,
        16,
        17,
        18,
        21
    ],
    "10EC-0283": [
        1,
        3,
        11,
        12,
        13,
        15,
        44,
        45,
        66,
        73,
        88
    ],
    "10EC-0284": [
        3
    ],
    "10EC-0285": [
        11,
        21,
        31,
        52,
        61,
        66,
        71,
        88
    ],
    "10EC-0286": [
        3,
        11,
        69
    ],
    "10EC-0287": [
        11,
        13,
        21
    ],
    "10EC-0288": [
        3,
        13,
        23
    ],
    "10EC-0289": [
        11,
        12,
        13,
        15,
        23,
        33,
        68,
        69,
        87,
        93,
        99
    ],
    "10EC-0290": [
        3,
        4,
        10,
        15,
        28
    ],
    "10EC-0292": [
        12,
        15,
        18,
        28,
        32,
        55,
        59
    ],
    "10EC-0293": [
        11,
        28,
        29,
        30,
        31
    ],
    "10EC-0294": [
        11,
        12,
        13,
        15,
        21,
        22,
        28,
        44,
        66,
        99
    ],
    "10EC-0299": [
        21,
        22
    ],
    "10EC-0623": [
        13,
        21
    ],
    "10EC-0662": [
        5,
        7,
        11,
        12,
        13,
        15,
        16,
        17,
        18,
        19,
        66
    ],
    "10EC-0663": [
        3,
        4,
        15,
        28,
        99
    ],
    "10EC-0665": [
        12,
        13
    ],
    "10EC-0668": [
        3,
        20,
        27,
        28,
        29
    ],
    "10EC-0670": [
        12
    ],
    "10EC-0671": [
        12,
        15,
        16,
        88
    ],
    "10EC-0700": [
        11,
        22
    ],
    "10EC-0882": [
        5,
        7
    ],
    "10EC-0883": [
        7,
        20
    ],
    "10EC-0885": [
        1,
        12,
        15
    ],
    "10EC-0887": [
        1,
        2,
        3,
        5,
        7,
        11,
        12,
        13,
        17,
        18,
        20,
        33,
        40,
        50,
        52,
        53,
        87,
        99
    ],
    "10EC-0888": [
        1,
        2,
        3,
        4,
        5,
        7,
        11,
        27,
        28,
        29
    ],
    "10EC-0889": [
        1,
        2,
        3,
        11,
        12
    ],
    "10EC-0867": [
        11,
        13
    ],
    "10EC-0892": [
        1,
        2,
        3,
        4,
        5,
        7,
        11,
        12,
        15,
        16,
        17,
        18,
        20,
        21,
        22,
        23,
        28,
        31,
        32,
        90,
        92,
        97,
        98,
        99,
        100
    ],
    "10EC-0897": [
        11,
        12,
        13,
        21,
        22,
        23,
        66,
        69,
        77,
        98,
        99
    ],
    "10EC-0899": [
        1,
        2,
        3,
        5,
        7,
        11,
        13,
        28,
        65,
        66,
        98,
        99,
        101
    ],
    "10EC-0900": [
        1,
        2,
        3,
        5,
        7,
        11,
        99
    ],
    "10EC-1220": [
        1,
        2,
        3,
        5,
        7,
        11,
        13,
        15,
        16,
        17,
        18,
        20,
        21,
        25,
        27,
        28,
        29,
        30,
        34,
        35,
        69,
        98,
        99,
        100
    ],
    "10EC-0B00": [
        1,
        2,
        3,
        7,
        11,
        49,
        50,
        51,
        52,
        69
    ],
    "14F1-1F72": [
        3,
        13
    ],
    "14F1-1F86": [
        15,
        21
    ],
    "14F1-1FD6": [
        21,
        22
    ],
    "14F1-2008": [
        3,
        15,
        21,
        23,
        80
    ],
    "14F1-20D0": [
        12,
        13
    ],
    "14F1-5051": [
        11
    ],
    "14F1-5067": [
        3
    ],
    "14F1-5069": [
        3,
        13
    ],
    "14F1-506C": [
        3
    ],
    "14F1-506E": [
        3,
        12,
        13,
        14,
        28
    ],
    "14F1-50A1": [
        11,
        13
    ],
    "14F1-50A2": [
        11,
        13
    ],
    "14F1-50F2": [
        3
    ],
    "14F1-50F4": [
        3,
        13
    ],
    "14F1-510F": [
        3,
        21,
        28
    ],
    "14F1-5111": [
        3,
        14,
        15,
        21
    ],
    "14F1-5113": [
        3
    ],
    "14F1-5114": [
        3,
        13
    ],
    "14F1-5115": [
        3,
        28
    ],
    "111D-76D1": [
        12,
        13
    ],
    "111D-76D9": [
        13
    ],
    "111D-76F3": [
        3
    ],
    "111D-76B2": [
        3
    ],
    "111D-7675": [
        19,
        21
    ],
    "111D-7676": [
        15
    ],
    "111D-76D5": [
        3,
        11
    ],
    "111D-7605": [
        3,
        3,
        12,
        20,
        21,
        28,
        76
    ],
    "111D-7608": [
        3
    ],
    "111D-7603": [
        3,
        11
    ],
    "111D-76E7": [
        3,
        12
    ],
    "111D-76E0": [
        3,
        12,
        13,
        33,
        84
    ],
    "111D-76DF": [
        12
    ],
    "111D-76E5": [
        3
    ],
    "8384-7690": [
        11
    ],
    "8384-76A0": [
        11
    ],
    "8384-7662": [
        12
    ],
    "1106-4760": [
        21
    ],
    "1106-8446": [
        3,
        33,
        65
    ],
    "1106-0441": [
        5,
        7,
        9,
        13
    ]
}