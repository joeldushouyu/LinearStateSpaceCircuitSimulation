
build/kernel/mvm_i8.o:	file format elf32-aie
architecture: aie2p
start address: 0x00000000

Program Header:

Dynamic Section:

Sections:
Idx Name                                                                           Size     VMA      Type
  0                                                                                00000000 00000000 
  1 .strtab                                                                        000000e0 00000000 
  2 .text                                                                          00000060 00000000 TEXT
  3 .rela.text                                                                     0000000c 00000000 
  4 .group                                                                         0000000c 00000000 
  5 .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_      00000230 00000000 TEXT
  6 .rela.text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_ 00000024 00000000 
  7 .linker-options                                                                00000000 00000000 
  8 .comment                                                                       00000064 00000000 
  9 .note.GNU-stack                                                                00000000 00000000 
 10 .llvm_addrsig                                                                  00000000 00000000 
 11 .symtab                                                                        00000080 00000000 

SYMBOL TABLE:
00000000 l    df *ABS*	00000000 mvm_i8.cc
00000040 l       .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_	00000000 .LBB1_1
000000c0 l       .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_	00000000 .LBB1_2
000001e0 l       .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_	00000000 .L_LEnd0
00000000 g     F .text	00000010 mv_int8
00000000  w    F .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_	00000230 _Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
00000010 g     F .text	00000050 zero_m_int8

DYNAMIC SYMBOL TABLE:
Contents of section .strtab:
 0000 002e7265 6c612e74 65787400 2e636f6d  ..rela.text..com
 0010 6d656e74 002e6c69 6e6b6572 2d6f7074  ment..linker-opt
 0020 696f6e73 002e6772 6f757000 2e6e6f74  ions..group..not
 0030 652e474e 552d7374 61636b00 2e6c6c76  e.GNU-stack..llv
 0040 6d5f6164 64727369 67006d76 6d5f6938  m_addrsig.mvm_i8
 0050 2e636300 2e737472 74616200 2e73796d  .cc..strtab..sym
 0060 74616200 2e72656c 612e7465 78742e5f  tab..rela.text._
 0070 5a32326d 61747665 635f7665 63746f72  Z22matvec_vector
 0080 697a6564 5f696e74 38496169 75375f5f  ized_int8Iaiu7__
 0090 61636333 324c6a31 3238454c 6a313238  acc32Lj128ELj128
 00a0 454c6a31 36454576 50545f53 315f5054  ELj16EEvPT_S1_PT
 00b0 305f006d 765f696e 7438007a 65726f5f  0_.mv_int8.zero_
 00c0 6d5f696e 7438002e 4c424231 5f32002e  m_int8..LBB1_2..
 00d0 4c424231 5f31002e 4c5f4c45 6e643000  LBB1_1..L_LEnd0.
Contents of section .text:
 0000 84000000 00000000 00000000 00000000  ................
 0010 2c000000 0000f872 02180000 982a1c08  ,......r.....*..
 0020 982a1c08 982a1c08 982a1c08 982a1c08  .*...*...*...*..
 0030 982a1c08 982a1c08 982a1c08 982a1c08  .*...*...*...*..
 0040 982a1c08 982a1c08 5c005050 8503982a  .*...*..\.PP...*
 0050 1c08982a 1c08982a 1c08982a 04080000  ...*...*...*....
Contents of section .rela.text:
 0000 00000000 01060000 00000000           ............
Contents of section .group:
 0000 01000000 05000000 06000000           ............
Contents of section .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_:
 0000 e1000078 a5010800 005b0120 00000101  ...x.....[. ....
 0010 7e602b00 4b00090d 06200000 2400ba70  ~`+.K.... ..$..p
 0020 00000004 00000565 765840c8 08768215  .......evX@..v..
 0030 850710fe 76580002 00808035 81071100  ....vX.....5....
 0040 1880701d 4400e001 00004400 e0060000  ..p.D.....D.....
 0050 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0060 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0070 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0080 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0090 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 00a0 e1000078 60b00100 000b7121 00b08240  ...x`.....q!...@
 00b0 e1000078 60310200 005b0120 00f00c65  ...x`1...[. ...e
 00c0 12000068 10f62c00 000018e0 1d3c0000  ...h..,......<..
 00d0 00000000 00007808 8019780c 8018b881  ......x...x.....
 00e0 9c1cb883 dc1cb885 1c1db887 5c1db889  ............\...
 00f0 9c1db88b dc1db88d 1c1eb88f 5c1eb891  ............\...
 0100 9c1eb893 dc1eb895 1c1fb897 5c1fb899  ............\...
 0110 9c1fb89b dc1fb89d 1c1a743f b9840661  ..........t?...a
 0120 78801919 78909919 f872481a f4e59885  x...x....rH.....
 0130 0661f872 50190a95 0428e672 d4691006  .a.rP....(.r.i..
 0140 7808001d 780c001c 7800551a 7810d51a  x...x...x.U.x...
 0150 7808001b 780c801d 7808801c 780c0018  x...x...x...x...
 0160 78800818 02304844 006086ff f8725818  x....0HD.`...rX.
 0170 22550029 e672dc00 78004419 7810c419  "U.).r..x.D.x...
 0180 7800331a 2215282a 6610b302 f8726018  x.3.".(*f....r`.
 0190 f872e418 f8726818 2215442b e672ec00  .r...rh.".D+.r..
 01a0 78805d19 d420bb73 b7fff872 70182215  x.].. .s...rp.".
 01b0 682ce672 f4007880 4c1a7890 cc1af872  h,.r..x.L.x....r
 01c0 78182215 842ce672 fc007800 33197810  x."..,.r..x.3.x.
 01d0 b319f872 20182215 882ce672 a4000000  ...r ."..,.r....
 01e0 a9204401 00000000 005b0120 00f02c00  . D......[. ..,.
 01f0 12432024 00f02c00 987c2414 84014000  .C $..,..|$...@.
 0200 00900000 00000000 98061c0a 98606214  .............`b.
 0210 ba78a501 00801020 26f01811 85071800  .x..... &.......
 0220 28100000 00000000 c4010000 f0ff0000  (...............
Contents of section .rela.text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_:
 0000 44000000 2a030000 00000000 4a000000  D...*.......J...
 0010 2a040000 00000000 fc010000 01020000  *...............
 0020 00000000                             ....
Contents of section .comment:
 0000 00636c61 6e672076 65727369 6f6e2031  .clang version 1
 0010 392e302e 30202868 74747073 3a2f2f67  9.0.0 (https://g
 0020 69746875 622e636f 6d2f5869 6c696e78  ithub.com/Xilinx
 0030 2f6c6c76 6d2d6169 65206232 61323739  /llvm-aie b2a279
 0040 63313933 39363034 65326565 38326136  c1939604e2ee82a6
 0050 35313638 33646439 39356465 63633235  51683dd995decc25
 0060 65652900                             ee).
Contents of section .symtab:
 0000 00000000 00000000 00000000 00000000  ................
 0010 4a000000 00000000 00000000 0400f1ff  J...............
 0020 cf000000 40000000 00000000 00000500  ....@...........
 0030 c7000000 c0000000 00000000 00000500  ................
 0040 d7000000 e0010000 00000000 00000500  ................
 0050 b3000000 00000000 10000000 12000200  ................
 0060 6f000000 00000000 30020000 22000500  o.......0..."...
 0070 bb000000 10000000 50000000 12000200  ........P.......

Disassembly of section .text:

00000000 <mv_int8>:
       0: 84 00 00 00 00 00    	j	#0x0
			00000000:  R_AIE_1	_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_
		...
       e: 00 00        	nop	

00000010 <zero_m_int8>:
      10: 2c 00 00 00 00 00    	mova	r0, #0x0;		nopx	
      16: f8 72 02 18  	vbcst.32	 x0, r0
      1a: 00 00        	nop	
      1c: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      20: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      24: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      28: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      2c: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      30: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      34: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      38: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      3c: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      40: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      44: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      48: 5c 00 50 50 85 03    	vst	 wl0, [p0], #0x20;		ret	lr
      4e: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      52: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      56: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      5a: 98 2a 04 08  	vst	 wl0, [p0, #0x0]
      5e: 00 00        	nop	

Disassembly of section .text._Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_:

00000000 <_Z22matvec_vectorized_int8Iaiu7__acc32Lj128ELj128ELj16EEvPT_S1_PT0_>:
       0: e1 00 00 78 a5 01 08 00 00 5b 01 20 00 00 01 01      	mova	r1, #0x8;		nopb	;		nops	;		movx	r0, #0x0;		nopm	;		nopv	
      10: 7e 60 2b 00 4b 00 09 0d 06 20 00 00 24 00    	mova	r4, #0x1;		nopb	;		movx	r3, #0x3;		mov	r2, #0x2;		nops	
      1e: ba 70 00 00 00 04 00 00 05 65	mova	r5, #0x328;		paddxm	 [sp], #0x80
      28: 76 58 40 c8 08 76 82 15 85 07 10 fe  	mova	r16, #-0x10;		st	 r8, [sp, #-124];		movx	r7, #0x70;		mov	r6, #0x40
      34: 76 58 00 02 00 80 80 35 81 07 11 00  	mova	r17, #0x0;		st	 r9, [sp, #-128];		event	#0;		mov	m0, #0x200

00000040 <.LBB1_1>:
      40: 18 80 70 1d  	add.nc	lc, r1, #0x0
      44: 44 00 e0 01 00 00    	movxm	ls, #0x0
			00000044:  R_AIE_42	.LBB1_2
      4a: 44 00 e0 06 00 00    	movxm	le, #0x0
			0000004a:  R_AIE_42	.L_LEnd0
      50: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      60: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      70: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      80: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      90: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      a0: e1 00 00 78 60 b0 01 00 00 0b 71 21 00 b0 82 40      	vlda	 bmll0, [p2, #0x0];		nopb	;		movs	m1, r17;		nopx	;		mov	p3, p0;		nopv	
      b0: e1 00 00 78 60 31 02 00 00 5b 01 20 00 f0 0c 65      	padda	 [p3], m1;		nopb	;		nops	;		nopx	;		mov	p4, p1;		nopv	

000000c0 <.LBB1_2>:
      c0: 12 00 00 68 10 f6 2c 00      	nopa	;		vldb	 x0, [p3], m0;		nopx	
      c8: 00 00        	nop	
      ca: 18 e0 1d 3c  	vldb.128	 wl7, [p4], #0x10
		...
      d6: 78 08 80 19  	vshuffle	x3, x0, x0, r2
      da: 78 0c 80 18  	vshuffle	x1, x0, x0, r3
      de: b8 81 9c 1c  	vextract.8	 r18, x7, #0x0, vaddsign1
      e2: b8 83 dc 1c  	vextract.8	 r19, x7, #0x1, vaddsign1
      e6: b8 85 1c 1d  	vextract.8	 r20, x7, #0x2, vaddsign1
      ea: b8 87 5c 1d  	vextract.8	 r21, x7, #0x3, vaddsign1
      ee: b8 89 9c 1d  	vextract.8	 r22, x7, #0x4, vaddsign1
      f2: b8 8b dc 1d  	vextract.8	 r23, x7, #0x5, vaddsign1
      f6: b8 8d 1c 1e  	vextract.8	 r24, x7, #0x6, vaddsign1
      fa: b8 8f 5c 1e  	vextract.8	 r25, x7, #0x7, vaddsign1
      fe: b8 91 9c 1e  	vextract.8	 r26, x7, #0x8, vaddsign1
     102: b8 93 dc 1e  	vextract.8	 r27, x7, #0x9, vaddsign1
     106: b8 95 1c 1f  	vextract.8	 r28, x7, #0xa, vaddsign1
     10a: b8 97 5c 1f  	vextract.8	 r29, x7, #0xb, vaddsign1
     10e: b8 99 9c 1f  	vextract.8	 r30, x7, #0xc, vaddsign1
     112: b8 9b dc 1f  	vextract.8	 r31, x7, #0xd, vaddsign1
     116: b8 9d 1c 1a  	vextract.8	 r8, x7, #0xe, vaddsign1
     11a: 74 3f b9 84 06 61    	vldb	 x0, [p3], m0;		vextract.8	 r9, x7, #0xf, vaddsign1
     120: 78 80 19 19  	vshuffle	x2, x3, x3, r0
     124: 78 90 99 19  	vshuffle	x3, x3, x3, r4
     128: f8 72 48 1a  	vbcst.8	 x4, r18
     12c: f4 e5 98 85 06 61    	vldb	 x0, [p3], m0;		vbcst.8	 x5, r19
     132: f8 72 50 19  	vbcst.8	 x2, r20
     136: 0a 95 04 28 e6 72 d4 69 10 06	vldb	 x0, [p3], m0;		vbcst.8	 x3, r21;		vmac	dm0, dm0, y1, y2,r5
     140: 78 08 00 1d  	vshuffle	x10, x0, x0, r2
     144: 78 0c 00 1c  	vshuffle	x8, x0, x0, r3
     148: 78 00 55 1a  	vshuffle	x4, x10, x10, r0
     14c: 78 10 d5 1a  	vshuffle	x5, x10, x10, r4
     150: 78 08 00 1b  	vshuffle	x6, x0, x0, r2
     154: 78 0c 80 1d  	vshuffle	x11, x0, x0, r3
     158: 78 08 80 1c  	vshuffle	x9, x0, x0, r2
     15c: 78 0c 00 18  	vshuffle	x0, x0, x0, r3
     160: 78 80 08 18  	vshuffle	x0, x1, x1, r0
     164: 02 30 48 44 00 60 86 ff      	vst	 x0, [sp, #-0x40];		vshuffle	x1, x1, x1, r4
     16c: f8 72 58 18  	vbcst.8	 x0, r22
     170: 22 55 00 29 e6 72 dc 00      	vbcst.8	 x1, r23;		vmac	dm1, dm0, y0, y1,r5
     178: 78 00 44 19  	vshuffle	x2, x8, x8, r0
     17c: 78 10 c4 19  	vshuffle	x3, x8, x8, r4
     180: 78 00 33 1a  	vshuffle	x4, x6, x6, r0
     184: 22 15 28 2a 66 10 b3 02      	vshuffle	x5, x6, x6, r4;		vmac	dm2, dm1, y2, y0,r5
     18c: f8 72 60 18  	vbcst.8	 x0, r24
     190: f8 72 e4 18  	vbcst.8	 x1, r25
     194: f8 72 68 18  	vbcst.8	 x0, r26
     198: 22 15 44 2b e6 72 ec 00      	vbcst.8	 x1, r27;		vmac	dm3, dm2, y1, y0,r5
     1a0: 78 80 5d 19  	vshuffle	x2, x11, x11, r0
     1a4: d4 20 bb 73 b7 ff    	vlda	 x6, [sp, #-0x40];		vshuffle	x3, x11, x11, r4
     1aa: f8 72 70 18  	vbcst.8	 x0, r28
     1ae: 22 15 68 2c e6 72 f4 00      	vbcst.8	 x1, r29;		vmac	dm4, dm3, y2, y0,r5
     1b6: 78 80 4c 1a  	vshuffle	x4, x9, x9, r0
     1ba: 78 90 cc 1a  	vshuffle	x5, x9, x9, r4
     1be: f8 72 78 18  	vbcst.8	 x0, r30
     1c2: 22 15 84 2c e6 72 fc 00      	vbcst.8	 x1, r31;		vmac	dm4, dm4, y1, y0,r5
     1ca: 78 00 33 19  	vshuffle	x2, x6, x6, r0
     1ce: 78 10 b3 19  	vshuffle	x3, x6, x6, r4
     1d2: f8 72 20 18  	vbcst.8	 x0, r8
     1d6: 22 15 88 2c e6 72 a4 00      	vbcst.8	 x1, r9;		vmac	dm4, dm4, y2, y0,r5
     1de: 00 00        	nop	

000001e0 <.L_LEnd0>:
     1e0: a9 20 44 01 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		vmac	dm0, dm4, y1, y0,r5
     1f0: 12 43 20 24 00 f0 2c 00      	nopa	;		nopb	;		add	r16, r16, #0x10
     1f8: 98 7c 24 14  	ltu	 r18, r16, r7
     1fc: 84 01 40 00 00 90    	jnz	 r18, #0x0
			000001fc:  R_AIE_1	.LBB1_1
     202: 00 00        	nop	
     204: 00 00        	nop	
     206: 00 00        	nop	
     208: 98 06 1c 0a  	vst	 bmll0, [p2], #0x40
     20c: 98 60 62 14  	add	 r17, r17, r6
     210: ba 78 a5 01 00 80 10 20 26 f0	lda	 r9, [sp, #-128];		event	#1;		nopm	
     21a: 18 11 85 07  	lda	 r8, [sp, #-124]
     21e: 18 00 28 10  	ret	lr
     222: 00 00        	nop	
     224: 00 00        	nop	
     226: 00 00        	nop	
     228: c4 01 00 00 f0 ff    	paddxm	 [sp], #-0x80
     22e: 00 00        	nop	
