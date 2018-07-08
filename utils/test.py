import sys
import chilkat

mht = chilkat.CkMht()

success = mht.UnlockComponent("7068325100505A2E")
if success != True:
    print(mht.lastErrorText())
    sys.exit()

mhtStr = mht.GetAndSaveMHT("https://paper.seebug.org/636/", "./test.mhtml")
if mht.get_LastMethodSuccess() != True:
    print(mht.lastErrorText())
else:
    print(mhtStr)
