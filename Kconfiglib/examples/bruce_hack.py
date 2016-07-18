# Loads a Kconfig and a .config and prints information about a symbol.

import kconfiglib
import sys

# Create a Config object representing a Kconfig configuration. (Any number of
# these can be created -- the library has no global state.)
conf = kconfiglib.Config(sys.argv[1])

# Load values from a .config file. 'srctree' is an environment variable set by
# the Linux makefiles to the top-level directory of the kernel tree. It needs
# to be used here for the script to work with alternative build directories
# (specified e.g. with O=).
#conf.load_config("$srctree/arch/x86/configs/i386_defconfig")
conf.load_config("/home/bruce/poky/build/tmp/work/genericx86-poky-linux/linux-yocto/4.4.10+gitAUTOINC+870134f4bf_bc64c81245-r0/linux-genericx86-standard-build/.config")

# Print some information about a symbol. (The Config class implements
# __getitem__() to provide a handy syntax for getting symbols.)
#print(conf["SERIAL_UARTLITE_CONSOLE"])
#print(conf["GENERIC_BUG"])
print(conf["X86_VSMP"])


print( "========== vars that depend on this ============")
x86 = conf["X86_VSMP"]
for sym in conf:
    if x86 in sym.get_referenced_symbols():
        print(sym.get_name())

print( "========== prompt ============")
print(x86.get_prompts())

#print( "========== references ============")
refs = x86.get_referenced_symbols()
#for s in refs:
#    print(s.get_name() + " [" + s.get_value() + "]")

#print( "========== selects ============")
selected = x86.get_selected_symbols()
#for sel in selected:
#    print( sel.get_name() )

print( "========== depends ============")

prompts_str_rows = []
for prompt, cond_expr in x86.orig_prompts:
    if cond_expr is None:
        print(prompt)
    else:
        f = conf._expr_val_str(cond_expr)
        print(f)

# if it is a referenced variable, but not selected, then it is a
# dependency
depends_string=""
for s in refs:
    if not s in selected:
        depends_string += " " + s.get_name() + " [" + s.get_value() + "]"

print(depends_string)

