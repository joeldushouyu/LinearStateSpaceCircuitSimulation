	.text
	.file	"mainKernel.cc"
	.globl	_Z31retrieveMatrixOFfsetBaseOnStatejiPf // -- Begin function _Z31retrieveMatrixOFfsetBaseOnStatejiPf
	.p2align	4
	.type	_Z31retrieveMatrixOFfsetBaseOnStatejiPf,@function
_Z31retrieveMatrixOFfsetBaseOnStatejiPf: // @_Z31retrieveMatrixOFfsetBaseOnStatejiPf
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		mul	r0, r1, r0
	ret	lr
	mova	r1, #2                          //  Delay Slot 5
	lshl	 r0, r0, r1                     //  Delay Slot 4
	movs	p0, p1;		mov	m0, r0          //  Delay Slot 3
	padda	 [p0], m0                       //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end0:
	.size	_Z31retrieveMatrixOFfsetBaseOnStatejiPf, .Lfunc_end0-_Z31retrieveMatrixOFfsetBaseOnStatejiPf
                                        // -- End function
	.globl	_Z17accum_float_valuePfS_ii     // -- Begin function _Z17accum_float_valuePfS_ii
	.p2align	4
	.type	_Z17accum_float_valuePfS_ii,@function
_Z17accum_float_valuePfS_ii:            // @_Z17accum_float_valuePfS_ii
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		nopb	;		jl	#_Z10accumValueIfEvPfS0_ii;		nops	
	nop	                                //  Delay Slot 5
	paddxm	 [sp], #64                      //  Delay Slot 4
	st	 lr, [sp, #-64]                 // 4-byte Folded Spill Delay Slot 3
	nop	                                //  Delay Slot 2
	event	#0                              //  Delay Slot 1
	lda	 lr, [sp, #-64];		nopb	;		nops	;		event	#1;		nopm	;		nopv	 // 4-byte Folded Reload
	nopx	
	nop	
	nop	
	nop	
	nop	
	nop	
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	paddxm	 [sp], #-64                     //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end1:
	.size	_Z17accum_float_valuePfS_ii, .Lfunc_end1-_Z17accum_float_valuePfS_ii
                                        // -- End function
	.section	.text._Z10accumValueIfEvPfS0_ii,"axG",@progbits,_Z10accumValueIfEvPfS0_ii,comdat
	.weak	_Z10accumValueIfEvPfS0_ii       // -- Begin function _Z10accumValueIfEvPfS0_ii
	.p2align	4
	.type	_Z10accumValueIfEvPfS0_ii,@function
_Z10accumValueIfEvPfS0_ii:              // @_Z10accumValueIfEvPfS0_ii
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		nopb	;		paddxm	 [sp], #64;		nops	
	st	 p7, [sp, #-64]                 // 4-byte Folded Spill
	mova	r2, #2;		st	 r8, [sp, #-56];		mov	p7, p1 // 4-byte Folded Spill
	st	 p6, [sp, #-60];		lshl	 r0, r0, r2 // 4-byte Folded Spill
	movs	p6, p0;		lshl	 r1, r1, r2;		mov	m0, r0
	padda	 [p6], m0;		st	 lr, [sp, #-52];		mov	m0, r1 // 4-byte Folded Spill
	padda	 [p7], m0;		movxm	r8, #8118
	.p2align	4
.LBB2_1:                                // %for.cond3.preheader
                                        // =>This Inner Loop Header: Depth=1
	lda	 r1, [p6], #4;		nopb	;		nopxm	;		nops	
	jl	#__addsf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	movx	r2, #0                          //  Delay Slot 1
	lda	 r2, [p6], #4;		nopb	;		nopxm	;		nops	
	jl	#__addsf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r1, r0                          //  Delay Slot 1
	st	 r0, [p7], #4;		nopx	
	lda	 r1, [p6], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4;		jl	#__addsf3
	st	 r0, [p7], #4                   //  Delay Slot 5
	st	 r0, [p7], #4                   //  Delay Slot 4
	st	 r0, [p7], #4                   //  Delay Slot 3
	st	 r0, [p7], #4                   //  Delay Slot 2
	mova	r2, #0                          //  Delay Slot 1
	lda	 r2, [p6], #4;		nopb	;		nopxm	;		nops	
	jl	#__addsf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r1, r0                          //  Delay Slot 1
	st	 r0, [p7], #4;		nopx	
	lda	 r1, [p6], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4;		jl	#__addsf3
	st	 r0, [p7], #4                   //  Delay Slot 5
	st	 r0, [p7], #4                   //  Delay Slot 4
	st	 r0, [p7], #4                   //  Delay Slot 3
	st	 r0, [p7], #4                   //  Delay Slot 2
	mova	r2, #0                          //  Delay Slot 1
	lda	 r2, [p6], #4;		nopb	;		nopxm	;		nops	
	jl	#__addsf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r1, r0                          //  Delay Slot 1
	nopa	;		nopb	;		nopx	;		st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4
	st	 r0, [p7], #4;		add	r8, r8, #-3
	st	 r0, [p7], #4;		jnz	 r8, #.LBB2_1
	st	 r0, [p7], #4                   //  Delay Slot 5
	st	 r0, [p7], #4                   //  Delay Slot 4
	st	 r0, [p7], #4                   //  Delay Slot 3
	st	 r0, [p7], #4                   //  Delay Slot 2
	st	 r0, [p7], #4                   //  Delay Slot 1
// %bb.2:                               // %for.cond.cleanup
	lda	 lr, [sp, #-52];		nopb	;		nopxm	 // 4-byte Folded Reload
	nop	
	nop	
	nop	
	lda	 p7, [sp, #-64]                 // 4-byte Folded Reload
	lda	 p6, [sp, #-60]                 // 4-byte Folded Reload
	lda	 r8, [sp, #-56]                 // 4-byte Folded Reload
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	paddxm	 [sp], #-64                     //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end2:
	.size	_Z10accumValueIfEvPfS0_ii, .Lfunc_end2-_Z10accumValueIfEvPfS0_ii
                                        // -- End function
	.text
	.globl	_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_ // -- Begin function _Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_
	.p2align	4
	.type	_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_,@function
_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_: // @_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		nopb	;		nops	;		movxm	ls, #.LBB3_1;		nopv	
	mova	r2, #7;		nopb	;		movxm	le, #.L_LEnd0
	add.nc	lc, r2, #0
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		vldb	 x0, [p1, #0];		nops	;		movxm	r1, #16256;		nopv	
	mova	r0, #0;		nopb	;		nops	;		movxm	r16, #65280;		nopv	
	nopa	;		nopb	;		nops	;		nopx	;		vbcst.32	 x2, r0;		nopv	
	nopa	;		nopb	;		nops	;		nopx	;		vbcst.16	 x4, r1;		nopv	
	nopa	;		nopb	;		nops	;		nopx	;		mov	r1, r0;		nopv	
	mova	r1, #60;		nopb	;		nops	;		nopx	;		vbcst.64	 x6, r1:r0;		nopv	
	.p2align	4
.LBB3_1:                                // %_ZNK3aie6vectorIfLj16EE3getEj.exit
                                        // =>This Inner Loop Header: Depth=1
	vlda	 bmll0, [p0], #64;		nopb	;		nops	;		nopxm	;		nopv	
	vextract.32	 r2, x0, r0, vaddsign1
	nop	
	vbcst.32	 x8, r2
	vmov	bmll2, x8
	nop	
	vconv.bf16.fp32	 wl1, bmll2
	vconv.bf16.fp32	 wl10, bmll0
	vsel.32	 x5, x1, x2, r16
	vsel.32	 x3, x10, x2, r16
	vmsc.f	dm1, dm1, x5, x4, r1
	vmov	bmll1, x8;		vmsc.f	dm2, dm0, x3, x4, r1
	nop	
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll1
	vconv.bf16.fp32	 wl7, bmll2
	vsel.32	 x9, x9, x2, r16
	vsel.32	 x11, x7, x2, r16
	vmsc.f	dm4, dm1, x9, x4, r1
	vmsc.f	dm3, dm2, x11, x4, r1
	nop	
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl10, bmll4
	vconv.bf16.fp32	 wl8, bmll3
	vsel.32	 x10, x10, x2, r16
	vsel.32	 x8, x8, x2, r16
	nop	
	vmul.f	dm0, x8, x10, r1
	vmul.f	dm2, x8, x9, r1
	nop	
	vmul.f	dm1, x11, x10, r1
	vadd.f	dm0, dm0, dm2, r1
	nop	
	vmul.f	dm3, x3, x10, r1
	vadd.f	dm0, dm0, dm1, r1
	nop	
	vmul.f	dm4, x11, x9, r1
	vadd.f	dm0, dm0, dm3, r1
	nop	
	vmul.f	dm2, x5, x8, r1
	vadd.f	dm0, dm0, dm4, r1
	nop	
	vmul.f	dm1, x11, x5, r1
	vadd.f	dm0, dm0, dm2, r1
	nop	
	vmul.f	dm3, x3, x9, r1
	vadd.f	dm0, dm0, dm1, r1
	nop	
	vmul.f	dm4, x3, x5, r1
	vadd.f	dm0, dm0, dm3, r1
	nop	
	nop	
	vadd.f	dm0, dm0, dm4, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm0, r1
	vmov	bmll1, x6
	nop	
	nop	
	nop	
	nop	
.L_LEnd0:
	nopa	;		nopb	;		nops	;		add	r0, r0, #1;		vmov	x6, bmll1;		nopv	
// %bb.2:                               // %for.cond.cleanup3
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	vst	 bmll1, [p2, #0]                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end3:
	.size	_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_, .Lfunc_end3-_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_
                                        // -- End function
	.globl	CT_main                         // -- Begin function CT_main
	.p2align	4
	.type	CT_main,@function
CT_main:                                // @CT_main
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		add	r1, r1, #48;		nopm	
	add	r2, r2, #48
	add	r0, r0, #48
	movxm	r17, #16256
	movxm	r4, #3584
	movxm	r5, #2147483647
	mova	r16, #0;		movxm	r20, #65280
	mova	r6, #-1;		add	r3, r3, #48;		vbcst.32	 x0, r16
	mova	r18, #60;		movx	r7, #7;		vbcst.16	 x2, r17
	mova	m0, #8;		movx	r19, #1;		mov	r17, r16
	mova	r29, #6;		movx	r21, #2;		vbcst.64	 x4, r17:r16
	mova	r17, #112;		or	 r22, r16, r16;		vmov	x6, x0
	.p2align	4
.LBB4_1:                                // %for.body4
                                        // =>This Loop Header: Depth=1
                                        //     Child Loop BB4_2 Depth 2
                                        //       Child Loop BB4_3 Depth 3
	nopa	;		nopb	;		nops	;		acq	r1, r6;		nopm	;		nopv	
	nop	
	nop	
	nop	
	mova	r24, #0;		acq	r2, r6;		mov	r23, #0
	.p2align	4
.LBB4_2:                                // %for.cond11.preheader
                                        //   Parent Loop BB4_1 Depth=1
                                        // =>  This Loop Header: Depth=2
                                        //       Child Loop BB4_3 Depth 3
	nopa	;		nopb	;		nops	;		nopx	;		add.nc	lc, r7, #0;		nopv	
	movxm	ls, #.LBB4_3
	lda	 r25, [p0, #0];		movxm	le, #.L_LEnd1
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		lshl	 r26, r24, r21;		vmov	x8, x4;		nopv	
	nopa	;		nopb	;		movs	p3, p2;		nopx	;		mov	m1, r26;		nopv	
	mova	r25, #0;		paddb	 [p3], m1;		nops	;		nopx	;		vinsert.32	 x6, x6, r29, r25;		nopv	
	.p2align	4
.LBB4_3:                                // %_ZNK3aie6vectorIfLj16EE3getEj.exit.i
                                        //   Parent Loop BB4_1 Depth=1
                                        //     Parent Loop BB4_2 Depth=2
                                        // =>    This Inner Loop Header: Depth=3
	vlda	 bmll0, [p3], #64;		nopb	;		nops	;		nopxm	;		nopv	
	vextract.32	 r26, x6, r25, vaddsign1
	nop	
	vbcst.32	 x10, r26
	vmov	bmll2, x10
	nop	
	vconv.bf16.fp32	 wl3, bmll2
	vconv.bf16.fp32	 wl1, bmll0
	vsel.32	 x7, x3, x0, r20
	vsel.32	 x5, x1, x0, r20
	vmsc.f	dm1, dm1, x7, x2, r18
	vmov	bmll1, x10;		vmsc.f	dm2, dm0, x5, x2, r18
	nop	
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll1
	vconv.bf16.fp32	 wl9, bmll2
	vsel.32	 x11, x11, x0, r20
	vsel.32	 x9, x9, x0, r20
	vmsc.f	dm4, dm1, x11, x2, r18
	vmsc.f	dm3, dm2, x9, x2, r18
	nop	
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl1, bmll4
	vconv.bf16.fp32	 wl10, bmll3
	vsel.32	 x1, x1, x0, r20
	vsel.32	 x10, x10, x0, r20
	nop	
	vmul.f	dm0, x10, x1, r18
	vmul.f	dm2, x10, x11, r18
	nop	
	vmul.f	dm1, x9, x1, r18
	vadd.f	dm0, dm0, dm2, r18
	nop	
	vmul.f	dm3, x5, x1, r18
	vadd.f	dm0, dm0, dm1, r18
	nop	
	vmul.f	dm4, x9, x11, r18
	vadd.f	dm0, dm0, dm3, r18
	nop	
	vmul.f	dm2, x7, x10, r18
	vadd.f	dm0, dm0, dm4, r18
	nop	
	vmul.f	dm1, x9, x7, r18
	vadd.f	dm0, dm0, dm2, r18
	nop	
	vmul.f	dm3, x5, x11, r18
	vadd.f	dm0, dm0, dm1, r18
	nop	
	vmul.f	dm4, x5, x7, r18
	vadd.f	dm0, dm0, dm3, r18
	nop	
	nop	
	vadd.f	dm0, dm0, dm4, r18
	nop	
	nop	
	vadd.f	dm1, dm1, dm0, r18
	vmov	bmll1, x8
	nop	
	nop	
	nop	
	nop	
.L_LEnd1:
	nopa	;		nopb	;		nops	;		add	r25, r25, #1;		vmov	x8, bmll1;		nopv	
// %bb.4:                               // %_Z16mult_with_C1_DSWPfPN3aie6vectorIfLj16EEES_.exit
                                        //   in Loop: Header=BB4_2 Depth=2
	nopa	;		nopb	;		nops	;		add	 r24, r24, r17;		nopm	;		nopv	
	nopa	;		eq	 r26, r24, r4
	jz	 r26, #.LBB4_2
	nop	                                //  Delay Slot 5
	lshl	 r25, r23, r21                  //  Delay Slot 4
	mov	dj0, r25                        //  Delay Slot 3
	padda	 [p0], m0;		vst	 bmll1, [p1, dj0] //  Delay Slot 2
	add	r23, r23, #16                   //  Delay Slot 1
// %bb.5:                               // %for.cond.cleanup8
                                        //   in Loop: Header=BB4_1 Depth=1
	nopa	;		nopb	;		rel	r0, r19;		nopm	;		nops	
	nop	
	nop	
	nop	
	rel	r3, r19
	nop	
	nop	
	nop	
	acq	r1, r6
	nop	
	nop	
	nop	
	acq	r2, r6
	nop	
	nop	
	nop	
	rel	r0, r19
	add	r16, r16, #1
	ltu	 r23, r16, r19
	add	 r22, r22, r23
	xor	 r23, r16, r6
	xor	 r24, r22, r5
	or	 r23, r23, r24
	jnz	 r23, #.LBB4_1
	nop	                                //  Delay Slot 5
	rel	r3, r19                         //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
// %bb.6:                               // %for.cond.cleanup3
	nopa	;		ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end4:
	.size	CT_main, .Lfunc_end4-CT_main
                                        // -- End function
	.section	".linker-options","e",@llvm_linker_options
	.ident	"clang version 19.0.0 (https://github.com/Xilinx/llvm-aie b2a279c1939604e2ee82a651683dd995decc25ee)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
