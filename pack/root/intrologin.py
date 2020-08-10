import app, net, ui, snd, wndMgr, musicInfo, systemSetting, localeInfo, constInfo, ime, os, uiScriptLocale
from _weakref import proxy

SERVER_IP = "160.20.146.133" # YOUR SERVER IP
CH1_PORT = 30003 # PORTS
CH2_PORT = 30007
CH3_PORT = 23000
CH4_PORT = 24000
PORT_AUTH = 30001
NUME_SERVER = "GOT"

class LoginWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.stream = stream
		self.AccUse = [None, None, None, None, None, None]
		self.AccDel = [None, None, None, None, None, None]
		self.AccName = [None, None, None, None, None, None]
		self.AccSave = [None, None, None, None, None, None]
		self.Login = [None, None, None, None, None, None]
		self.SelectedChannel = [None, None, None, None, None, None]
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

	def Open(self):
		print("TEST")
		if (False == os.path.exists('./loginsettings')):
			try:
				print("DEBUG01")
				os.mkdir("/loginsettings/")
			except OSError:
				print("EXIT")
				app.Exit
			
		f = open("loginsettings/loginsetting1.cfg", "a+")
		f.close()
		f = open("loginsettings/loginsetting2.cfg", "a+")
		f.close()
		f = open("loginsettings/loginsetting3.cfg", "a+")
		f.close()
		f = open("loginsettings/loginsetting4.cfg", "a+")
		f.close()
		f = open("loginsettings/loginsetting5.cfg", "a+")
		f.close()
		f = open("loginsettings/loginsetting6.cfg", "a+")
		f.close()
		
		self.loginFailureMsgDict={

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		self.__LoadScript("UIScript/loginwindow.py")
		
		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
		self.SetChannel(0)
		
		self.Show()
		app.ShowCursor()	

	def Close(self):
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.loginMusic)
	
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
			
		self.AccUse = [None, None, None, None, None, None]
		self.AccDel = [None, None, None, None, None, None]
		self.AccName = [None, None, None, None, None, None]
		self.AccSave = [None, None, None, None, None, None]
		self.Login = [None, None, None, None, None, None]
		self.SelectedChannel = [None, None, None, None, None, None]
	
		self.Hide()
		self.KillFocus()
		app.HideCursor()
		ime.ClearExceptKey()

	def OnConnectFailure(self):
		snd.PlaySound("sound/ui/loginfail.wav")
		self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.EmptyFunc)

	def OnHandShake(self):
		snd.PlaySound("sound/ui/loginok.wav")
		self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
		
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error

		loginFailureFunc = self.loginFailureFuncDict.get(error, self.EmptyFunc)

		self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)

		snd.PlaySound("sound/ui/loginfail.wav")

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")

		try:
			self.idEditLine = self.GetChild("id")
			self.pwdEditLine = self.GetChild("pwd")
			self.loginButton = self.GetChild("login_button")
			
			self.channelButton = {
				0 : self.GetChild("ch1"),
				1 :	self.GetChild("ch2"),
				2 : self.GetChild("ch3"),
				3 : self.GetChild("ch4")}
			
			self.AccUse[0]	= self.GetChild("saved_accs_acc1_use")
			self.AccUse[1]	= self.GetChild("saved_accs_acc2_use")
			self.AccUse[2]	= self.GetChild("saved_accs_acc3_use")
			self.AccUse[3]	= self.GetChild("saved_accs_acc4_use")
			self.AccUse[4]	= self.GetChild("saved_accs_acc5_use")
			self.AccUse[5]	= self.GetChild("saved_accs_acc6_use")
			
			self.AccDel[0]	= self.GetChild("saved_accs_acc1_del")
			self.AccDel[1]	= self.GetChild("saved_accs_acc2_del")
			self.AccDel[2]	= self.GetChild("saved_accs_acc3_del")
			self.AccDel[3]	= self.GetChild("saved_accs_acc4_del")
			self.AccDel[4]	= self.GetChild("saved_accs_acc5_del")
			self.AccDel[5]	= self.GetChild("saved_accs_acc6_del")
			
			self.AccName[0]	= self.GetChild("saved_accs_acc1")
			self.AccName[1]	= self.GetChild("saved_accs_acc2")
			self.AccName[2]	= self.GetChild("saved_accs_acc3")
			self.AccName[3]	= self.GetChild("saved_accs_acc4")
			self.AccName[4]	= self.GetChild("saved_accs_acc5")
			self.AccName[5]	= self.GetChild("saved_accs_acc6")

			self.AccSave[0]	= self.GetChild("save_acc1")
			self.AccSave[1]	= self.GetChild("save_acc2")
			self.AccSave[2]	= self.GetChild("save_acc3")
			self.AccSave[3]	= self.GetChild("save_acc4")
			self.AccSave[4]	= self.GetChild("save_acc5")
			self.AccSave[5]	= self.GetChild("save_acc6")
			
			self.SelectedChannel[0]	= self.GetChild("selected_channel1")
			self.SelectedChannel[1]	= self.GetChild("selected_channel2")
			self.SelectedChannel[2]	= self.GetChild("selected_channel3")
			self.SelectedChannel[3]	= self.GetChild("selected_channel4")
			self.SelectedChannel[4]	= self.GetChild("selected_channel5")
			self.SelectedChannel[5]	= self.GetChild("selected_channel6")

		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")
			
				
		for (channelID, channelButtons) in self.channelButton.items():
				channelButtons.SetEvent(ui.__mem_func__(self.SetChannel), channelID)

		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
		# self.exitButton.SetEvent(ui.__mem_func__(self.OnPressExitKey))
		
		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))
		self.idEditLine.SetFocus()

		self.AccSave[0].SetEvent(lambda : self.__OnClickLoginSaveButton(0))
		self.AccSave[1].SetEvent(lambda : self.__OnClickLoginSaveButton(1))
		self.AccSave[2].SetEvent(lambda : self.__OnClickLoginSaveButton(2))
		self.AccSave[3].SetEvent(lambda : self.__OnClickLoginSaveButton(3))
		self.AccSave[4].SetEvent(lambda : self.__OnClickLoginSaveButton(4))
		self.AccSave[5].SetEvent(lambda : self.__OnClickLoginSaveButton(5))
		
		self.AccUse[0].SetEvent(lambda : self.__LoadACCInfos(0))
		self.AccUse[1].SetEvent(lambda : self.__LoadACCInfos(1))
		self.AccUse[2].SetEvent(lambda : self.__LoadACCInfos(2))
		self.AccUse[3].SetEvent(lambda : self.__LoadACCInfos(3))
		self.AccUse[4].SetEvent(lambda : self.__LoadACCInfos(4))
		self.AccUse[5].SetEvent(lambda : self.__LoadACCInfos(5))
		
		self.AccDel[0].SetEvent(lambda : self.__OnClickDeleteButton(0))
		self.AccDel[1].SetEvent(lambda : self.__OnClickDeleteButton(1))
		self.AccDel[2].SetEvent(lambda : self.__OnClickDeleteButton(2))
		self.AccDel[3].SetEvent(lambda : self.__OnClickDeleteButton(3))
		self.AccDel[4].SetEvent(lambda : self.__OnClickDeleteButton(4))
		self.AccDel[5].SetEvent(lambda : self.__OnClickDeleteButton(5))
		
	def SetChannel(self, ch):
		for key, button in self.channelButton.items():
			button.SetUp()
			
		self.channelButton[ch].Down()
		
		for i in range(6):
			self.SelectedChannel[i].Hide()
		self.SelectedChannel[ch].Show()

		self.stream.SetConnectInfo(SERVER_IP, self.ChannelPort(ch, 0), SERVER_IP, self.ChannelPort("LOGIN"))
		net.SetMarkServer(SERVER_IP, self.ChannelPort("LOGO"))
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
		self.__LoadACCNames()
		net.SetServerInfo(self.ChannelPort(ch, 2))
		
	def ChannelPort(self, ch, value=0):
		channel = {

			0	:	CH1_PORT,
			1	:	CH2_PORT,
			2	:	CH3_PORT,
			3	:	CH4_PORT,}
		
		if ch == "LOGIN":
			return PORT_AUTH
		elif ch == "LOGO":
			return channel[0]
		elif value == 2:
			return NUME_SERVER + ", CH%s" % (ch+1)
		else:
			return channel[ch]
				
	def Connect(self, id, pwd):
		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()
			
		constInfo.LastAccount = id.lower()

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.EmptyFunc, localeInfo.UI_CANCEL)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()
		
	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return TRUE

	def EmptyFunc(self):
		pass

	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()

		if len(id)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.EmptyFunc)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.EmptyFunc)
			return

		self.Connect(id, pwd)
		
	def __LoadACCInfos(self, accid):
		import linecache
		login = linecache.getline("loginsettings/loginsetting" + str(accid) + ".cfg", 1)
		password = linecache.getline("loginsettings/loginsetting" + str(accid) + ".cfg", 2)
		login = login.replace("\n", "")
		password = password.replace("\n", "")
		if login != "" and password != "":
			self.Connect(login, password)
		else:
			self.PopupNotifyMessage(uiScriptLocale.LOGIN_INTERFACE_NOSAVED_ACC)

	def __LoadACCNames(self):
		for i in range(6):
			fd = open( "loginsettings/loginsetting" + str(i) + ".cfg" )
			self.Login[i] = fd.readline()
			self.Login[i].replace( "\n", "" )
			fd.close()
			
			if self.Login[i] != "":
				self.AccName[i].SetText(str(self.Login[i]))
				self.AccUse[i].Show()
				self.AccDel[i].Show()
				self.AccSave[i].Hide()
			else:
				self.AccName[i].SetText(uiScriptLocale.LOGIN_INTERFACE_FREE_SPACE)
				self.AccSave[i].Show()
				self.AccUse[i].Hide()
				self.AccDel[i].Hide()

	def __OnClickLoginSaveButton(self, id):
		user = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		
		fd = open("loginsettings/loginsetting" + str(id) + ".cfg")
		self.Login[id] = fd.readline()
		self.Login[id].replace( "\n", "" )
		fd.close()
		
		if user == "":
			self.PopupNotifyMessage(uiScriptLocale.LOGIN_INTERFACE_PASTE_ID)
			return
			
		if pwd == "":
			self.PopupNotifyMessage(uiScriptLocale.LOGIN_INTERFACE_PASTE_PW)
			return
		
		f = open("loginsettings/loginsetting" + str(id) + ".cfg", "r+")
		f.write (user +"\n")
		f.write (pwd)
		f.close()
		
		self.PopupNotifyMessage(uiScriptLocale.LOGIN_INTERFACE_SAVED)
		self.__LoadACCNames()
		
	def __OnClickDeleteButton(self, id):
		f = open("loginsettings/loginsetting" + str(id) + ".cfg", "r+")
		check = f.readline()
		if check != "":
			f.truncate(0)
			f.close()
			self.__LoadACCNames()
			self.PopupNotifyMessage("Slot " + str(id+1) + " " + uiScriptLocale.LOGIN_INTERFACE_DELETED)
		else:
			self.PopupNotifyMessage("Slot " + str(id+1) + " " + uiScriptLocale.LOGIN_INTERFACE_ALREADY_EMPTY)
