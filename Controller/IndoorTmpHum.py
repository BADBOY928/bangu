# -*- coding: UTF-8 -*- 
'''
Controller.IndoorTmpHum is a part of the project bangu.
bangu is an open-source project which follows MVC design pattern mainly based on python.

Copyright (C) 2014 - 2016, Vlon Jang(WeChat:wangqingbaidu)
Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China.

The codes are mainly developed by Zhiwei Zhang.
As an open-source project, your can use or modify it as you want.

Contact Info: you can send an email to 564326047@qq.com(Vlon) 
  or visit my website www.wangqingbaidu.cn

Note: Please keep the above information whenever or wherever the codes are used.
'''
import GetBanguHome
from datetime import datetime
from utils.ReadConfig import configurations
import time, os
from Model import ModelDB
from Model import model
from Controller import putErrorlog2DB

def GetTmpHum2DB(cfg = configurations.get_tmphum_pin_setting(), db = model):
    """
    This method is used to put indoor temperature and humidity to DB.
    One who want to use this must `make` in Sensor Directory which generate exec file.
    @map2writingPi: variable maps Board pins to writingPi pins. You can get details by
    referring to http://wiringpi.com/pins/.
    Parameters
    -------------
    @cfg: Bangu system basic settings.
    @db: which DB connection to be used, Test use global. Thread use own. 
    """
    home = GetBanguHome.getHome()
    cmd = os.path.join(home, 'Controller/Sensors/TmpHum ')
    
    try:
        if cfg:
            map2writingPi = {16:'4', 18:'5'}
            if map2writingPi.has_key(cfg['pin']):
                cmd += map2writingPi[cfg['pin']]

        hum_tmp = os.popen(cmd).read()
        if hum_tmp:
            humtmp = {}
            hum, tmp = hum_tmp.replace('\n', '').split()
            humtmp['hum'] = int(hum)
            humtmp['tmp'] = int(tmp)
            humtmp['datetime'] = datetime.now()
            db.insert_tmphum(humtmp)            
    
    except Exception,e:
        putErrorlog2DB('ThreadIndoorTmpHum2DB', e, db)
        pass
        
    
def ThreadIndoorTmpHum2DB(decay = 5):
    db = ModelDB()
    while True:
        GetTmpHum2DB(db = db)
        time.sleep(decay)
        
if __name__ == '__main__':
    ThreadIndoorTmpHum2DB()
    desc = model.get_latest_tmphum()
    print desc.hum, desc.tmp