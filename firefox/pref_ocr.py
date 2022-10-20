import sys
import datetime
import csv
reload(sys)
sys.setdefaultencoding("UTF-8")

class FxVerify:
  def show_message(self, msg, timeout=1):
      Do.popup(msg, timeout)

  def startup_notification(self):
    self.show_message(u"Firefoxを起動し、about:configを表示できるようにしておいてください。\nこのダイアログは自動的に閉じます。", 3)
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
# Put *.traineddata under tessdata
Settings.OcrDataPath = "c:/Users/Public/testcases/tessdata"
now = datetime.datetime.today()
Debug.setUserLogFile("log." + now.strftime("%Y%m%d.%H%M%S") + ".txt")

# OCR configuration
OCR.globalOptions().language("eng")
Debug.user(OCR.status())

Debug.user("Start auto verification with SikuliX")

fxverify = FxVerify()
fxverify.startup_notification()

fxverify.access_about_config()

# Select region for matched pref
fxverify.search_about_pref("browser.migration.version")
# Specify region for 1920x1080 scaling 125% display
# reg=Region(12,148,1423,35)
# Select
area = selectRegion()
area.highlight(3, "red")

with open('about_config.csv') as f:
  #reader = csv.reader(f, delimiter='\t')
  reader = csv.reader(f)
  for row in reader:
    print(row)
    expected = "%s %s" % (row[0], row[1].strip())
    type("a", Key.CTRL)
    paste(row[0].strip())
    type(Key.ENTER)
    actual = fxverify.scan_text_from_area(area, False, False)
    fxverify.assert_equal(row[0], expected, actual)

Debug.user("End auto vefification with SikuliX")

