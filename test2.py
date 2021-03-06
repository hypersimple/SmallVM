def get_reg_value(text,line,reg):
    subline = 0
    for subline in range(1,1000000):
        if text[line-subline].startswith('&') and text[line-subline].endswith('HLT=0'):
            if reg == 'eax':
                return text[line-subline].split()[1].split('=')[1]
            if reg == 'ebx':
                return text[line-subline].split()[2].split('=')[1]
            if reg == 'ecx':
                return text[line-subline].split()[3].split('=')[1]
            if reg == 'edx':
                return text[line-subline].split()[4].split('=')[1]
            if reg == 'esi':
                return text[line-subline].split()[5].split('=')[1]
            if reg == 'edi':
                return text[line-subline].split()[6].split('=')[1]
            if reg == 'ebp':
                return text[line-subline].split()[7].split('=')[1]
            if reg == 'esp':
                return text[line-subline].split()[8].split('=')[1]
            if reg == 'eip':
                return text[line-subline].split()[9].split('=')[1]
            if reg == 'efl':
                return text[line-subline].split()[10].split('=')[1]
            if reg == 'cr3':
                return text[line-subline].split()[12].split('=')[1]




text1 = []
text1.append( '& EAX=00ffff00 EBX=f86a4c58 ECX=bf99c440 EDX=00ffffff ESI=f86a4c58 EDI=e1477e6c EBP=f86a4b70 ESP=f86a4b58 EIP=804e2ea8 EFL=00000246 [---Z-P-] CR3=0ea97000 CPL=0 II=0 A20=1 SMM=0 HLT=0')
text1.append('1')
text1.append('3')

print get_reg_value(text1,2,'cr3')
