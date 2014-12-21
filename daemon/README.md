# Todo


# Done

+ catch ctrl-C
+ update wb with current energy at beginning or if it reboots
- only post once per minute for xively - decided to leave as is
+ fetch battery life and uptime from wristband, post to xively
	+ if fails, wait for a bit before trying again
+ need to maintain a small queue of bluetooth and xively threads, joining later?
    - xively threads don't need limiting because they will time out after 30s
+ what happens if thread throws exception, will parent catch it - still need to
  join
    - unhandled exception will kill thread but not affect parent
    - daemon threads don't need joining
+ deal with histroy from cc:
    


