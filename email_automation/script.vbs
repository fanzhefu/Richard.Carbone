 Dim ToAddress
 Dim MessageSubject
 Dim MessageBody
 Dim MessageAttachment
 
 Dim ol, ns, newMail, ToAddresses
 
 ToAddresses = Array( "zhefu.fan@forces.gc.ca", & _
					"richard.carbone@ecn.forces.gc.ca", & _
					"zhefu.fan@ecn.forces.gc.ca", & _
					"richard.carbone@ecn.forces.gc.ca", & _
					"rcarbone@videotron.ca", & _
					"fanzhefu@gmail.com")
 
 MessageSubject = "automation test, please reply"
 MessageBody = "Good morning." & _ 
 "This is a test for outlook/exchange automation." & _
 "bob." & _
 vbCrLf & vbCrLf
 MessageAttachment = "C:\Users\fan.z\Desktop\test.txt"
 
 Set ol = WScript.CreateObject("Outlook.Application")
 Set ns = ol.getNamespace("MAPI")
 ns.logon "","",true,false
 
 For Each ToAddress In ToAddresses
	 Set newMail = ol.CreateItem(olMailItem)
	 newMail.Subject = MessageSubject
	 newMail.Body = MessageBody & vbCrLf

	 ' validate the recipient, just in case...
	 Set myRecipient = ns.CreateRecipient(ToAddress)
	 myRecipient.Resolve
	 If Not myRecipient.Resolved Then
		 'MsgBox "unknown recipient"
		 WScript.Echo "Unknown recipient:", ToAddress
	 Else
		newMail.Recipients.Add(myRecipient)
		newMail.Attachments.Add(MessageAttachment).Displayname = "Test.txt"
		newMail.Send
		WScript.Echo "Send to recipient:", ToAddress

	 End If
 Next
 Set ol = Nothing
