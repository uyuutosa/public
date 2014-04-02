#!/usr/bin/env python
#-*- coding:utf-8 -*-
class grace_aliases():
    coldic = {"white": 0,
              "black": 1,
              "red": 2,
              "green": 3,
              "blue": 4,
              "yellow": 5,
              "brown": 6,
              "grey": 7,
              "violet": 8,
              "cyan": 9,
              "magenta": 10,
              "orange": 11,
              "indigo": 12,
              "maroon": 13,
              "turquoise": 14,
              "green": 15}

    def show_color(self):
        print "       Color list"
        print "------------------------"
        print " %-12s%-12s" %("Color","Color name")
        print "------------------------"
        for col, num in self.coldic.items(): print " %-12s%-12s" %(col, num)
        print "------------------------"

    def ifcolname(self, colname):
        if type(colname) == str: return self.coldic[colname]
        
