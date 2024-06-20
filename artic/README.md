Disk 674 has enable reader and seems to contain binaries for votalker, artic, etc.

EPROM Notes

  * A0-A12 to ISA BUS A0-A12
  * OE GND
  * CE 245-20, 32-11
  * O0 245-4  ( buffer to D0)
  * O1 245-6
  * O2 245-8

MAP Jumper

  * 1 - 138-7  Y7
  * 2 - 138-10 Y5
  * 3 - 138-12 Y3
  * 3 - 138-14 Y1

  * C - 04-1 (invert to SSI-263 CS0)

  * 138-A is A5
  * 138-B is A6
  * 138-C is A7
  * 138-!G2A is A8
  * 138-!G2B is 32-3  (A4 or AEN)
  * 138-G1 is A9

Address decode must be

  * Map 1 - 101110XXXX - 2E0 to 2EF 
  * Map 2 - 101010XXXX - 2A0 to 2AF
  * Map 3 - 100110XXXX - 260 to 26F
  * Map 4 - 100010XXXX - 220 to 22F

SSI-263

  * CS0 is MAP-C
  * !CS1 is IOW
  * A/R is inverted via 04-3 to 04-4 to the interrupt jumper
  * Clock comes from 161, which is a divider, probably derived from bus clock

Reading
  * IOR goes to 32-9 where it is ORed with MAP-C
  * Output on 32-8 goes to 32-4 where it is ORed with 04-9/04-10 which is inverted from 04-11 which comes from A3
  * Output from 32-6 goes to 244-1/19
  * The read port is probably 2E8/2A8/268/228
  * I don't think it can be polled for status, because !CS1 is IOW, and R/!W is tied to GND.

Software ideas
  * Heathkit HV-2000 driver might use port 300 by default.
  * "DEVICE=VOICE.SYS XXX" where XXX is port number
  * Heathkit driver won't work because it doesn't support IRQ, only polling.
