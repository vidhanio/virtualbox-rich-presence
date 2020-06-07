import virtualbox, json, pprint, configparser, time, psutil
from pypresence import Presence

# Machine State
## virtualbox.library.MachineState(int)
### 1 - PoweredOff
### 2 - Saved
### 3 - Teleported
### 4 - Aborted
### 5 - FirstOnline
### 6 - Paused
### 7 - Stuck
### 8 - FirstTransient
### 9 - LiveSnapshotting
### 10 - Starting
### 11 - Stopping
### 12 - Saving
### 13 - Restoring
### 14 - TeleportingPausedVM
### 15 - TeleportingIn
### 16 - FaultTolerantSyncing
### 17 - DeletingSnapshotOnline
### 18 - DeletingSnapshotPaused
### 19 - LastOnline
### 20 - RestoringSnapshot
### 21 - DeletingSnapshot
### 22 - SettingUp
### 23 - LastTransient


class rich_presence:
    def __init__(self):
        super().__init__()

        self.vbox = virtualbox.VirtualBox()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.assets = json.load(open("assets.json", "r"))
        self.previous_formatdict = None

        client_id = self.config["Rich Presence"]["client_id"]
        self.RPC = Presence(client_id)
        self.RPC.connect()
        self.start_time = time.time()

        while True:
            if "VirtualBox.exe" in (
                p.name() for p in psutil.process_iter()
            ) or "VirtualBoxVM.exe" in (p.name() for p in psutil.process_iter()):
                pvars = self.presence_gen()
                # print("-------------------------\npresence_dict\n-------------------------")
                # pprint.pprint(pvars)
                self.RPC.update(
                    large_image=pvars["large_image"],
                    large_text=pvars["large_text"],
                    small_image=pvars["small_image"],
                    small_text=pvars["small_text"],
                    details=pvars["details"],
                    state=pvars["state"],
                    start=pvars["start"],
                )
                pprint.pprint(pvars)
                print("--------------------")
            else:
                print("VirtualBox is not running")
                self.RPC.clear()
            time.sleep(15)

    def vbox_to_dict(self):

        # Generate metadata for each machine
        self.machines = self.vbox.machines
        self.machine_names = [m.name for m in self.machines]
        self.machine_states = [m.state for m in self.machines]
        self.machine_operating_systems = [m.os_type_id for m in self.machines]

        # Create dictionary to store info
        self.vd_machine_dict = {}

        for i in range(len(self.machines)):

            # Extract OS version and architecture info
            self.vd_operating_system, self.vd_architecture = self.os_to_arch(
                self.machine_operating_systems[i]
            )

            self.vd_name = self.machine_names[i]  # Get name of VM
            self.vd_machine_dict[self.vd_name] = {}  # Initialize dictionaries
            self.vd_machine_dict[self.vd_name][
                "os version"
            ] = self.vd_operating_system  # Add OS version
            self.vd_machine_dict[self.vd_name][
                "architecture"
            ] = self.vd_architecture  # Add architecture
            self.vd_machine_dict[self.vd_name]["state"] = str(
                self.machine_states[i]
            )  # Add state

            # Run through assets and find the correct OS
            for key in list(self.assets["operating systems"].keys()):
                if self.vd_operating_system in list(
                    self.assets["operating systems"][key]["versions"].keys()
                ):
                    self.vd_machine_dict[self.vd_name]["operating system"] = key

        # print("-------------------------\nvbox_to_dict\n-------------------------")
        pprint.pprint(self.vd_machine_dict)
        return self.vd_machine_dict

    def os_to_arch(self, oa_input):
        if "_" in oa_input:
            self.oa_operating_system, self.oa_architecture = oa_input.split("_", 1)
        else:
            self.oa_operating_system = oa_input
            self.oa_architecture = "32"
        return self.oa_operating_system, self.oa_architecture

    def vdict_to_formatdict(self, vf_input):
        self.vf_active_vm = None
        self.format_dict = {}
        self.format_dict["active_vm"] = False
        for vf_key in list(vf_input.keys()):
            if vf_input[vf_key]["state"] == "FirstOnline":
                self.vf_active_vm = vf_key
        if self.vf_active_vm:
            self.format_dict["active_vm"] = True
            self.format_dict["os_hf"] = vf_input[self.vf_active_vm]["operating system"]
            self.format_dict["version_hf"] = self.assets["operating systems"][
                vf_input[self.vf_active_vm]["operating system"]
            ]["versions"][vf_input[self.vf_active_vm]["os version"]]["name"]
            self.format_dict["version_image"] = self.assets["operating systems"][
                vf_input[self.vf_active_vm]["operating system"]
            ]["versions"][vf_input[self.vf_active_vm]["os version"]]["image"]
            self.format_dict["architecture"] = vf_input[self.vf_active_vm][
                "architecture"
            ]
        self.format_dict["icon"] = "icon"
        # print("-------------------------\nformat_dict\n-------------------------")
        # pprint.pprint(self.format_dict)
        return self.format_dict

    def presence_gen(self):
        self.pg_formatdict = self.vdict_to_formatdict(self.vbox_to_dict())
        if self.pg_formatdict != self.previous_formatdict:
            self.pg_presencedict = {}
            self.pg_presencedict["start"] = time.time()
        else:
            self.pg_pdtime = self.pg_presencedict["start"]
            self.pg_presencedict = {"start": self.pg_pdtime}

        if self.pg_formatdict["active_vm"] == True:
            for pg_field in list(self.config["In VM"].keys()):
                self.pg_presencedict[pg_field] = self.config["In VM"][pg_field].format(
                    **self.pg_formatdict
                )

        else:
            for pg_field in list(self.config["In Menu"].keys()):
                self.pg_presencedict[pg_field] = self.config["In Menu"][
                    pg_field
                ].format(**self.pg_formatdict)
            self.pg_presencedict["start"] = None
        for pg_field in list(self.pg_presencedict.keys()):
            if (
                self.pg_presencedict[pg_field] == ""
                or self.pg_presencedict[pg_field] == []
            ):
                self.pg_presencedict[pg_field] = None
        self.previous_formatdict = self.pg_formatdict
        return self.pg_presencedict


rich_presence()
