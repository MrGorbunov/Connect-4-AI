# Style Guide



---
## Naming / Cosmetic

**`names_are_underscore_seperated`** so as to fit with pygame

**`GLOBAL_CONSTANTS_ARE_UPPERCASE`**, even though python does not support global constants, these signal not to change the value

All function names have a verb in their name. Use **`check_vertical_win():`** over **`vertical_win():`**

Always have function lines - the **`''' Description of function '''`** that is the first line of a function

\#-------------- These are used to seperate / group parts of code ----------------------------


---
## Functional / Architecture

Functions either return something and are fully parameterized (do not change state) *or* only touch state and return nothing
