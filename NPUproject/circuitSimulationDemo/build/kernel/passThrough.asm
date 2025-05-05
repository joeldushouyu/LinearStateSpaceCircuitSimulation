	.text
	.file	"passThrough.cc"
	.globl	passThroughLine_float_0         // -- Begin function passThroughLine_float_0
	.p2align	4
	.type	passThroughLine_float_0,@function
passThroughLine_float_0:                // @passThroughLine_float_0
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z18passThrough_simpleIfEvPfS0_i
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end0:
	.size	passThroughLine_float_0, .Lfunc_end0-passThroughLine_float_0
                                        // -- End function
	.section	.text._Z18passThrough_simpleIfEvPfS0_i,"axG",@progbits,_Z18passThrough_simpleIfEvPfS0_i,comdat
	.weak	_Z18passThrough_simpleIfEvPfS0_i // -- Begin function _Z18passThrough_simpleIfEvPfS0_i
	.p2align	4
	.type	_Z18passThrough_simpleIfEvPfS0_i,@function
_Z18passThrough_simpleIfEvPfS0_i:       // @_Z18passThrough_simpleIfEvPfS0_i
	.p2align	4
// %bb.0:                               // %entry
	mova	r1, #0
	ge	 r1, r1, r0
	jnz	 r1, #.LBB1_2
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	paddxm	 [sp], #64                      //  Delay Slot 3
	st	 lr, [sp, #-64]                 // 4-byte Folded Spill Delay Slot 2
	event	#0                              //  Delay Slot 1
// %bb.1:                               // %for.body.preheader
	nopa	;		jl	#memcpy
	nop	                                //  Delay Slot 5
	mova	r1, #2                          //  Delay Slot 4
	lshl	 r0, r0, r1                     //  Delay Slot 3
	movxm	r1, #1048575                    //  Delay Slot 2
	and	 r0, r0, r1;		mov	p2, p0  //  Delay Slot 1
	.p2align	4
.LBB1_2:                                // %for.cond.cleanup
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
	.size	_Z18passThrough_simpleIfEvPfS0_i, .Lfunc_end1-_Z18passThrough_simpleIfEvPfS0_i
                                        // -- End function
	.text
	.globl	passThroughLine_float_1         // -- Begin function passThroughLine_float_1
	.p2align	4
	.type	passThroughLine_float_1,@function
passThroughLine_float_1:                // @passThroughLine_float_1
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z18passThrough_simpleIfEvPfS0_i
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end2:
	.size	passThroughLine_float_1, .Lfunc_end2-passThroughLine_float_1
                                        // -- End function
	.globl	passThroughLine_float_2         // -- Begin function passThroughLine_float_2
	.p2align	4
	.type	passThroughLine_float_2,@function
passThroughLine_float_2:                // @passThroughLine_float_2
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z18passThrough_simpleIfEvPfS0_i
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end3:
	.size	passThroughLine_float_2, .Lfunc_end3-passThroughLine_float_2
                                        // -- End function
	.globl	passThroughLine_float_3         // -- Begin function passThroughLine_float_3
	.p2align	4
	.type	passThroughLine_float_3,@function
passThroughLine_float_3:                // @passThroughLine_float_3
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z18passThrough_simpleIfEvPfS0_i
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end4:
	.size	passThroughLine_float_3, .Lfunc_end4-passThroughLine_float_3
                                        // -- End function
	.globl	accum_float_value               // -- Begin function accum_float_value
	.p2align	4
	.type	accum_float_value,@function
accum_float_value:                      // @accum_float_value
	.p2align	4
// %bb.0:                               // %entry
	j	#_Z10accumValueIfEvPfS0_iiiii
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end5:
	.size	accum_float_value, .Lfunc_end5-accum_float_value
                                        // -- End function
	.section	.text._Z10accumValueIfEvPfS0_iiiii,"axG",@progbits,_Z10accumValueIfEvPfS0_iiiii,comdat
	.weak	_Z10accumValueIfEvPfS0_iiiii    // -- Begin function _Z10accumValueIfEvPfS0_iiiii
	.p2align	4
	.type	_Z10accumValueIfEvPfS0_iiiii,@function
_Z10accumValueIfEvPfS0_iiiii:           // @_Z10accumValueIfEvPfS0_iiiii
	.p2align	4
// %bb.0:                               // %entry
	paddxm	 [sp], #64
	st	 p6, [sp, #-60];		nopx	        // 4-byte Folded Spill
	st	 p7, [sp, #-64]                 // 4-byte Folded Spill
	st	 r11, [sp, #-44]                // 4-byte Folded Spill
	st	 r12, [sp, #-48]                // 4-byte Folded Spill
	st	 r8, [sp, #-32]                 // 4-byte Folded Spill
	st	 r10, [sp, #-40];		jl	#__divsi3 // 4-byte Folded Spill
	st	 r13, [sp, #-52]                // 4-byte Folded Spill Delay Slot 5
	st	 r9, [sp, #-36];		mov	p6, p0  // 4-byte Folded Spill Delay Slot 4
	st	 lr, [sp, #-28];		mov	r11, r0 // 4-byte Folded Spill Delay Slot 3
	st	 r14, [sp, #-56];		or	 r12, r1, r1;		mov	r8, r2 // 4-byte Folded Spill Delay Slot 2
	mova	r13, #0;		movs	p7, p1;		or	 r1, r3, r3;		mov	r10, r4 //  Delay Slot 1
	nopa	;		nopb	;		nops	;		jl	#__divsi3;		nopv	
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	mov	r9, r0                          //  Delay Slot 2
	or	 r1, r10, r10;		mov	r2, r8  //  Delay Slot 1
	nopa	;		nopb	;		ge	 r1, r13, r8;		nopm	;		nops	
	jnz	 r1, #.LBB6_9
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	event	#0                              //  Delay Slot 1
// %bb.1:                               // %for.cond4.preheader.lr.ph
	nopa	;		nopb	;		nops	;		j	#.LBB6_3;		nopv	
	mova	r0, #2;		nopx	;		mov	r10, r0 //  Delay Slot 5
	lshl	 r1, r12, r0                    //  Delay Slot 4
	lshl	 r2, r11, r0;		mov	m0, r1  //  Delay Slot 3
	padda	 [p7], m0;		mov	m0, r2  //  Delay Slot 2
	padda	 [p6], m0;		lshl	 r14, r9, r0 //  Delay Slot 1
	.p2align	4
.LBB6_2:                                // %for.cond.cleanup13
                                        //   in Loop: Header=BB6_3 Depth=1
	nopa	;		nopb	;		nops	;		add	r8, r8, #-1;		nopm	;		nopv	
	jz	 r8, #.LBB6_9
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
	.p2align	4
.LBB6_3:                                // %for.cond4.preheader
                                        // =>This Loop Header: Depth=1
                                        //     Child Loop BB6_4 Depth 2
                                        //     Child Loop BB6_8 Depth 2
	nopa	;		nopb	;		ge	 r1, r13, r9
	jnz	 r1, #.LBB6_6
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mova	r0, #0;		or	 r11, r9, r9;		mov	r12, p6 //  Delay Slot 1
	.p2align	4
.LBB6_4:                                // %for.body7
                                        //   Parent Loop BB6_3 Depth=1
                                        // =>  This Inner Loop Header: Depth=2
	lda	 r2, [p6], #4;		nopb	;		nopxm	;		nops	
	jl	#__addsf3
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r1, r0                          //  Delay Slot 1
	nopa	;		nopb	;		nops	;		add	r11, r11, #-1;		nopm	;		nopv	
	jnz	 r11, #.LBB6_4
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
// %bb.5:                               // %for.cond11.preheader.loopexit
                                        //   in Loop: Header=BB6_3 Depth=1
	nopa	;		nopb	;		j	#.LBB6_7;		nops	
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	movs	p6, r12;		mov	m0, r14         //  Delay Slot 2
	padda	 [p6], m0                       //  Delay Slot 1
	.p2align	4
.LBB6_6:                                //   in Loop: Header=BB6_3 Depth=1
	nopa	;		nopb	;		nops	;		nopx	;		mov	p6, r12;		nopv	
	.p2align	4
.LBB6_7:                                // %for.cond11.preheader
                                        //   in Loop: Header=BB6_3 Depth=1
	nopa	;		nopb	;		ge	 r2, r13, r10;		nopm	;		nops	
	jnz	 r2, #.LBB6_2
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	mov	r1, r10                         //  Delay Slot 1
	.p2align	4
.LBB6_8:                                // %for.body14
                                        //   Parent Loop BB6_3 Depth=1
                                        // =>  This Inner Loop Header: Depth=2
	nopa	;		nopb	;		add	r1, r1, #-1;		nopm	;		nops	
	jnz	 r1, #.LBB6_8
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	st	 r0, [p7], #4                   //  Delay Slot 2
	nop	                                //  Delay Slot 1
	j	#.LBB6_2
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	nop	                                //  Delay Slot 2
	nop	                                //  Delay Slot 1
	.p2align	4
.LBB6_9:                                // %for.cond.cleanup
	lda	 p7, [sp, #-64];		event	#1;		nopm	 // 4-byte Folded Reload
	lda	 p6, [sp, #-60]                 // 4-byte Folded Reload
	lda	 r14, [sp, #-56]                // 4-byte Folded Reload
	lda	 lr, [sp, #-28]                 // 4-byte Folded Reload
	lda	 r13, [sp, #-52]                // 4-byte Folded Reload
	lda	 r12, [sp, #-48]                // 4-byte Folded Reload
	lda	 r11, [sp, #-44]                // 4-byte Folded Reload
	lda	 r10, [sp, #-40]                // 4-byte Folded Reload
	lda	 r9, [sp, #-36]                 // 4-byte Folded Reload
	lda	 r8, [sp, #-32]                 // 4-byte Folded Reload
	ret	lr
	nop	                                //  Delay Slot 5
	nop	                                //  Delay Slot 4
	nop	                                //  Delay Slot 3
	paddxm	 [sp], #-64                     //  Delay Slot 2
	nop	                                //  Delay Slot 1
.Lfunc_end6:
	.size	_Z10accumValueIfEvPfS0_iiiii, .Lfunc_end6-_Z10accumValueIfEvPfS0_iiiii
                                        // -- End function
	.section	".linker-options","e",@llvm_linker_options
	.ident	"clang version 19.0.0 (https://github.com/Xilinx/llvm-aie b2a279c1939604e2ee82a651683dd995decc25ee)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
