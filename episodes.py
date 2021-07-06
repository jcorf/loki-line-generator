from script_structure import ScriptStructure, combine_scripts
from script_cleaner import ScriptCleaner

ep1 = ScriptCleaner("https://transcripts.fandom.com/wiki/Glorious_Purpose")
ep2 = ScriptCleaner("https://transcripts.fandom.com/wiki/The_Variant")
ep3 = ScriptCleaner("https://transcripts.fandom.com/wiki/Lamentis")
ep4 = ScriptCleaner("https://transcripts.fandom.com/wiki/The_Nexus_Event")

structure = combine_scripts(ep1, ep2, ep3, ep4)





