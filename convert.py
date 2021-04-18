import sys
import os

name = '' 
counter = 0
triggers = ['']
triggers.append('//Converted using Xineras converting script')

cfg_files = [f for f in os.listdir('.') if f.endswith('.cfg')]
if len(cfg_files) != 1:
    raise ValueError('should be only one txt file in the current directory')
    
def positionTrigger(center,size,name,angle):
    string = 'sar_speedrun_cc_rule "' + name + '" zone center='
    for coord in center:
        string += str(coord)
        if(coord != center[len(center)-1]):
            string += ','
    string += ' size='
    for coord in size:
        string += str(coord)
        if(coord != size[len(center)-1]):
            string += ','
    string += ' angle=' + angle
    triggers.append(string)
    
def otherTrigger(name,id,type):
    string = 'sar_speedrun_cc_rule "' + name + '" entity targetname=' + id + ' inputname=' + type.replace(';','').replace('\n','')
    triggers.append(string)

for file in cfg_files:
    with open(file, 'r+') as f:
        lines = f.readlines()
        
        for line in lines:
            cfg = open(file,'w')
            words = line.split(' ')
            if(counter == 0 or counter == 1):
                counter = counter
            elif(counter == 2):
                mapname = ''
                for word in words:
                    if word == words[0]:
                        counter = counter
                    else:
                        mapname += word.replace('"','').replace('\n','')
                map = file.replace('.cfg','')
                triggers.append('sar_speedrun_cc_start "' + mapname + '" map=' + map + ' action=split')
                triggers.append('sar_speedrun_cc_rule "Start" load action=force_start')
            elif(len(words) > 4):
                center = [round((float(words[2])+float(words[5]))/2,2),round((float(words[3])+float(words[6]))/2,2),round((float(words[4])+float(words[7]))/2,2)]
                size = [round(float(words[5])-float(words[2]),2),round(float(words[6])-float(words[3]),2),round(float(words[7])-float(words[4]),2)]
                name = words[1]
                angle = words[8].replace('\n','').replace(';','')
                positionTrigger(center,size,name,angle)
            else:
                name = words[1]
                id = words[2]
                type = words[3]
                otherTrigger(name,id,type)
            counter += 1
        final = ''
        triggers.append('sar_speedrun_cc_rule "Finish" flags action=stop')
        triggers.append('sar_speedrun_cc_finish')
        for trigger in triggers:
            final += str(trigger)
            final += '\n'
        f.write(final)