import sys
import uuid, json, os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pickle
import time
global mqttc, home, room, bulb, key, rkey, keyset, homeset, roomset,status
keyset, homeset, roomset, status = False, False, False, False
home, room = "", ""

if sys.version_info[0] > 2:
	from six.moves import input as raw_input


def print_bulb(switch):
		global mqttc, home, room, cl, bulb, status
		status = switch
		save_vars()
		if sys.platform == 'win32':
			os.system('cls')
		else:
			os.system('clear')
		print("\033[1;37;40m")
		print("Hi! My #LB id is "+bulb)
		print("and I'm at "+home+" located at "+room)
		print("\n")
		if(status):
			print("\033[1;33;40m")
		else:
			print("")
		print("    _.-\"```\"-._")
		print("  .'           '.")
		print(" /      .-.      \\")
		print(";       | |       ;")
		print("|       | |       |")
		print(";       \_/       ;")
		print(" \      (_)      /")
		print("  '.           .'")
		print("    `;_______;`")
		print("     \033[1;37;40m|_..--\"`)")
		print("     (_..--'`|")
		print("     |_..--'`)")
		print("     (_..--'`|")
		print("      `-...-`")
		print("\033[1;37;40m")

def save_vars():
	with open('obj.lbdata', 'wb') as f: 
		pickle.dump([home, room, bulb, key, rkey, keyset, homeset, roomset,status], f)

def on_message(mqttc, obj, msg):
	global home, room, bulb, key, rkey, keyset, homeset, roomset
	#mqttc.publish("lightbulb-debug/r/"+bulb+"/setup", (msg.topic+" "+msg.payload.decode("utf-8") ) , qos=2)
	if msg.topic == "lightbulb-discover/"+bulb+"/help":
		os.system('cls')
		print("To setup device send a message to "+"lightbulb-discover/"+bulb+"/setup"+" with a message \"start\"")
		print("You will recieve a message at "+"lightbulb-discover/r/"+bulb+"/setup"+" with a key that will be needed for further comunicaton")
		
		
	if msg.topic == "lightbulb-discover/"+bulb+"/setup":
		#mqttc.publish("lightbulb-debug/r/"+bulb+"/setup", (str(keyset)+" "+str(roomset)+" "+str(homeset)) , qos=2)
		if keyset:
			if (not homeset):
				homeset = True
				home = msg.payload.decode("utf-8") 
				mqttc.publish("lightbulb-discover/r/"+bulb+"/setup", '{"msg":"Next setp is to set room name. To do so send room the name to '+"lightbulb-discover/"+bulb+"/setup"+'"}', qos=2)
			else:
				if (not roomset):
					roomset = True
					room = msg.payload.decode("utf-8") 
					mqttc.publish("lightbulb-discover/r/"+bulb+"/setup", '{"msg":"Device is set up thank you"}', qos=2)
					save_vars()
					mqttc.unsubscribe("lightbulb-discover/"+bulb+"/#")
					mqttc.subscribe(home+"/"+room+'/'+bulb+"/#", 0)
					print_bulb(False)
					time.sleep(1)
					print_bulb(True)
					time.sleep(1)
					print_bulb(False)
					time.sleep(1)
					print_bulb(True)
					time.sleep(1)
		if msg.payload.decode("utf-8")  == "start":
			if not keyset:
				keyset = True
				key = str(uuid.uuid4())
				rkey = str(uuid.uuid4())[:8]
				mqttc.publish("lightbulb-discover/r/"+bulb+"/setup", '{"key":"'+key+'","msg":"Next setp is to set home name. To do so send the home name to '+"lightbulb-discover/"+bulb+"/setup"+'"}', qos=2)
		
	if msg.topic == home+"/"+room+'/'+bulb+"/help":
		mqttc.publish(home+"/"+room+'/r/'+bulb+"/help",("The device is already set up and locateted at "+home+" in "+room+" if you want to reset the device you can do so at "+home+"/"+room+'/'+bulb+"/reset"+" by sending "+rkey), qos=2)
		
		
		
	if msg.topic == home+"/"+room+'/'+bulb+"/switch":
		jd = json.loads(msg.payload.decode("utf-8") )
		if jd['key'] == key:
			if "ON" == jd["switch"].upper():
				print_bulb(True)
			elif "OFF" == jd["switch"].upper():
				print_bulb(False)
			
			
	if msg.topic == home+"/"+room+'/'+bulb+"/reset":
		if rkey == msg.payload.decode("utf-8") :
			key = str(uuid.uuid4())
			rkey = str(uuid.uuid4())[:8]
			mqttc.publish(home+"/"+room+'/r/'+bulb+"/reset", '{"key":"'+key+'"}', qos=2)
			save_vars()
		else:
			mqttc.publish(home+"/"+room+'/r/'+bulb+"/reset", 'error', qos=2)
	
	
		
		
def mcon():
	print("\033[1;37;40m")
	global mqttc, home, room, bulb, key, rkey, keyset, homeset, roomset
	mqttc = mqtt.Client()
	mqttc.on_message = on_message
	mqttc.connect("broker.hivemq.com", 1883, 60)
	if os.path.exists('obj.lbdata'):
		with open("obj.lbdata", 'rb') as f: 
			home, room, bulb, key, rkey, keyset, homeset, roomset, status = pickle.load(f)
		mqttc.subscribe(home+"/"+room+'/'+bulb+"/#", 0)
		print_bulb(status)
		
	else:
		bulb = str(uuid.uuid4())[:8]
		key = str(uuid.uuid4())
		mqttc.subscribe("lightbulb-discover/"+bulb+"/#", 0)
		mqttc.publish("lightbulb-discover/new_devices", "{\"msg\":\"Hi! My #LB id is "+bulb+" Please run the device setup - for help send any message to lightbulb-discover/"+bulb+"/help\",\"id\":\""+bulb+"\"}", qos=2, retain=True)
		print("Hi! Welcome to #LB")		
	mqttc.loop_forever()

# with open('obj.lbdata', 'w') as f: 
	# pickle.dump([home, room, cl, bulb], f)


def main():
	os.system('cls')
	print("Welcome to #LightBulb")
	try:
		mcon()
	finally:
		os.system('cls')
		print("\033[1;37;40m")
		print("\n Goodbye from #LB")
				


if __name__ == '__main__':
	main()