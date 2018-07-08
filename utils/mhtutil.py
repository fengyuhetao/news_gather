import sys
import chilkat

mht = chilkat.CkMht()


def saveAsMht(url, dest):
    success = mht.UnlockComponent("7068325100505A2E")
    if success != True:
        print(mht.lastErrorText())
        sys.exit()

    mhtStr = mht.GetAndSaveMHT(url, dest)
    if mht.get_LastMethodSuccess() != True:
        print(mht.lastErrorText())
