#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import json
import os

# CPU INFO
f = open("/proc/cpuinfo")
data = f.readlines()
f.close()

cpu_model_name = filter(lambda x: "model name" in x, data)[0].split(":")[1].strip()
cpu_number_of_core = max(map(lambda x: int(x.split(":")[1].strip()), filter(lambda x: "core id" in x, data))) + 1
cpu_virtual_cores = filter(lambda x: "siblings" in x, data)[0].split(":")[1].strip()


# Memory
s = subprocess.Popen(["sudo",  "dmidecode",  "--type", "memory"], stdout=subprocess.PIPE)
s.wait()
data = s.stdout.read().split("\n")

memory_modules = map(
    lambda x: x.split(":")[1].strip(),
    filter(lambda x: x.strip().startswith("Size:") or x.strip().startswith("Speed:"), data)
)

memory_modules = zip(memory_modules[::2], memory_modules[1::2])
memory_max_capacity = filter(lambda x: "Maximum Capacity:" in x, data)[0].split(":")[1].strip()


# Motherboard
s = subprocess.Popen(["sudo",  "dmidecode",  "-t", "2"], stdout=subprocess.PIPE)
s.wait()
data = s.stdout.read().split("\n")

try:
	motherboard_manufacturer = map(
	    lambda x: x.split(":")[1].strip(),
	    filter(lambda x: x.strip().startswith("Manufacturer:"), data)
	)[0]
except IndexError:
	motherboard_manufacturer = "Not Available"

try:
	motherboard_model = map(
	    lambda x: x.split(":")[1].strip(),
	    filter(lambda x: x.strip().startswith("Product Name:"), data)
	)[0]
except IndexError:
	motherboard_model = "Not Available"

try:
	motherboard_sn = map(
	    lambda x: x.split(":")[1].strip(),
	    filter(lambda x: x.strip().startswith("Serial Number:"), data)
	)[0]
except IndexError:
	motherboard_sn = "Not Available"


#Disk
s = subprocess.Popen(["sudo",  "hdparm",  "-I"] + [ "/dev/"+d for d in os.listdir("/dev/") if d.startswith("sd") ], stdout=subprocess.PIPE)
s.wait()
data = s.stdout.read().split("\n")

disk_name = filter(lambda x: "Model Number" in x, data)
disk_size = filter(lambda x: "M = 1000*1000" in x, data)
disk_sn = filter(lambda x: "Serial Number" in x, data)

disk_size = map(lambda x:x.split(":")[1].strip(), disk_size)
disk_name = map(lambda x:x.split(":")[1].strip(), disk_name)
disk_sn = map(lambda x:x.split(":")[1].strip(), disk_sn)
disks = { dsn: (dn, ds) for dsn, dn, ds in zip(disk_sn, disk_name, disk_size) }



print("-"*60)
print("")
print("Cpu: %s" % cpu_model_name)
print("Cpu Cores: %s" % cpu_number_of_core)
print("Cpu Virtual Cores: %s" % cpu_virtual_cores)
print("")
print("Ram Modules: %s" %  ", ".join(map(lambda x: "%s %s" % x, memory_modules)))
print("Ram Max: %s" % memory_max_capacity)
print("")
print("Motherboard: %s" % motherboard_manufacturer)
print("Motherboard Model: %s" % motherboard_model)
print("Motherboard Serial: %s" % motherboard_sn)
print("")
for disk_sn, data in disks.items():
	print("Disk: %s" % disk_sn)
	print("⌙Name: %s" % data[0])
	print("⌙Size: %s" % data[1])
print("")
print("-"*60)