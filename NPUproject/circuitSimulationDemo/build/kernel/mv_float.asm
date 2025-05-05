	.text
	.file	"mv_float.cc"
	.globl	test_float_operation            // -- Begin function test_float_operation
	.p2align	4
	.type	test_float_operation,@function
test_float_operation:                   // @test_float_operation
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		nopb	;		jl	#__addsf3
	nop	                                //  Delay Slot 5
	paddxm	 [sp], #64                      //  Delay Slot 4
	st	 lr, [sp, #-60]                 // 4-byte Folded Spill Delay Slot 3
	st	 r8, [sp, #-64]                 // 4-byte Folded Spill Delay Slot 2
	mov	r8, r3                          //  Delay Slot 1
	nopa	;		nopb	;		nops	;		jl	#__addsf3;		nopv	
	nopx	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	or	 r1, r0, r0;		mov	r2, r8  //  Delay Slot 1
	nopa	;		nopb	;		nops	;		jl	#__extendsfdf2;		nopv	
	nopa	;		nopx	                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r2, r0                          //  Delay Slot 1
	nopa	;		jl	#__adddf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	movxm	r4, #1374389535                 //  Delay Slot 3
	movxm	r5, #1079578296                 //  Delay Slot 2
	or	 r2, r0, r0;		mov	r3, r1  //  Delay Slot 1
	nopa	;		nopb	;		nops	;		jl	#__truncdfsf2;		nopv	
	nopx	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	or	 r2, r1, r1;		mov	r1, r0  //  Delay Slot 1
	lda	 lr, [sp, #-60];		nopb	;		nops	;		nopxm	;		nopv	 // 4-byte Folded Reload
	nop	
	nop	
	nop	
	nop	
	nop	
	lda	 r8, [sp, #-64]                 // 4-byte Folded Reload
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	paddxm	 [sp], #-64                     //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end0:
	.size	test_float_operation, .Lfunc_end0-test_float_operation
                                        // -- End function
	.globl	mv_float32                      // -- Begin function mv_float32
	.p2align	4
	.type	mv_float32,@function
mv_float32:                             // @mv_float32
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end1:
	.size	mv_float32, .Lfunc_end1-mv_float32
                                        // -- End function
	.section	.text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_,"axG",@progbits,_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_,comdat
	.weak	_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_ // -- Begin function _Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
	.p2align	4
	.type	_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_,@function
_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_: // @_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
	.p2align	4
// %bb.0:                               // %entry
	nopa	;		nopb	;		event	#0;		nopm	
	movxm	r1, #16256
	mova	r0, #0;		movxm	r16, #65280
	mova	r3, #-16;		movx	r2, #48;		vbcst.32	 x0, r0
	mova	r1, #60;		movx	r0, #4;		vbcst.16	 x2, r1
	.p2align	4
.LBB2_1:                                // %for.body
                                        // =>This Loop Header: Depth=1
                                        //     Child Loop BB2_2 Depth 2
	add.nc	lc, r0, #0
	movxm	ls, #.LBB2_2
	movxm	le, #.L_LEnd0
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	vlda	 bmll0, [p2, #0];		nopb	;		nops	;		nopx	;		mov	p3, p1;		nopv	
	.p2align	4
.LBB2_2:                                // %for.body4
                                        //   Parent Loop BB2_1 Depth=1
                                        // =>  This Inner Loop Header: Depth=2
	vldb	 x4, [p3], #64;		nopx	
	nop	
	nop	
	nop	
	vlda	 bmll1, [p0], #64
	nop	
	nop	
	vextract.64	 r5:r4, x4, #0, vaddsign1
	nop	
	vbcst.32	 x6, r4
	vmov	bmll3, x6
	vconv.bf16.fp32	 wl8, bmll1
	vconv.bf16.fp32	 wl10, bmll3
	vsel.32	 x1, x8, x0, r16
	vsel.32	 x3, x10, x0, r16
	vmsc.f	dm1, dm1, x1, x2, r1
	vmsc.f	dm2, dm2, x3, x2, r1
	vmov	bmll2, x6
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl5, bmll1
	vconv.bf16.fp32	 wl7, bmll2
	vsel.32	 x9, x5, x0, r16
	vsel.32	 x11, x7, x0, r16
	vmsc.f	dm1, dm1, x9, x2, r1
	vmsc.f	dm2, dm2, x11, x2, r1
	nop	
	nop	
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll1
	vconv.bf16.fp32	 wl8, bmll2
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x8, x8, x0, r16
	vmul.f	dm2, x6, x11, r1
	vmul.f	dm1, x6, x8, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x9, x8, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x5, r5
	vmov	bmll4, x5
	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
	vconv.bf16.fp32	 wl7, bmll4
	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x10, x2, r1
	vmsc.f	dm1, dm3, x7, x2, r1
	vmov	bmll3, x5
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
	vconv.bf16.fp32	 wl9, bmll1
	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x6, x2, r1
	vmsc.f	dm1, dm1, x9, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x1, x11, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
	vsel.32	 x11, x11, x0, r16
	vsel.32	 x1, x1, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x11, x1, r1
	vmul.f	dm2, x11, x9, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x6, x1, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #1, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x8, r4
	vmov	bmll4, x8
	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x10, x1, r1
	vconv.bf16.fp32	 wl5, bmll4
	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x6, x9, r1
	vsel.32	 x5, x5, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x3, x2, r1
	vmsc.f	dm1, dm3, x5, x2, r1
	vmov	bmll3, x8
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x7, x11, r1
	vconv.bf16.fp32	 wl6, bmll1
	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x7, r1
	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x11, x2, r1
	vmsc.f	dm1, dm1, x6, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x10, x9, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
	vsel.32	 x9, x9, x0, r16
	vsel.32	 x10, x10, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x9, x10, r1
	vmul.f	dm2, x9, x6, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x11, x10, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x1, r5
	vmov	bmll4, x1
	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x3, x10, r1
	vconv.bf16.fp32	 wl8, bmll4
	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x11, x6, r1
	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x7, x2, r1
	vmsc.f	dm1, dm3, x8, x2, r1
	vmov	bmll3, x1
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x5, x9, r1
	vconv.bf16.fp32	 wl11, bmll1
	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x5, r1
	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x9, x2, r1
	vmsc.f	dm1, dm1, x11, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x3, x6, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl3, bmll1;		vmul.f	dm2, x3, x5, r1
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x3, x3, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x6, x3, r1
	vmul.f	dm2, x6, x11, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x9, x3, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #2, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x10, r4
	vmov	bmll4, x10
	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x3, r1
	vconv.bf16.fp32	 wl1, bmll4
	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x9, x11, r1
	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x5, x2, r1
	vmsc.f	dm1, dm3, x1, x2, r1
	vmov	bmll3, x10
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x8, x6, r1
	vconv.bf16.fp32	 wl9, bmll1
	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x8, r1
	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x6, x2, r1
	vmsc.f	dm1, dm1, x9, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x7, x11, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl7, bmll1;		vmul.f	dm2, x7, x8, r1
	vsel.32	 x11, x11, x0, r16
	vsel.32	 x7, x7, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x11, x7, r1
	vmul.f	dm2, x11, x9, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x6, x7, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x3, r5
	vmov	bmll4, x3
	vconv.bf16.fp32	 wl8, bmll2;		vmul.f	dm3, x5, x7, r1
	vconv.bf16.fp32	 wl10, bmll4
	vsel.32	 x8, x8, x0, r16;		vmul.f	dm4, x6, x9, r1
	vsel.32	 x10, x10, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x8, x2, r1
	vmsc.f	dm1, dm3, x10, x2, r1
	vmov	bmll3, x3
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x1, x11, r1
	vconv.bf16.fp32	 wl6, bmll1
	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x1, r1
	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x11, x2, r1
	vmsc.f	dm1, dm1, x6, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x5, x9, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl5, bmll1;		vmul.f	dm2, x5, x1, r1
	vsel.32	 x9, x9, x0, r16
	vsel.32	 x5, x5, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x9, x5, r1
	vmul.f	dm2, x9, x6, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x11, x5, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #3, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x7, r4
	vmov	bmll4, x7
	vconv.bf16.fp32	 wl1, bmll2;		vmul.f	dm3, x8, x5, r1
	vconv.bf16.fp32	 wl3, bmll4
	vsel.32	 x1, x1, x0, r16;		vmul.f	dm4, x11, x6, r1
	vsel.32	 x3, x3, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x1, x2, r1
	vmsc.f	dm1, dm3, x3, x2, r1
	vmov	bmll3, x7
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x10, x9, r1
	vconv.bf16.fp32	 wl11, bmll1
	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x10, r1
	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x9, x2, r1
	vmsc.f	dm1, dm1, x11, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x8, x6, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl8, bmll1;		vmul.f	dm2, x8, x10, r1
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x8, x8, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x6, x8, r1
	vmul.f	dm2, x6, x11, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x9, x8, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x5, r5
	vmov	bmll4, x5
	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
	vconv.bf16.fp32	 wl7, bmll4
	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x10, x2, r1
	vmsc.f	dm1, dm3, x7, x2, r1
	vmov	bmll3, x5
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
	vconv.bf16.fp32	 wl9, bmll1
	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x6, x2, r1
	vmsc.f	dm1, dm1, x9, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x1, x11, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
	vsel.32	 x11, x11, x0, r16
	vsel.32	 x1, x1, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x11, x1, r1
	vmul.f	dm2, x11, x9, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x6, x1, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #4, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x8, r4
	vmov	bmll4, x8
	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x10, x1, r1
	vconv.bf16.fp32	 wl5, bmll4
	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x6, x9, r1
	vsel.32	 x5, x5, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x3, x2, r1
	vmsc.f	dm1, dm3, x5, x2, r1
	vmov	bmll3, x8
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x7, x11, r1
	vconv.bf16.fp32	 wl6, bmll1
	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x7, r1
	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x11, x2, r1
	vmsc.f	dm1, dm1, x6, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x10, x9, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
	vsel.32	 x9, x9, x0, r16
	vsel.32	 x10, x10, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x9, x10, r1
	vmul.f	dm2, x9, x6, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x11, x10, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x1, r5
	vmov	bmll4, x1
	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x3, x10, r1
	vconv.bf16.fp32	 wl8, bmll4
	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x11, x6, r1
	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x7, x2, r1
	vmsc.f	dm1, dm3, x8, x2, r1
	vmov	bmll3, x1
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x5, x9, r1
	vconv.bf16.fp32	 wl11, bmll1
	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x5, r1
	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x9, x2, r1
	vmsc.f	dm1, dm1, x11, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x3, x6, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl3, bmll1;		vmul.f	dm2, x3, x5, r1
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x3, x3, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x6, x3, r1
	vmul.f	dm2, x6, x11, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x9, x3, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #5, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x10, r4
	vmov	bmll4, x10
	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x3, r1
	vconv.bf16.fp32	 wl1, bmll4
	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x9, x11, r1
	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x5, x2, r1
	vmsc.f	dm1, dm3, x1, x2, r1
	vmov	bmll3, x10
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x8, x6, r1
	vconv.bf16.fp32	 wl9, bmll1
	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x8, r1
	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x6, x2, r1
	vmsc.f	dm1, dm1, x9, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x7, x11, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl7, bmll1;		vmul.f	dm2, x7, x8, r1
	vsel.32	 x11, x11, x0, r16
	vsel.32	 x7, x7, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x11, x7, r1
	vmul.f	dm2, x11, x9, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x6, x7, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x3, r5
	vmov	bmll4, x3
	vconv.bf16.fp32	 wl8, bmll2;		vmul.f	dm3, x5, x7, r1
	vconv.bf16.fp32	 wl10, bmll4
	vsel.32	 x8, x8, x0, r16;		vmul.f	dm4, x6, x9, r1
	vsel.32	 x10, x10, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x8, x2, r1
	vmsc.f	dm1, dm3, x10, x2, r1
	vmov	bmll3, x3
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x1, x11, r1
	vconv.bf16.fp32	 wl6, bmll1
	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x1, r1
	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x11, x2, r1
	vmsc.f	dm1, dm1, x6, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x5, x9, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl5, bmll1;		vmul.f	dm2, x5, x1, r1
	vsel.32	 x9, x9, x0, r16
	vsel.32	 x5, x5, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x9, x5, r1
	vmul.f	dm2, x9, x6, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x11, x5, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #6, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x7, r4
	vmov	bmll4, x7
	vconv.bf16.fp32	 wl1, bmll2;		vmul.f	dm3, x8, x5, r1
	vconv.bf16.fp32	 wl3, bmll4
	vsel.32	 x1, x1, x0, r16;		vmul.f	dm4, x11, x6, r1
	vsel.32	 x3, x3, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x1, x2, r1
	vmsc.f	dm1, dm3, x3, x2, r1
	vmov	bmll3, x7
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x10, x9, r1
	vconv.bf16.fp32	 wl11, bmll1
	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x10, r1
	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x9, x2, r1
	vmsc.f	dm1, dm1, x11, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x8, x6, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl8, bmll1;		vmul.f	dm2, x8, x10, r1
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x8, x8, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x6, x8, r1
	vmul.f	dm2, x6, x11, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x9, x8, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x5, r5
	vmov	bmll4, x5
	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
	vconv.bf16.fp32	 wl7, bmll4
	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x10, x2, r1
	vmsc.f	dm1, dm3, x7, x2, r1
	vmov	bmll3, x5
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
	vconv.bf16.fp32	 wl9, bmll1
	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x6, x2, r1
	vmsc.f	dm1, dm1, x9, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x1, x11, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
	vsel.32	 x11, x11, x0, r16
	vsel.32	 x1, x1, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x11, x1, r1
	vmul.f	dm2, x11, x9, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x6, x1, r1
	nop	
	nop	
	vextract.64	 r5:r4, x4, #7, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x3, r4
	vmov	bmll4, x3
	vconv.bf16.fp32	 wl4, bmll2;		vmul.f	dm3, x10, x1, r1
	vconv.bf16.fp32	 wl8, bmll4
	vsel.32	 x4, x4, x0, r16;		vmul.f	dm4, x6, x9, r1
	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x4, x2, r1
	vmsc.f	dm1, dm3, x8, x2, r1
	vmov	bmll3, x3
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x11, r1
	vconv.bf16.fp32	 wl6, bmll1
	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x6, x7, r1
	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x5, x2, r1
	vmsc.f	dm1, dm1, x6, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x10, x9, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
	vsel.32	 x9, x9, x0, r16
	vsel.32	 x10, x10, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x9, x10, r1
	vmul.f	dm2, x9, x6, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vlda	 bmll2, [p0], #64;		vmul.f	dm2, x5, x10, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	vbcst.32	 x11, r5
	vmov	bmll4, x11
	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x4, x10, r1
	vconv.bf16.fp32	 wl1, bmll4
	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x5, x6, r1
	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
	vmsc.f	dm2, dm2, x7, x2, r1
	vmsc.f	dm1, dm3, x1, x2, r1
	vmov	bmll3, x11
	vadd.f	dm4, dm1, dm4, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x8, x9, r1
	vconv.bf16.fp32	 wl5, bmll1
	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x5, x8, r1
	vsel.32	 x5, x5, x0, r16;		vadd.f	dm3, dm4, dm3, r1
	vmsc.f	dm2, dm2, x3, x2, r1
	vmsc.f	dm1, dm1, x5, x2, r1
	vadd.f	dm3, dm3, dm4, r1
	vmul.f	dm4, x4, x6, r1
	nop	
	nop	
	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
	vconv.bf16.fp32	 wl4, bmll1;		vmul.f	dm2, x4, x8, r1
	vsel.32	 x6, x6, x0, r16
	vsel.32	 x4, x4, x0, r16
	vadd.f	dm2, dm3, dm2, r1
	vmul.f	dm1, x6, x4, r1
	vmul.f	dm2, x6, x5, r1
	nop	
	vadd.f	dm0, dm0, dm2, r1
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x3, x4, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x7, x4, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x3, x5, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x1, x6, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x3, x1, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x7, x5, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	vmul.f	dm2, x7, x1, r1
	nop	
	nop	
	vadd.f	dm1, dm1, dm2, r1
	nop	
	nop	
.L_LEnd0:
	nopa	;		nopb	;		nops	;		nopxm	;		vadd.f	dm0, dm0, dm1, r1
// %bb.3:                               // %for.cond.cleanup3
                                        //   in Loop: Header=BB2_1 Depth=1
	nopa	;		add	r3, r3, #16;		nopm	
	ltu	 r4, r3, r2
	jnz	 r4, #.LBB2_1
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	vst	 bmll0, [p2], #64               //  Delay Slot 2
	nop	                                //  Delay Slot 1
// %bb.4:                               // %for.cond.cleanup
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	event	#1                              //  Delay Slot 1
.Lfunc_end2:
	.size	_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_, .Lfunc_end2-_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
                                        // -- End function
	.text
	.globl	zero_m_float32                  // -- Begin function zero_m_float32
	.p2align	4
	.type	zero_m_float32,@function
zero_m_float32:                         // @zero_m_float32
	.p2align	4
// %bb.0:                               // %entry
	mova	r0, #0;		nopx	
	vbcst.32	 x0, r0
	nop	
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32;		ret	lr
	vst	 wl0, [p0], #32                 //  Delay Slot 5
	vst	 wl0, [p0], #32                 //  Delay Slot 4
	vst	 wl0, [p0], #32                 //  Delay Slot 3
	vst	 wl0, [p0, #0]                  //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end3:
	.size	zero_m_float32, .Lfunc_end3-zero_m_float32
                                        // -- End function
	.section	".linker-options","e",@llvm_linker_options
	.ident	"clang version 19.0.0 (https://github.com/Xilinx/llvm-aie b2a279c1939604e2ee82a651683dd995decc25ee)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
