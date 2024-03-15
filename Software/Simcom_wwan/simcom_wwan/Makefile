obj-m:=simcom_wwan.o
simcom_wwanmodule-objs:=module
MAKE:=make
PWD=$(shell pwd)
VER=5.10.104-tegra
KERNEL_BUILD=/lib/modules/$(VER)/build
INSTALL_ROOT=/

default:
	$(MAKE) -C $(KERNEL_BUILD) M=$(PWD) modules
clean:
	$(MAKE) -C $(KERNEL_BUILD) M=$(PWD) clean
install:
	$(MAKE) -C $(KERNEL_BUILD) M=$(PWD) INSTALL_MOD_PATH=$(INSTALL_ROOT) modules_install
