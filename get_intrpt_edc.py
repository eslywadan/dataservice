import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from ttlsap.adapter.intrpt import IntRptConnect

res = IntRptConnect()
res.get_apikey()
print(res.apikey.__str__)

