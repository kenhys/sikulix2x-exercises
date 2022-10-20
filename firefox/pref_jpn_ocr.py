import sys
import datetime
reload(sys)
sys.setdefaultencoding("UTF-8")

class FxVerify:
  def show_message(self, msg, timeout=1):
      Do.popup(msg, timeout)

  def launch_firefox(self):
    self.show_message(u"Firefoxを起動します\nこのダイアログは自動的に閉じます。")
    App.open("C:/work/firefox/esr102/run.bat")
    wait(2)
   
  def access_about(self, about):
    type("l", Key.CTRL)
    paste(about)
    type(Key.ENTER)
    wait(1)
    
     
  def access_about_config(self):
    self.access_about("about:config")
    type(Key.ENTER)
 
  def search_about_pref(self, pref):
    paste(pref)
    type(Key.ENTER)
    wait(2)

  def assert_equal(self, caption, expected, actual):
    if expected == actual:
      Debug.user("pass: %s (%s)" % (caption, expected))
    else:
      Debug.user("fail: %s (%s != %s)" % (caption, expected, actual.decode('utf-8')))

  def scan_text_from_area(self, area, strip=True, remove=True):
    img = getScreen().capture(area)
    Debug.user("scan area: %s" % (area.toString()))
    content = find(img.filename).text()
    if strip:
      content = content.strip()
    if remove:
      content = content.replace(" ", "")
    return content

# Log configuration
Settings.UserLogs = True
Settings.UserLogPrefix = "fxverify"
now = datetime.datetime.today()
Debug.setUserLogFile("log." + now.strftime("%Y%m%d.%H%M%S") + ".txt")

# OCR configuration
OCR.globalOptions().language("eng")
Debug.user(OCR.status())

Debug.user("Start auto verification with SikuliX")

fxverify = FxVerify()
fxverify.launch_firefox()

fxverify.access_about_config()
fxverify.search_about_pref("browser.migration.version")
# Specify region for 1920x1080 scaling 125% display
reg=Region(12,148,1423,35)
Debug.user("browser.migration.version: [%s]" % reg.text())

type("l", Key.CTRL)

fxverify.access_about("about:preferences")

Debug.user(u"Scan Japanese OCR text")
OCR.globalOptions().language("eng")
area=Region(296,106,307,28)
#area = selectRegion()

actual = fxverify.scan_text_from_area(area)
fxverify.assert_equal("managed with policy", u"ご使用のブラウザーはあなたの所属組織に管理されています。", actual)

type("q", Key.CTRL + Key.SHIFT)

Debug.user("End auto vefification with SikuliX")
