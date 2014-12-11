# Todo

- fetch battery life and uptime from wristband, post to xively
- how to deal with unfresh data from wristband?
- when starting, update wristband
- only post once per minute for xively
- only wait as long as necessary for gatttool - poll it?

# Done

+ need to maintain a small queue of bluetooth and xively threads, joining later?
    - xively threads don't need limiting because they will time out after 30s
+ what happens if thread throws exception, will parent catch it - still need to
  join
    - unhandled exception will kill thread but not affect parent
    - daemon threads don't need joining
+ deal with histroy from cc:
    


