             Notes on the DE430 and DE431 Planet and Lunar Ephemerides
                            C. Acton   8/15/2013

JPL's Solar System Dynamics Group has released two new planet ephemeris files: DE430 and DE431.
Each contains ephemeris data for the planet barycenters--Mercury through Pluto 
(NAIF ID codes 1 through 9), plus the Sun (10), the earth mass center (399) and the moon (301).
Also present are the Mercury and Venus mass centers--199 and 299 respectively--since these have
the same locations as the respective barycenters.

The difference between DE430 and DE431 is mainly in the dynamical model for the Earth's Moon.
DE430 uses a more complete dynamical model which produces a slightly more accurate ephemeris for 
the Moon. However the dynamical model used for DE430 includes a model of an excited lunar 
core/mantle rotation interaction which does not extrapolate into the distant past well. 
Therefore DE430 was integrated over a limited time span. DE431 does not include the excited 
core/mantle state so is less accurate for times near the current epoch but is more accurate for 
the distant past.

The difference in the positions of the planets agree to better than 0.001 km over the time 
period covered by DE430, a difference which is not statistically distinguished by the currently 
available data. The difference in the lunar position is less than 0.01 km over the period 
1950 to 2050.

As of the date of this posting DE430 is now considered the official lunar/planetary ephemeris, 
suitable for all users/uses.

For those whose need of a planet ephemeris can be satisfied by the DE430 time span, and for 
those in need of the most accurate JPL-produced lunar ephemeris, DE430 is now considered 
the official export ephemeris.

  de430.bsp
  Approximate file size:   120 Mbytes
  Approximate time span:   1550 Jan 01 to 2650 Jan 22


For those in need of a very long planetary ephemeris, and where the degradation in the lunar 
state is not significant, DE431 provides longer coverage.

  de431.bsp
  Approximate file size:  3.2 Gbytes
  Approximate time span:  13201 B.C. to 17191 A.D.

NOTE ON MARS: Starting with the DE43x files the location of the Mars mass center (NAIF ID = 499) 
is no longer included in the planet ephemeris; only the Mars barycenter (ID = 4) is present.

The offset between the location of the Mars barycenter and the  Mars mass center is extremely 
small--about 20 cm--so most SPICE users could use the Mars B.C. (4) instead of the Mars mass 
center (499). But if you do wish or need to have the location of 499 available in your program, 
you must also load a Mars  satellite ephemeris such as mar097.bsp.

For those familiar with JPL's "Horizons" on-line ephemeris system, it now uses DE431 for 
its planetary ephemeris.

            ---------------------------------------------

For more details about SPICE planet and satellite ephemeris files, known as SPK files, including 
how to read them using SPICE Toolkit software, see the SPK tutorial (PDF format file name is 
"19_spk") available from the NAIF website here:
  
   http://naif.jpl.nasa.gov/naif/tutorials.html

