# TRRC-Injection-Packer-Depth-Compliance
Checks Texas RRC injection/disposal permits for permitted injection zone depths and compares it to the most recent H-10 reported packer depths.
If packer depth is 100' above Top Injection Zone then the well is considered SWR 9/46 delinquent*. I recommend that the packer depth be verified using other records before evaluating decisions to pull well and move packer.

Uses Selenium web driver with python to scrape Texas RRC Online System. This web driver will be used with Google Chrome.
Chromedriver needs to be installed in the same folder that you are running the python script from.

User will have to enter the lease number. Results will be output to a csv file. A pie chart with the non-compliant packer counts will also be displayed.

*Statewide Rule 46, which governs injection or disposal into productive formations, provides greater flexibility within the general requirement that injected fluids be confined within the authorized injection interval. Rule 46 states that the packer must be set at least 200 feet below the production casing cement and at least 150 feet below the deepest usable quality groundwater. If, for example, a well was completed with 1200 feet of annular cement above the injection interval and the interval had 1000 feet of overlying clay/shale, then the packer could be set 1000 feet above the permitted zone. If, on the other hand, there was a small water sand 110 feet above the permitted zone, then the packer must be set below that water sand. One option to deal with this is to amend the proposed permitted injection zone to include that little water sand.

https://www.rrc.state.tx.us/oil-gas/publications-and-notices/manuals/injectiondisposal-well-manual/summary-of-standards-and-procedures/technical-review/technical-discussion-of-packer-setting-depth-issues/
