	.text
	.file	"mvm_i8.cc"
	.globl	mv_int8                         // -- Begin function mv_int8
	.p2align	4
	.type	mv_int8,@function
mv_int8:                                // @mv_int8
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end0:
	.size	mv_int8, .Lfunc_end0-mv_int8
                                        // -- End function
	.section	.text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_,"axG",@progbits,_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_,comdat
	.weak	_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_ // -- Begin function _Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
	.p2align	4
	.type	_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_,@function
_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_: // @_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
	.p2align	4
// %bb.0:                               // %entry
	mova	r1, #8;		nopb	;		nops	;		movx	r0, #0;		nopm	;		nopv	
	mova	r4, #1;		nopb	;		movx	r3, #3;		mov	r2, #2;		nops	
	mova	r5, #808;		paddxm	 [sp], #128
	mova	r16, #-16;		st	 r8, [sp, #-124];		movx	r7, #112;		mov	r6, #64 // 4-byte Folded Spill
	mova	r17, #0;		st	 r9, [sp, #-128];		event	#0;		mov	m0, #512 // 4-byte Folded Spill
	.p2align	4
.LBB1_1:                                // %for.body
                                        // =>This Loop Header: Depth=1
                                        //     Child Loop BB1_2 Depth 2
	add.nc	lc, r1, #0
	movxm	ls, #.LBB1_2
	movxm	le, #.L_LEnd0
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
	vlda	 bmll0, [p2, #0];		nopb	;		movs	m1, r17;		nopx	;		mov	p3, p0;		nopv	
	padda	 [p3], m1;		nopb	;		nops	;		nopx	;		mov	p4, p1;		nopv	
	.p2align	4
.LBB1_2:                                // %for.body4
                                        //   Parent Loop BB1_1 Depth=1
                                        // =>  This Inner Loop Header: Depth=2
	nopa	;		vldb	 x0, [p3], m0;		nopx	
	nop	
	vldb.128	 wl7, [p4], #16
	nop	
	nop	
	nop	
	nop	
	vshuffle	x3, x0, x0, r2
	vshuffle	x1, x0, x0, r3
	vextract.8	 r18, x7, #0, vaddsign1
	vextract.8	 r19, x7, #1, vaddsign1
	vextract.8	 r20, x7, #2, vaddsign1
	vextract.8	 r21, x7, #3, vaddsign1
	vextract.8	 r22, x7, #4, vaddsign1
	vextract.8	 r23, x7, #5, vaddsign1
	vextract.8	 r24, x7, #6, vaddsign1
	vextract.8	 r25, x7, #7, vaddsign1
	vextract.8	 r26, x7, #8, vaddsign1
	vextract.8	 r27, x7, #9, vaddsign1
	vextract.8	 r28, x7, #10, vaddsign1
	vextract.8	 r29, x7, #11, vaddsign1
	vextract.8	 r30, x7, #12, vaddsign1
	vextract.8	 r31, x7, #13, vaddsign1
	vextract.8	 r8, x7, #14, vaddsign1
	vldb	 x0, [p3], m0;		vextract.8	 r9, x7, #15, vaddsign1
	vshuffle	x2, x3, x3, r0
	vshuffle	x3, x3, x3, r4
	vbcst.8	 x4, r18
	vldb	 x0, [p3], m0;		vbcst.8	 x5, r19
	vbcst.8	 x2, r20
	vldb	 x0, [p3], m0;		vbcst.8	 x3, r21;		vmac	dm0, dm0, y1, y2,r5
	vshuffle	x10, x0, x0, r2
	vshuffle	x8, x0, x0, r3
	vshuffle	x4, x10, x10, r0
	vshuffle	x5, x10, x10, r4
	vshuffle	x6, x0, x0, r2
	vshuffle	x11, x0, x0, r3
	vshuffle	x9, x0, x0, r2
	vshuffle	x0, x0, x0, r3
	vshuffle	x0, x1, x1, r0
	vst	 x0, [sp, #-64];		vshuffle	x1, x1, x1, r4 // 64-byte Folded Spill
	vbcst.8	 x0, r22
	vbcst.8	 x1, r23;		vmac	dm1, dm0, y0, y1,r5
	vshuffle	x2, x8, x8, r0
	vshuffle	x3, x8, x8, r4
	vshuffle	x4, x6, x6, r0
	vshuffle	x5, x6, x6, r4;		vmac	dm2, dm1, y2, y0,r5
	vbcst.8	 x0, r24
	vbcst.8	 x1, r25
	vbcst.8	 x0, r26
	vbcst.8	 x1, r27;		vmac	dm3, dm2, y1, y0,r5
	vshuffle	x2, x11, x11, r0
	vlda	 x6, [sp, #-64];		vshuffle	x3, x11, x11, r4 // 64-byte Folded Reload
	vbcst.8	 x0, r28
	vbcst.8	 x1, r29;		vmac	dm4, dm3, y2, y0,r5
	vshuffle	x4, x9, x9, r0
	vshuffle	x5, x9, x9, r4
	vbcst.8	 x0, r30
	vbcst.8	 x1, r31;		vmac	dm4, dm4, y1, y0,r5
	vshuffle	x2, x6, x6, r0
	vshuffle	x3, x6, x6, r4
	vbcst.8	 x0, r8
	vbcst.8	 x1, r9;		vmac	dm4, dm4, y2, y0,r5
	nop	
.L_LEnd0:
	nopa	;		nopb	;		nops	;		nopxm	;		vmac	dm0, dm4, y1, y0,r5
// %bb.3:                               // %for.cond.cleanup3
                                        //   in Loop: Header=BB1_1 Depth=1
	nopa	;		nopb	;		add	r16, r16, #16
	ltu	 r18, r16, r7
	jnz	 r18, #.LBB1_1
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	vst	 bmll0, [p2], #64               //  Delay Slot 2
	add	 r17, r17, r6                   //  Delay Slot 1
// %bb.4:                               // %for.cond.cleanup
	lda	 r9, [sp, #-128];		event	#1;		nopm	 // 4-byte Folded Reload
	lda	 r8, [sp, #-124]                // 4-byte Folded Reload
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	paddxm	 [sp], #-128                    //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end1:
	.size	_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_, .Lfunc_end1-_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
                                        // -- End function
	.text
	.globl	zero_m_int8                     // -- Begin function zero_m_int8
	.p2align	4
	.type	zero_m_int8,@function
zero_m_int8:                            // @zero_m_int8
	.p2align	4
// %bb.0:                               // %entry
	mova	r0, #0;		nopx	
	vbcst.32	 x0, r0
	nop	
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32
	vst	 wl0, [p0], #32;		ret	lr
	vst	 wl0, [p0], #32                 //  Delay Slot 5
	vst	 wl0, [p0], #32                 //  Delay Slot 4
	vst	 wl0, [p0], #32                 //  Delay Slot 3
	vst	 wl0, [p0, #0]                  //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end2:
	.size	zero_m_int8, .Lfunc_end2-zero_m_int8
                                        // -- End function
	.section	".linker-options","e",@llvm_linker_options
	.ident	"clang version 19.0.0 (https://github.com/Xilinx/llvm-aie b2a279c1939604e2ee82a651683dd995decc25ee)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym __gxx_personality_v0
