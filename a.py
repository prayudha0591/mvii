# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()


wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def NOTIFIED_INVITE_INTO_GROUP (op):
    Amid = "u32b63e6b0d4b514632c574746843a0dc"
    if op.param2 in Amid:
        client.acceptGroupInvitation(op.param1)
    else:
		pass

tracer.addOpInterrupt(13,NOTIFIED_INVITE_INTO_GROUP)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    Amid = "u32b63e6b0d4b514632c574746843a0dc"
    if Amid in op.param3:
                client.kickoutFromGroup(op.param1,[op.param2])
                client.inviteIntoGroup(op.param1,[op.param3])
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", itu pacar gue, kampret")
    else:
		pass
tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        if msg.toType == 2:
            if "DHEVmviiGS" in msg.text:
                sendMessage(msg.to, "miss beauty lg sibuk kerja\n,mlm mojok,jangan ganggu ntar nongol sendri")
                print "[mvii]"
            if "@DHEVmviiGS" in msg.text:
                print "[mviii]"
            if "mvii apakah" in msg.text:
                x = ["bisa jadi,bisa jadi", "ngimpiii luu..", "ah fitnah ituu" ,"mana gw tauu,haha", "iya sih dikit"]
                sendMessage(msg.to,random.choice(x))
        else:
            pass
    except:
        pass
			
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)


def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "help":
                    sendMessage(msg.to, msg.to)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass

        if msg.text == "movie":
            content = movie()
            client.sendMessage(msg.to,(content))
            return 0

				
        if "Inv " in msg.text:
            midd = msg.text.replace("Inv ","")
            client.findAndAddContactsByMid(midd)
            client.inviteIntoGroup(msg.to,[midd])

        if msg.toType == 2:
            if msg.text in ["tag all","Tagall"]:
                  group = client.getGroup(msg.to)
                  nama = [contact.mid for contact in group.members]

                  cb = ""
                  cb2 = ""
                  strt = int(0)
                  akh = int(0)
                  for md in nama:
                      akh = akh + int(6)

                      cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""

                      strt = strt + int(7)
                      akh = akh + 1
                      cb2 += "@nrik \n"

                  cb = (cb[:int(len(cb)-1)])
                  msg.contentType = 0
                  msg.text = cb2
                  msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}

                  try:
                      client.sendMessage(msg)
                  except Exception as error:
                      print error
            if msg.text in ["Speedbot","speed"]:
				start = time.time()
				sendMessage(msg.to, "please wait...")
				elapsed_time = time.time() - start
				sendMessage(msg.to, "%ss" % (elapsed_time))
            elif "spam" in msg.text:
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
				sendMessage(msg.to, "up")
            elif "bye @" in msg.text:
                if msg.toType == 2:
                    _name = msg.text.replace("bye @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            for target in targets:
						        client.kickoutFromGroup(msg.to,[target])
            elif "get @" in msg.text:
                if msg.toType == 2:
                    print "[Get]"
                    _name = msg.text.replace("get @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            client.findAndAddContactsByMid(g.mid)
                            for target in targets:
                                M = Message()
                                M.to = msg.to
                                M.contentType = 13
                                M.contentMetadata = {'mid': g.mid}
                                client.sendMessage(M)

            if msg.contentType == 0:
                if msg.text == "help":
                    sendMessage(msg.to,text="set\ntes\nmid\ngid\nginfo\ntag all\nme\ngift\nurl\nqr open\nqrc close\nyd cancel\nget @\ntime\nspeed\nbye @")
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    sendMessage(msg.to,md)
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "qr open":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "already open")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                if msg.text == "qr close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "already close")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL close")

                if msg.text == "yd cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "No one is inviting.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if msg.text == "time":
                    sendMessage(msg.to, "Current time is" + datetime.datetime.today().strftime('%Y.%m.%d. %H:%M:%S') + "is")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "set":
                    sendMessage(msg.to, "--batas cctv--")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "tes":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "----T E R C I D U K---- %s\n\n\n--T E R S A N G K A--\n%s\n\nReading point creation date n time:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "An already read point has not been set.\n「set」you can send ♪ read point will be created ♪")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
