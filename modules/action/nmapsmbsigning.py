from core.actionModule import actionModule
from core.keystore import KeyStore as kb
from core.mynmap import mynmap


class nmapsmbsigning(actionModule):
    def __init__(self, config, display, lock):
        super(nmapsmbsigning, self).__init__(config, display, lock)
        self.title = "NMap SMB-Signing Scan"
        self.shortName = "NmapSMBSigning"
        self.description = "execute [nmap -p445 --script=smb-security-mode] on each target"

        self.requirements = ["nmap"]
        self.triggers = ["newPort445"]

        self.safeLevel = 5

    def getTargets(self):
        self.targets = kb.get(['host/*/tcpport/139', 'host/*/tcpport/445'])

    def process(self):
        # load any targets we are interested in
        self.getTargets()

        # loop over each target
        for t in self.targets:
            # verify we have not tested this host before
            if not self.seentarget(t):
                # add the new IP to the already seen list
                self.addseentarget(t)
                # run nmap
                n = mynmap(self.config, self.display)
                scan_results = n.run(target=t, flags="--script=smb-security-mode", ports="445", vector=self.vector,
                                     filetag=t + "_SMBSINGINGSCAN")['scan']

        return
