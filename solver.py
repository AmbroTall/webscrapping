# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:48:24 2022

@author: Asad Mehmood
"""

import logging
import time
import re
import random
import os
import urllib
import pydub
import speech_recognition as sr

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

global dev
dev = True

# Current Directory
current_directory = os.getcwd()


def print_log(text, error=False):
	if dev:
		print(text)
	else:
		if error:
			logging.error(text.strip())
		else:
			logging.info(text.strip())


def delay(browser, waiting_time=5):
	browser.implicitly_wait(waiting_time)


def solve_audio(driver, element):
	solved = False
	# switch to recaptcha audio challenge frame
	try:
		driver.switch_to.default_content()
		driver.switch_to.frame(element)

		# get the mp3 audio file
		delay(driver)
		# WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "audio-source")))
		audio_tag = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload-link")))
		# audio_tag = driver.find_element_by_id("audio-source")
		# src = audio_tag.get_attribute("src")
		src = audio_tag.get_attribute("href")
		print_log("[INFO] Audio src")

		folder_name = "recaptcha_audio"
		path_audio = os.path.join(current_directory, folder_name)
		if not os.path.exists(path_audio):
			print_log("Creating folder: '{}'".format(folder_name))
			os.makedirs(path_audio)

		path_to_mp3 = os.path.normpath(os.path.join(path_audio, "sample.mp3"))
		path_to_wav = os.path.normpath(os.path.join(path_audio, "sample.wav"))

	except Exception as e:
		error_str = "{}: {}".format(str(type(e).__name__), str(e))
		print_log(error_str, True)
		print_log("[ERR] Unable to Download Audio", True)

	try:
		# download the mp3 audio file from the source
		urllib.request.urlretrieve(src, path_to_mp3)
		# load downloaded mp3 audio file as .wav

		sound = pydub.AudioSegment.from_mp3(path_to_mp3)
		sound.export(path_to_wav, format="wav")
		sample_audio = sr.AudioFile(path_to_wav)
	except Exception as e:
		error_str = "{}: {}".format(str(type(e).__name__), str(e))
		print_log(error_str, True)
		print_log(
			"[ERR] Please run program as administrator or download ffmpeg manually, https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/",
			True)

	try:
		# translate audio to text with google voice recognition
		delay(driver)
		r = sr.Recognizer()
		with sample_audio as source:
			audio = r.record(source)
		key = r.recognize_google(audio)
		key = key.strip()
		print_log(f"[INFO] Recaptcha Passcode: {key}")

		# key in results and submit
		delay(driver)
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "audio-response")))
		audio_tag = driver.find_element_by_id("audio-response")
		audio_tag.clear()
		audio_tag.send_keys(key.lower())
		iii = random.randint(3, 5)
		time.sleep(iii)
		audio_tag.send_keys(Keys.ENTER)
		solved = True
		print_log("Recaptcha Solved")
	except Exception as e:
		solved = False
		error_str = "{}: {}".format(str(type(e).__name__), str(e))
		print_log(error_str)
		print_log("Unable to solve captcha.", True)

	if solved:
		driver.switch_to.default_content()

	return solved


def recaptcha_solver(driver, multi=False):
	recaptcha_solved = False

	# main program
	# auto locate recaptcha frames
	print_log("Waiting on Recaptcha...")
	clicks = False
	no_audio_handle = False
	no_iframe = False
	try:
		delay(driver)
		wait_time = 15

		if multi:
			i = 1
			www = i
			print_log("Waiting {} seconds for Recaptcha...".format(www))
			while not driver.current_url.endswith("captcha") and i <= www:
				time.sleep(i)
				i += 1
			wait_time = 1
		try:
			WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
			frames = driver.find_elements_by_tag_name("iframe")
			recaptcha_control_frame = None
			recaptcha_challenge_frame = None
			for index, frame in enumerate(frames):
				if re.search('reCAPTCHA', frame.get_attribute("title")):
					recaptcha_control_frame = frame

				if re.search('recaptcha challenge', frame.get_attribute("title")):
					recaptcha_challenge_frame = frame
			if not (recaptcha_control_frame and recaptcha_challenge_frame):
				print_log("[ERR] Unable to find recaptcha. Abort solver.", True)
			# sys.exit()
		except:
			print_log("No Recaptcha Found!")
			no_iframe = True

		if not no_iframe:
			try:
				# switch to recaptcha frame
				delay(driver)
				frames = driver.find_elements_by_tag_name("iframe")
				driver.switch_to.frame(recaptcha_control_frame)

				# click on checkbox to activate recaptcha
				WebDriverWait(driver, 30).until(
					EC.presence_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-border")))
				driver.find_element_by_class_name("recaptcha-checkbox-border").click()

				# switch to recaptcha audio control frame
				delay(driver)
				driver.switch_to.default_content()
				frames = driver.find_elements_by_tag_name("iframe")
				driver.switch_to.frame(recaptcha_challenge_frame)
				clicks = True
			except:
				print_log("Unable to click on I am not Robot.", True)

			# click on audio challenge
			ww = random.randint(3, 5)
			time.sleep(ww)
			try:
				WebDriverWait(driver, ww).until(EC.presence_of_element_located((By.ID, "recaptcha-audio-button")))
				el = driver.find_element_by_id("recaptcha-audio-button")
				el.click()
				clicks = True
			except:
				print_log("No Audio Handle or Recaptcha is solved.", True)
				clicks = False
				no_audio_handle = True
	except:
		# if ip is blocked.. renew tor ip
		print_log("[INFO] IP address has been blocked for recaptcha.", True)

	if clicks:
		# switch to recaptcha audio challenge frame
		recaptcha_solved = solve_audio(driver, recaptcha_challenge_frame)
		solve = True
		attempt = 1
		while solve and attempt <= 5:
			driver.switch_to.default_content()
			driver.switch_to.frame(recaptcha_challenge_frame)
			w = random.randint(3, 5)
			print_log("Attempt # {} to Solve again for {} seconds...".format(attempt, w))
			time.sleep(w)
			try:
				WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "audio-response")))
				audio_tag = driver.find_element_by_id("audio-response")
				audio_tag.send_keys('g')
				solve = solve_audio(driver, recaptcha_challenge_frame)
			except Exception as e:
				solve = False
				error_str = "{}: {}".format(str(type(e).__name__), str(e))
				print_log(error_str)

			if not solve:
				break
			attempt += 1

	driver.switch_to.default_content()

	if no_audio_handle:
		recaptcha_solved = True
		print_log("Recaptcha Solved")

	if not no_iframe:
		recaptcha_solved = True
	return recaptcha_solved, driver


if __name__ == '__main__':
	pass