## User Experience
### Cheapjack Feedback

![felix with wristband image](https://github.com/cheapjack/cheapjack.github.io/blob/master/tumblr_files/tumblr_nk70a9PXSf1r2ybsso2_540.jpg)

Aside from some initial setup issues of wifi with dongle on new pi (more to do with me only using wired in pi's) and finding and setting a max current value it was quite reliable but occasionally it would seem to go off for no apparent change in energy use. Of course it was hard to avoid sudden spikes in data or spikes in boiler useage from the Current Cost.

We learnt as a family that the boiler pump was a hidden cost of the heating: it can come off and on at unexpected times and that the cost of dishwasher is higher than we expected.

It also revealed a hidden cost to underfloor heating that although efficient it showed how much the pump seemed to come off and on to keep track of the thermostat.

I suspect I needed to spend a bit more time checking the accuracy of the current cost unit itself. From the kids perspective they realised just how power hungry xbox's can be!

It did seem to be that sudden changes, not necessarily rises, in energy use triggered the wristband. The rumble also seemed unnecessarily long and it would be useful to have a varying scale of rumble length and intensity.

I would say it very quickly becomes something that the children and adults just don't want to wear and the pester power element although exciting did make you eventually take it off. I started making a cover for it to protect the rumble pack and made a new lower profile wristband that seemed a bit more appealing to wear. I did wonder how allowing a choice of fabric band would be nice and could imagine it being rolled out and styled ergnomically like this [BluetoothLE device for tagging music](http://www.skute.me/)


### Old Habits Die Hard

As a family we ended up leaving it on the mantelpiece so that it could alert us to unexpected spikes in use but could not quite tune it well enough to tell whether individual lights where left on upstairs or not, but could see that it could be tuned to specific uses like this. A nice docking station could be a way to allow this while also having a place to recharge.

There were times that we just let it de-charge as it became an annoying notification to be very honest! After a while you are aware of energy use but override your money saving desires and the notification becomes unwanted. A week off and we were happy to have it on again; in a way can see how it could fade in and out of use; not every notification is wanted at all times, in the same way you can just not get around to changing central heating settings.

I think something that could work is combining it with another 'use' like an ID tag that you need to have anyway; the tricky thing is having to keep wanting/needing to wear it I think; if it could have a parrallel use; like a mp3 player/torch/radio for example. The beauty of it is its low profile and ability to run from a pi; it appeals to the pi/arduino/oomlout using hobbyist and can see that this could potentially be a real potential market for it.

### Take Your Toys To Work

I also wondered whether an NFC tag could be incorporated to make it easily point to visualised data or graphs on mobile devices. I can see how the system itself could be adapted to suit other needs: for example @DoESLIverpool we monitor current in our workshop laser cutter and wondered about combining it with a workshop RFID tag that you need in order to enter and use the room when you've booked it.

A common problem is that people new to the laser cutter forget to monitor the temperature which can lead to damaging the laser tube; and to be honest most people just using it for the day basically dont care enough to do this. A physical alert on a wristband would work as they need it to get in and out of the workshop and its alot more difficult to forget! Its easy to leave a fob in the bottom of a bag and forget where the wristband even if forgotten would easily be found (but less easily returned perhaps). I'd be interested in buying one to try in this context.

<img src="https://cloud.githubusercontent.com/assets/128456/7890203/5ad3c75e-063c-11e5-849a-b749d4d3f688.jpg" width="200">

I also liked idea of 3D printed shaped covers related to monthly energy use somehow and this could be something people could choose and either print themselves or have printed via Shapeways. You can see my prototype Felix and I made using a week's energy useage graph, a big peak on useage as we had a cold spell on Thursday and people over for dinner.

I also liked the idea of it being able to send messages perhaps triggering lights/heating turned off using energenie kits or connecting it to [node-red](http://nodered.org/)

It also seemed a cheap entry into bluetooth LE as a piece of wearble technology and many people were interested in it at our  Wearables hackday at DoESLiverpool last week.

### Workshops

I think to run as a workshop you would need to think carefully where and how the engagement is happening, where the current cost monitor would be used etc; it could be more about energy use of electrical devices in the classroom rather than school energy use; depending on school of course. Id imagine you could use to show the energy use of a PC or classroom projector?

It may be that 4 or so devices might be useful that could respond in different ways if given to a class; it may be worth sketching out a lesson plan with a school to see how it works, I had hoped to do this with a group from a school in liverpool but the host organiser changed the remit of the school groups work so they only got a cursory demo of the device.

### DIY

As a raspberry pi intermediate project I think its got real potential: whether the core group of people who will take up its use is the beginner  market is unclear i think. It would be great to make a foolproof how-to easy for someone to plug and play but it could be a lot of work when the majority interested could potentially bypass it. That said I would benefit from the code commented 'for idiots' and some troubleshooting tips, I will contribute some suggestions for this.

I think a recommended parts list (for wifi dongles/differing pi model etc) would be good even this is hard to do as suppliers change etc. I really appreciated and benefitted from being part of the testing group and only wish I'd had more time to modify it's use in the home!
