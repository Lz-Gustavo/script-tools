"""Description
Lorem ipsum yolo
"""
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Allocate a node and ask for a 30GB file system mounted at /mydata
node = request.RawPC("node")
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
node.hardware_type = "d430"

bs = node.Blockstore("bs", "/tmp")
bs.size = "200GB"
bs.placement = "sysvol"  # any||nonsysvol

bs1 = node.Blockstore("disk1", "/disk1")
bs1.placement = "nonsysvol"
bs1.size = "900GB"

bs2 = node.Blockstore("disk2", "/disk2")
bs2.placement = "nonsysvol"
bs2.size = "900GB"

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()