#!/usr/bin/env python# -*- coding: utf-8 -*-import timeclass WarTimer():    def __init__(self,warRun,target,callfunc,timespace = 1,repeattimes = 1,isRepeatforever = False,isRunBefor = False):        self.timespace = timespace              #时间间隔        self.repeattimes = repeattimes            #重复次数        self.isRepeatforever = isRepeatforever     #是否无限重复        self.isRunBefor = isRunBefor        self.target = target        self.callfunc = callfunc                self.nextRun = 0.0                #下次运行时间        self.warRun = warRun        self.setTimer()    def setTimer(self):        self.nextRun = self.warRun.nowTime + self.timespace        if self.isRunBefor:            self.isRunBefor = False            self.callfunc()    def updata(self):        if self.isRepeatforever:            self.nextRun += self.timespace            self.callfunc()            self.warRun.updataTimerForList(self)        elif self.repeattimes > 1:            self.repeattimes -=1            self.nextRun += self.timespace            self.callfunc()            self.warRun.updataTimerForList(self)class WarRun():    def __init__(self):        self.eventlist = []             #事件运行定时器列表        self.nowTime = 0        self.isWarNotEnd = True    def addTimerFunc(self,target,callfunc,timespace = 1,isRepeatforever = False,repeattimes = 1,isRunBefor = False):        wartimer = WarTimer(self,target,callfunc,timespace,repeattimes,isRepeatforever,isRunBefor)        self.updataTimerForList(wartimer)    def updataTimerForList(self,ptimer):        at = 0        if self.eventlist:            for n in range(len(self.eventlist)):                if ptimer.nextRun <= self.eventlist[n].nextRun:                    at = n                    break                else:                    at = -1            if at == -1:                self.eventlist.append(ptimer)            else:                self.eventlist.insert(at, ptimer)        else:            self.eventlist.append(ptimer)        teststr = ''        for ev in self.eventlist:            teststr += '%f '%(ev.nextRun)        print '%s\n'%teststr    def runLoop(self):        while self.isWarNotEnd:            time.sleep(1)            if self.eventlist:                ptimer = self.eventlist.pop(0)                ptimer.updata()            else:                breakif __name__ == '__main__':    warrun = WarRun()    def functest(a = 1):        print a    warrun.addTimerFunc(1, functest, timespace = 0.1, isRepeatforever = True, repeattimes = 2 )    def functest2(a = 2):        print a    warrun.addTimerFunc(2, functest2, timespace = 0.3,isRepeatforever = True, repeattimes = 10)    warrun.runLoop()