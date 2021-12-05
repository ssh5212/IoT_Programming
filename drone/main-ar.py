#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import tello
import time
import cv2	
import time
import friend_send
url_On = 'http://192.168.0.34/LED_B=OFF' # 서보 모터 제어
url_Off = 'http://192.168.0.34/LED_B=ON'

friend_send.kakao()

def main():

	aruco = cv2.aruco
	dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

	drone = tello.Tello('', 8889, command_timeout=.01) # 드론과 네트워크 간 연결을 시도

	current_time = time.time()	
	pre_time = current_time

	time.sleep(0.5)

	pre_idno = None
	count = 0

	try:
		while True:
			frame = drone.read()
			if frame is None or frame.size == 0:
				continue 

			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			small_image = cv2.resize(image, dsize=(480,360) ) # 드론의 카메라를 이용하여 Frame 단위로 read

			corners, ids, rejectedImgPoints = aruco.detectMarkers(small_image, dictionary)
			aruco.drawDetectedMarkers(small_image, corners, ids, (0,255,0)) # 그림(마커) 인식, 인식된 범위를 표시

			try:
				if ids != None:
					idno = ids[0,0]

					if idno == pre_idno:
						count+=1

						if count > 50:
							print("ID=%d"%(idno))
							
							if idno == 0:
								print("takeoff, close")
								print("land, open")
								requests.get(url=url_On) # 서보 모터 제어
								time.sleep(10)
								requests.get(url=url_Off)
							elif idno == 1:
								drone.land()

							elif idno == 2:
								drone.move_up(0.3)
							elif idno == 3:
								drone.move_down(0.3)
							elif idno == 4:
								drone.rotate_ccw(90)
							elif idno == 5:
								drone.rotate_cw(90)
							elif idno == 6:
								drone.move_forward(0.3)
							elif idno == 7:
								drone.move_backward(0.3)
							elif idno == 8:
								drone.move_left(0.3)
							elif idno == 9:
								drone.move_right(0.3)
							
							count = 0
					else:
						count = 0

					pre_idno = idno
				else:
					count = 0

			except ValueError as e:
				print("ValueError")

			cv2.imshow('OpenCV Window', small_image)

			key = cv2.waitKey(1)
			if key == 27:
				break
			elif key == ord('t'):
				drone.takeoff()
			elif key == ord('l'):
				drone.land()
			elif key == ord('w'):
				drone.move_forward(0.3)
			elif key == ord('s'):
				drone.move_backward(0.3)
			elif key == ord('a'):
				drone.move_left(0.3)
			elif key == ord('d'):
				drone.move_right(0.3)
			elif key == ord('q'):
				drone.rotate_ccw(20)
			elif key == ord('e'):
				drone.rotate_cw(20)
			elif key == ord('r'):
				drone.move_up(0.3)
			elif key == ord('f'):
				drone.move_down(0.3)

			current_time = time.time()
			if current_time - pre_time > 5.0 :
				drone.send_command('command')
				pre_time = current_time

	except( KeyboardInterrupt, SystemExit):
		print( "SIGINT" )

	del drone

if __name__ == "__main__":
	main()