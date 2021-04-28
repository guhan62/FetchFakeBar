"""
    Fetch Rewards Coding Exercise - SDET
    @Author: Hari Guhan, Engineers @ FetchRewards
    @Description: Find Fake Goldbars on a simulated CRA App
    @Date: 27th April 1600 - 1930
"""
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

import random as rd
import unittest

class FetchFakebars(unittest.TestCase):
    def setUp(self):
        """setUp UnitTest Case for Selenium Webdriver"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://ec2-54-208-152-154.compute-1.amazonaws.com/"
        self.accept_next_alert = True
        self.maxBars = 9
        self.foundBar = False
        self.balancedScales = False
        self.bars = [i for i in range(0, self.maxBars)]
        self.visitedBars = [False]* (self.maxBars)
        self.leftScale = self.reset_scales(self.bars)
        self.rightScale = self.reset_scales(self.bars)
    
    def test_grid(self):
        """Simulator to test the grid until we find the fake_bar"""
        driver = self.driver
        driver.get(self.base_url)
        while(not self.foundBar):
            if(8 - sum(self.visitedBars)==0):
                self.visitedBars = [False]* (self.maxBars)
                self.leftScale = self.reset_scales(self.bars)
                self.rightScale = self.reset_scales(self.bars)
                self.driver.find_element_by_xpath("(//button[@id='reset'])[2]").click()
                self.balancedScales = False
            self.generate_grid_scales()
            self.fill_grid("left", list({k:v for (k,v) in self.leftScale.items() if v!=-1}.keys()), list({k:v for (k,v) in self.leftScale.items() if v!=-1}.values()))
            self.fill_grid("right", list({k:v for (k,v) in self.rightScale.items() if v!=-1}.keys()), list({k:v for (k,v) in self.rightScale.items() if v!=-1}.values()))
            self.weigh_scales()
        #driver.find_element_by_id("coin_3").click()
        self.assertEqual(self.foundBar, True)

    def reset_scales(self, bars):
        """Reset Grid Index mapping to Bars"""
        return {x:-1 for x in bars}

    def generate_grid_scales(self):
        """Generate New grid Scale""" 
        # In case of Exhaustion of weights, reset and restart
        if(8 - sum(self.visitedBars)==0):
            self.visitedBars = [False]* (self.maxBars)
            self.leftScale = self.reset_scales(self.bars)
            self.rightScale = self.reset_scales(self.bars)
        # Generate Random Values, if = or Visited[left, right] - Loop until we get Random Values
        leftVal, rightVal = rd.choice(self.bars), rd.choice(self.bars)
        while(leftVal==rightVal or self.visitedBars[leftVal] or self.visitedBars[rightVal]):
            leftVal, rightVal = rd.choice(self.bars), rd.choice(self.bars)
        self.visitedBars[leftVal] = True
        self.visitedBars[rightVal] = True
        #print(self.leftScale, self.rightScale, self.visitedBars)
        # If any index/scale has a weight generate new pairs of indexes
        leftIdx, rightIdx = rd.choice(self.bars), rd.choice(self.bars)
        while(self.leftScale[leftIdx]!=-1 or self.rightScale[rightIdx]!=-1):
            leftIdx, rightIdx = rd.choice(self.bars), rd.choice(self.bars)
        self.leftScale[leftIdx] = leftVal
        self.rightScale[rightIdx] = rightVal


    def weigh_scales(self):
        """Click Weight Button and get the Score listings"""
        self.driver.find_element_by_id("weigh").click()
        self.get_score_listing()

    def fill_grid(self, board, gridCells, gridValues):
        """Fill Grid at Specified Indices, and Grid Values for respective Grid"""
        driver = self.driver
        for i in range(0, len(gridCells)):
            cellId = board+"_"+str(gridCells[i])
            driver.find_element_by_id(cellId).click()
            driver.find_element_by_id(cellId).clear()
            driver.find_element_by_id(cellId).send_keys(str(gridValues[i]))

    def find_fake_bar(self, board):
        """Find Fake bar, by looping all cells and finding right value from AlertBox"""
        driver = self.driver
        for i in range(0, self.maxBars):
            if(driver.find_element_by_id(board + "_" + str(i)).get_attribute("value") == ""):
                continue
            else:
                driver.find_element_by_id("coin"+"_"+str(i)).click()
                alertText = self.close_alert_and_get_its_text()
                if("Yay! You find it!" != alertText):
                    continue
                else:
                    self.assertEqual("Yay! You find it!", alertText)
                    self.foundBar = True
                    print("Fake Bar (in Board-{0}) => <Cell Index {1},Weight {2}>".format(board,i,driver.find_element_by_id(board + "_" + str(i)).get_attribute("value")))
                    #print("Fake Bar:",  driver.find_element_by_id(board + "_" + str(i)).get_attribute("value"))

    def get_score_listing(self):
        """Parse Game Info"""
        driver = self.driver
        weighingElements = [w_li.text for w_li in driver.find_elements_by_xpath("//div[@class=\"game-info\"]/ol/li")]
        print("Testing for scale ::", weighingElements[-1])
        scale = weighingElements[-1].split(' ')[1]
        if(scale == ">"):
            self.find_fake_bar("right")
        elif(scale == "<"):
            self.find_fake_bar("left")
        else:
            self.balancedScales = True
            return
        

    def close_alert_and_get_its_text(self):
        """Get Alert Text - generated from Katalon Recorder"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
