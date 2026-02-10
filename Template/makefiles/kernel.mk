# common.mk
# This file is licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# Copyright (C) 2024, Advanced Micro Devices, Inc.
# Created by Alfred

# Kernel stuff
KERNEL_O_DIR := build/kernel
KERNEL_SRCS := $(wildcard ${HOME_DIR}/kernel/*.cc)
KERNEL_OBJS := $(patsubst ${HOME_DIR}/kernel/%.cc, ${KERNEL_O_DIR}/%.o, $(KERNEL_SRCS))
KERNEL_HEADERS := $(wildcard ${HOME_DIR}/kernel/*.h) $(wildcard ${HOME_DIR}/kernel/*.hpp)
OUTPUT_KERNEL_ASSEMBLY ?= false

${KERNEL_O_DIR}/%.o: ${HOME_DIR}/kernel/%.cc ${KERNEL_HEADERS}
	mkdir -p ${@D}
ifeq ($(DEVICE),npu1)
    ifeq ($(ENABLE_CHESSCC),1)
	cd ${@D} && xchesscc_wrapper ${CHESSCCWRAP2_FLAGS} -c $< -o ${@F}
    else # else for ENABLE_CHESSCC
	cd ${@D} && ${PEANO_INSTALL_DIR}/bin/clang++ ${PEANOWRAP2P_FLAGS} -DBIT_WIDTH=8 -c $< -o ${@F}
        ifeq ($(OUTPUT_KERNEL_ASSEMBLY), true) # Corrected syntax
	    ${PEANO_INSTALL_DIR}/bin/llvm-objdump -d -g -S -s -t -T -x --full-contents $@ > ${@:.o=.s}
	    ${PEANO_INSTALL_DIR}/bin/clang++ ${PEANOWRAP2P_FLAGS} -DBIT_WIDTH=8  -S -fverbose-asm   -o ${@:.o=.asm} $<
        endif # endif for OUTPUT_KERNEL_ASSEMBLY
    endif # endif for ENABLE_CHESSCC
else ifeq ($(DEVICE),npu2) # This 'else ifeq' structure is specific to GNU Make
    ifeq ($(ENABLE_CHESSCC),1)
	cd ${@D} && xchesscc_wrapper ${CHESSCCWRAP2P_FLAGS} -DNPU2 -c $< -o ${@F}
    else # else for ENABLE_CHESSCC
	cd ${@D} && ${PEANO_INSTALL_DIR}/bin/clang++ ${PEANOWRAP2P_FLAGS} -DBIT_WIDTH=8 -c $< -o ${@F}
        ifeq ($(OUTPUT_KERNEL_ASSEMBLY), true) # Corrected syntax
	    ${PEANO_INSTALL_DIR}/bin/llvm-objdump -d -g -S -s -t -T -x --full-contents $@ > ${@:.o=.s}
	    ${PEANO_INSTALL_DIR}/bin/clang++ ${PEANOWRAP2P_FLAGS} -DBIT_WIDTH=8  -S -fverbose-asm   -o ${@:.o=.asm} $<
        endif # endif for OUTPUT_KERNEL_ASSEMBLY
    endif # endif for ENABLE_CHESSCC
else # else for DEVICE type
	@echo "Device type not supported: $(DEVICE)"
endif # endif for DEVICE type