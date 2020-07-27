# TRRC-Packer-Depth-Delinquency
Checks Texas RRC injection/disposal permits for injection zone depths and compares it to the most recent H-10 reported packer depths.

Use selenium web driver with python to scrape Texas RRC Online System.
Open Injection/Disposal Permit Query.
User will have to enter lease name or number.
Open Injection/Disposal Permit Detail.

If H-10 Status is active proceed to get:
  UIC Number
  Approved Packer Depth
  Top Injection Zone
  Bottom Injection Zone
Output attributes to dataframe.

Use web driver to scrape RRC Online System. Open H-10 Annual Disposal/Injection Well Monitoring Report Query.
Use UIC numbers from dataframe to search H-10 Records.
Open most recent submitted H-10.
Get "17. Depth of Tubing Packer:"

If packer depth is 100' above Top Injection Zone then the well is SWR 9 delinquent (injection/disposal into non-productive zone).
If packer depth is 1000' above Top Injection Zone, then the well is SWR 46 delinquent*.

*Statewide Rule 46, which governs injection or disposal into productive formations, provides greater flexibility within the general requirement that injected fluids be confined within the authorized injection interval. Rule 46 states that the packer must be set at least 200 feet below the production casing cement and at least 150 feet below the deepest usable quality groundwater. If, for example, a well was completed with 1200 feet of annular cement above the injection interval and the interval had 1000 feet of overlying clay/shale, then the packer could be set 1000 feet above the permitted zone. If, on the other hand, there was a small water sand 110 feet above the permitted zone, then the packer must be set below that water sand. One option to deal with this is to amend the proposed permitted injection zone to include that little water sand.
https://www.rrc.state.tx.us/oil-gas/publications-and-notices/manuals/injectiondisposal-well-manual/summary-of-standards-and-procedures/technical-review/technical-discussion-of-packer-setting-depth-issues/
