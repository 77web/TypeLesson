#coding: utf-8

import wx



class QuestionPanel(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id, size=wx.Size(180, 80))
    
    self.text = wx.TextCtrl(self, -1, value="", size=wx.Size(160, 70), style=wx.TE_READONLY | wx.EXPAND)

class TypePanel(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id, size=wx.Size(180, 80))
    self.text = wx.TextCtrl(self, -1, value="", size=wx.Size(160, 70), style=wx.TE_PROCESS_ENTER | wx.EXPAND)

class NanaWin(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=wx.Size(200, 200))
    
    self.missType = 0
    
    #load test file
    self.loadQuestion()
    
    #font
    font = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    
    #panels
    panel = wx.Panel(self, -1)
    self.QuestionPanel = QuestionPanel(panel, -1)
    self.QuestionPanel.text.SetFont(font)
    self.TypePanel = TypePanel(panel, -1)
    self.TypePanel.text.SetFont(font)
    
    #panel layout
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(self.QuestionPanel, flag=wx.EXPAND | wx.BOTTOM)
    vbox.Add((-1, 10))
    vbox.Add(self.TypePanel, flag=wx.EXPAND)
    
    panel.SetSizer(vbox)

    #menu
    settingMenu = wx.Menu()
    self.isUpper = settingMenu.AppendCheckItem(1, u'大文字で表示')
    self.isUpper.Check()
    menuBar = wx.MenuBar()
    menuBar.Append(settingMenu, u'設定')
    self.SetMenuBar(menuBar)
    
    #question & input initialize
    self.goNext()
    
    #validate input
    self.TypePanel.text.Bind(wx.EVT_CHAR, self.onTyped)
    
    
    #centering & show
    self.Centre()
    self.Show(True)
    
  def onTyped(self, event):
    keyCode = event.GetKeyCode()
    if keyCode == wx.WXK_BACK or keyCode == wx.WXK_DELETE:
      event.Skip()
      return True
    char = chr(keyCode)
    if self.isUpper.IsChecked():
      char = char.upper()
    self.TypePanel.text.WriteText(char)
    input = self.TypePanel.text.GetValue()
    test = self.QuestionPanel.text.GetValue()
    if input == test:
      self.goNext()
    elif test[0:len(input)] == input:
      self.TypePanel.text.SetBackgroundColour('White')
    else:
      self.missType += 1
      self.TypePanel.text.SetBackgroundColour('Pink')

  def goNext(self):
    self.TypePanel.text.SetValue('')
    self.TypePanel.text.SetBackgroundColour('White')
    try:
      next = self.questions[self.questionCursor]
      if self.isUpper.IsChecked():
        next = next.upper()
      self.QuestionPanel.text.SetValue(next)
      self.questionCursor += 1
    except IndexError:
      self.goFinish()
      
  def goFinish(self):
    clearMessage = u'クリアおめでとう！\nもんだい%s\nしっぱい%s' % (len(self.questions), self.missType)
    dlg = wx.MessageDialog(self, caption=u'クリアおめでとう！', message=clearMessage, style=wx.OK)
    if dlg.ShowModal():
      self.Close()
  
  def loadQuestion(self):
    import os
    path = os.getcwd() + os.sep + 'lessons' + os.sep + '01.txt'
    f = open(path)
    data = f.read()
    f.close()
    self.questions = data.split('\n')
    self.questionCursor = 0

app = wx.App()

NanaWin(None, -1, u'かんたんタイピング')

app.MainLoop()

