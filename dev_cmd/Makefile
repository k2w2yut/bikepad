gimxkeyboard:
	gimx --config key.xml -t GPP --window-events --status --nograb
gimxnet:
	gimx -t GPP --src 127.0.0.1:5050 --nograb --status
gimxnetbg:
	gimx -t GPP --src 127.0.0.1:5050 --nograb --status &
gimxpad:
	gimx --config LINUX_X360PadUsb.xml --dst 127.0.0.1:5050 --nograb --status
xboxdrv:
	#sudo rmmod xpad
	sudo xboxdrv --silent --detach-kernel-driver &
run: 
	make gimxnetbg
	make xboxdrv
	python bikepad_final.py
	
