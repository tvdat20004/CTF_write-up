enc = "DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL"
flag = ""

for i in range(len(enc)):
	if not enc[i].isalpha():
		flag +=enc[i]
	else:
		char = (ord(enc[i]) - 0x41 - i) % 26 
		flag += chr(char + 0x41)

print(flag)