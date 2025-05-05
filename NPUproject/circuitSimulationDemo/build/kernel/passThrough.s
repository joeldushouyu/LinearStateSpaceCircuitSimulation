
build/kernel/passThrough.o:	file format elf32-aie
architecture: aie2p
start address: 0x00000000

Program Header:

Dynamic Section:

Sections:
Idx Name                                        Size     VMA      Type
  0                                             00000000 00000000 
  1 .strtab                                     00000188 00000000 
  2 .text                                       00000050 00000000 TEXT
  3 .rela.text                                  0000003c 00000000 
  4 .group                                      0000000c 00000000 
  5 .text._Z18passThrough_simpleIfEvPfS0_i      00000070 00000000 TEXT
  6 .rela.text._Z18passThrough_simpleIfEvPfS0_i 00000018 00000000 
  7 .group                                      0000000c 00000000 
  8 .text._Z10accumValueIfEvPfS0_iiiii          00000200 00000000 TEXT
  9 .rela.text._Z10accumValueIfEvPfS0_iiiii     00000090 00000000 
 10 .linker-options                             00000000 00000000 
 11 .comment                                    00000064 00000000 
 12 .note.GNU-stack                             00000000 00000000 
 13 .llvm_addrsig                               00000000 00000000 
 14 .symtab                                     00000140 00000000 

SYMBOL TABLE:
00000000 l    df *ABS*	00000000 passThrough.cc
00000040 l       .text._Z18passThrough_simpleIfEvPfS0_i	00000000 .LBB1_2
000001c0 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_9
000000e0 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_3
000000c0 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_2
00000160 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_6
00000100 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_4
00000170 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_7
00000190 l       .text._Z10accumValueIfEvPfS0_iiiii	00000000 .LBB6_8
00000000 g     F .text	00000010 passThroughLine_float_0
00000000  w    F .text._Z18passThrough_simpleIfEvPfS0_i	00000070 _Z18passThrough_simpleIfEvPfS0_i
00000000         *UND*	00000000 memcpy
00000010 g     F .text	00000010 passThroughLine_float_1
00000020 g     F .text	00000010 passThroughLine_float_2
00000030 g     F .text	00000010 passThroughLine_float_3
00000040 g     F .text	00000010 accum_float_value
00000000  w    F .text._Z10accumValueIfEvPfS0_iiiii	00000200 _Z10accumValueIfEvPfS0_iiiii
00000000         *UND*	00000000 __divsi3
00000000         *UND*	00000000 __addsf3

DYNAMIC SYMBOL TABLE:
Contents of section .strtab:
 0000 006d656d 63707900 2e72656c 612e7465  .memcpy..rela.te
 0010 7874002e 636f6d6d 656e7400 2e6c696e  xt..comment..lin
 0020 6b65722d 6f707469 6f6e7300 2e67726f  ker-options..gro
 0030 7570002e 6e6f7465 2e474e55 2d737461  up..note.GNU-sta
 0040 636b002e 72656c61 2e746578 742e5f5a  ck..rela.text._Z
 0050 31306163 63756d56 616c7565 49664576  10accumValueIfEv
 0060 50665330 5f696969 6969002e 72656c61  PfS0_iiiii..rela
 0070 2e746578 742e5f5a 31387061 73735468  .text._Z18passTh
 0080 726f7567 685f7369 6d706c65 49664576  rough_simpleIfEv
 0090 50665330 5f69002e 6c6c766d 5f616464  PfS0_i..llvm_add
 00a0 72736967 00616363 756d5f66 6c6f6174  rsig.accum_float
 00b0 5f76616c 75650070 61737354 68726f75  _value.passThrou
 00c0 67682e63 63002e73 74727461 62002e73  gh.cc..strtab..s
 00d0 796d7461 62002e4c 4242365f 39002e4c  ymtab..LBB6_9..L
 00e0 4242365f 38002e4c 4242365f 37002e4c  BB6_8..LBB6_7..L
 00f0 4242365f 36002e4c 4242365f 34005f5f  BB6_6..LBB6_4.__
 0100 64697673 6933005f 5f616464 73663300  divsi3.__addsf3.
 0110 70617373 5468726f 7567684c 696e655f  passThroughLine_
 0120 666c6f61 745f3300 2e4c4242 365f3300  float_3..LBB6_3.
 0130 70617373 5468726f 7567684c 696e655f  passThroughLine_
 0140 666c6f61 745f3200 2e4c4242 365f3200  float_2..LBB6_2.
 0150 2e4c4242 315f3200 70617373 5468726f  .LBB1_2.passThro
 0160 7567684c 696e655f 666c6f61 745f3100  ughLine_float_1.
 0170 70617373 5468726f 7567684c 696e655f  passThroughLine_
 0180 666c6f61 745f3000                    float_0.
Contents of section .text:
 0000 84000000 00000000 00000000 00000000  ................
 0010 84000000 00000000 00000000 00000000  ................
 0020 84000000 00000000 00000000 00000000  ................
 0030 84000000 00000000 00000000 00000000  ................
 0040 84000000 00000000 00000000 00000000  ................
Contents of section .rela.text:
 0000 00000000 010b0000 00000000 10000000  ................
 0010 010b0000 00000000 20000000 010b0000  ........ .......
 0020 00000000 30000000 010b0000 00000000  ....0...........
 0030 40000000 01110000 00000000           @...........
Contents of section .group:
 0000 01000000 05000000 06000000           ............
Contents of section .text._Z18passThrough_simpleIfEvPfS0_i:
 0000 18080000 98094210 84014000 00080000  ......B...@.....
 0010 0000c401 00000800 983dc00f 18001010  .........=......
 0020 ba400000 000000f0 2c000000 18080200  .@......,.......
 0030 981d0010 44febff0 0f00e481 c1940200  ....D...........
 0040 e1000078 a5010080 105b0120 002007f8  ...x.....[. . ..
 0050 18000010 00000000 00000000 00001800  ................
 0060 28100000 00000000 c4010000 f8ff0000  (...............
Contents of section .rela.text._Z18passThrough_simpleIfEvPfS0_i:
 0000 08000000 01020000 00000000 20000000  ............ ...
 0010 020c0000 00000000                    ........
Contents of section .group:
 0000 01000000 08000000 09000000           ............
Contents of section .text._Z10accumValueIfEvPfS0_iiiii:
 0000 c4010000 08005c00 00b0e3f8 989dc30f  ......\.........
 0010 9875d50f 9895d10f 9815e10f 3a410000  .u..........:A..
 0020 000000b0 2afb98b5 cd0f0270 603003b0  ....*......p`0..
 0030 a6fb0270 106801b0 87fc3a79 9008adc0  ...p.h....:y....
 0040 02b03af9 76781049 ad11068b 84070d00  ..:.vx.I........
 0050 e1000040 00000000 005b0120 00f02c00  ...@.....[. ..,.
 0060 00000000 0000f820 501ae441 28b15450  ....... P..A(.TP
 0070 7e602b00 af348089 422300f0 2c008401  ~`+..4..B#..,...
 0080 40000008 00000000 00000000 18001010  @...............
 0090 e1000020 00000000 005b0120 00f02c00  ... .....[. ..,.
 00a0 ba781048 01000000 4000980d 0213e441  .x.H....@......A
 00b0 01b08158 d44102f0 0ce12c1b b8f40cc1  ...X.A....,.....
 00c0 e1000078 a501f88f 105b0120 00f02c00  ...x.....[. ..,.
 00d0 84010000 00400000 00000000 00000000  .....@..........
 00e0 92994223 00f02c00 84014000 00080000  ..B#..,...@.....
 00f0 00000000 0000ba78 608eadb4 12000000  .......x`.......
 0100 7e602b00 00000000 002000d0 8ac30401  ~`+...... ......
 0110 00000000 00000000 00000000 f8205018  ............. P.
 0120 e1000078 a501f8bf 165b0120 00f02c00  ...x.....[. ..,.
 0130 84014000 00580000 00000000 00000000  ..@..X..........
 0140 7e602b00 04000000 002000f0 2c000000  ~`+...... ..,...
 0150 00000000 02709003 006081d1 98670806  .....p...`...g..
 0160 e1000078 10330300 005b0120 00f02c00  ...x.3...[. ..,.
 0170 7e602b00 af3480a9 442300f0 2c008401  ~`+..4..D#..,...
 0180 40000010 00000000 00000000 f8205518  @............ U.
 0190 7e602b00 af3400ff 432000f0 2c008401  ~`+..4..C ..,...
 01a0 40000008 00000000 00009811 1c0f0000  @...............
 01b0 84000000 00000000 00000000 00000000  ................
 01c0 ba78a501 00801020 73f81819 c70718d1  .x..... s.......
 01d0 c9071839 e40718b1 cd071891 d1071871  ...9...........q
 01e0 d5071851 d9071831 dd071811 e1071800  ...Q...1........
 01f0 28100000 00000000 c4010000 f8ff0000  (...............
Contents of section .rela.text._Z10accumValueIfEvPfS0_iiiii:
 0000 1c000000 02120000 00000000 50000000  ............P...
 0010 00120000 00000000 7e000000 01030000  ........~.......
 0020 00000000 90000000 00040000 00000000  ................
 0030 d0000000 01030000 00000000 e8000000  ................
 0040 01060000 00000000 0e010000 01130000  ................
 0050 00000000 30010000 01070000 00000000  ....0...........
 0060 40010000 07080000 00000000 7e010000  @...........~...
 0070 01050000 00000000 9e010000 01090000  ................
 0080 00000000 b0010000 01050000 00000000  ................
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
 0010 b7000000 00000000 00000000 0400f1ff  ................
 0020 50010000 40000000 00000000 00000500  P...@...........
 0030 d6000000 c0010000 00000000 00000800  ................
 0040 28010000 e0000000 00000000 00000800  (...............
 0050 48010000 c0000000 00000000 00000800  H...............
 0060 ee000000 60010000 00000000 00000800  ....`...........
 0070 f6000000 00010000 00000000 00000800  ................
 0080 e6000000 70010000 00000000 00000800  ....p...........
 0090 de000000 90010000 00000000 00000800  ................
 00a0 70010000 00000000 10000000 12000200  p...............
 00b0 76000000 00000000 70000000 22000500  v.......p..."...
 00c0 01000000 00000000 00000000 10000000  ................
 00d0 58010000 10000000 10000000 12000200  X...............
 00e0 30010000 20000000 10000000 12000200  0... ...........
 00f0 10010000 30000000 10000000 12000200  ....0...........
 0100 a5000000 40000000 10000000 12000200  ....@...........
 0110 4e000000 00000000 00020000 22000800  N..........."...
 0120 fe000000 00000000 00000000 10000000  ................
 0130 07010000 00000000 00000000 10000000  ................

Disassembly of section .text:

00000000 <passThroughLine_float_0>:
       0: 84 00 00 00 00 00    	j	#0x0
			00000000:  R_AIE_1	_Z18passThrough_simpleIfEvPfS0_i
		...
       e: 00 00        	nop	

00000010 <passThroughLine_float_1>:
      10: 84 00 00 00 00 00    	j	#0x0
			00000010:  R_AIE_1	_Z18passThrough_simpleIfEvPfS0_i
		...
      1e: 00 00        	nop	

00000020 <passThroughLine_float_2>:
      20: 84 00 00 00 00 00    	j	#0x0
			00000020:  R_AIE_1	_Z18passThrough_simpleIfEvPfS0_i
		...
      2e: 00 00        	nop	

00000030 <passThroughLine_float_3>:
      30: 84 00 00 00 00 00    	j	#0x0
			00000030:  R_AIE_1	_Z18passThrough_simpleIfEvPfS0_i
		...
      3e: 00 00        	nop	

00000040 <accum_float_value>:
      40: 84 00 00 00 00 00    	j	#0x0
			00000040:  R_AIE_1	_Z10accumValueIfEvPfS0_iiiii
		...
      4e: 00 00        	nop	

Disassembly of section .text._Z18passThrough_simpleIfEvPfS0_i:

00000000 <_Z18passThrough_simpleIfEvPfS0_i>:
       0: 18 08 00 00  	mova	r1, #0x0
       4: 98 09 42 10  	ge	 r1, r1, r0
       8: 84 01 40 00 00 08    	jnz	 r1, #0x0
			00000008:  R_AIE_1	.LBB1_2
       e: 00 00        	nop	
      10: 00 00        	nop	
      12: c4 01 00 00 08 00    	paddxm	 [sp], #0x40
      18: 98 3d c0 0f  	st	 lr, [sp, #-64]
      1c: 18 00 10 10  	event	#0
      20: ba 40 00 00 00 00 00 f0 2c 00	nopa	;		jl	#0x0
			00000020:  R_AIE_2	memcpy
      2a: 00 00        	nop	
      2c: 18 08 02 00  	mova	r1, #0x2
      30: 98 1d 00 10  	lshl	 r0, r0, r1
      34: 44 fe bf f0 0f 00    	movxm	r1, #0xfffff
      3a: e4 81 c1 94 02 00    	and	 r0, r0, r1;		mov	p2, p0

00000040 <.LBB1_2>:
      40: e1 00 00 78 a5 01 00 80 10 5b 01 20 00 20 07 f8      	lda	 lr, [sp, #-64];		nopb	;		nops	;		event	#1;		nopm	;		nopv	
      50: 18 00 00 10  	nopx	
		...
      5c: 00 00        	nop	
      5e: 18 00 28 10  	ret	lr
      62: 00 00        	nop	
      64: 00 00        	nop	
      66: 00 00        	nop	
      68: c4 01 00 00 f8 ff    	paddxm	 [sp], #-0x40
      6e: 00 00        	nop	

Disassembly of section .text._Z10accumValueIfEvPfS0_iiiii:

00000000 <_Z10accumValueIfEvPfS0_iiiii>:
       0: c4 01 00 00 08 00    	paddxm	 [sp], #0x40
       6: 5c 00 00 b0 e3 f8    	st	 p6, [sp, #-60];		nopx	
       c: 98 9d c3 0f  	st	 p7, [sp, #-64]
      10: 98 75 d5 0f  	st	 r11, [sp, #-44]
      14: 98 95 d1 0f  	st	 r12, [sp, #-48]
      18: 98 15 e1 0f  	st	 r8, [sp, #-32]
      1c: 3a 41 00 00 00 00 00 b0 2a fb	st	 r10, [sp, #-40];		jl	#0x0
			0000001c:  R_AIE_2	__divsi3
      26: 98 b5 cd 0f  	st	 r13, [sp, #-52]
      2a: 02 70 60 30 03 b0 a6 fb      	st	 r9, [sp, #-36];		mov	p6, p0
      32: 02 70 10 68 01 b0 87 fc      	st	 lr, [sp, #-28];		mov	r11, r0
      3a: 3a 79 90 08 ad c0 02 b0 3a f9	st	 r14, [sp, #-56];		or	 r12, r1, r1;		mov	r8, r2
      44: 76 78 10 49 ad 11 06 8b 84 07 0d 00  	mova	r13, #0x0;		movs	p7, p1;		or	 r1, r3, r3;		mov	r10, r4
      50: e1 00 00 40 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		jl	#0x0;		nopv	
			00000050:  R_AIE_0	__divsi3
      60: 00 00        	nop	
      62: 00 00        	nop	
      64: 00 00        	nop	
      66: f8 20 50 1a  	mov	r9, r0
      6a: e4 41 28 b1 54 50    	or	 r1, r10, r10;		mov	r2, r8
      70: 7e 60 2b 00 af 34 80 89 42 23 00 f0 2c 00    	nopa	;		nopb	;		ge	 r1, r13, r8;		nopm	;		nops	
      7e: 84 01 40 00 00 08    	jnz	 r1, #0x0
			0000007e:  R_AIE_1	.LBB6_9
		...
      8c: 18 00 10 10  	event	#0
      90: e1 00 00 20 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		j	#0x0;		nopv	
			00000090:  R_AIE_0	.LBB6_3
      a0: ba 78 10 48 01 00 00 00 40 00	mova	r0, #0x2;		nopx	;		mov	r10, r0
      aa: 98 0d 02 13  	lshl	 r1, r12, r0
      ae: e4 41 01 b0 81 58    	lshl	 r2, r11, r0;		mov	m0, r1
      b4: d4 41 02 f0 0c e1    	padda	 [p7], m0;		mov	m0, r2
      ba: 2c 1b b8 f4 0c c1    	padda	 [p6], m0;		lshl	 r14, r9, r0

000000c0 <.LBB6_2>:
      c0: e1 00 00 78 a5 01 f8 8f 10 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		add	r8, r8, #-0x1;		nopm	;		nopv	
      d0: 84 01 00 00 00 40    	jz	 r8, #0x0
			000000d0:  R_AIE_1	.LBB6_9
		...
      de: 00 00        	nop	

000000e0 <.LBB6_3>:
      e0: 92 99 42 23 00 f0 2c 00      	nopa	;		nopb	;		ge	 r1, r13, r9
      e8: 84 01 40 00 00 08    	jnz	 r1, #0x0
			000000e8:  R_AIE_1	.LBB6_6
		...
      f6: ba 78 60 8e ad b4 12 00 00 00	mova	r0, #0x0;		or	 r11, r9, r9;		mov	r12, p6

00000100 <.LBB6_4>:
     100: 7e 60 2b 00 00 00 00 00 00 20 00 d0 8a c3    	lda	 r2, [p6], #4;		nopb	;		nopxm	;		nops	
     10e: 04 01 00 00 00 00    	jl	#0x0
			0000010e:  R_AIE_1	__addsf3
		...
     11c: f8 20 50 18  	mov	r1, r0
     120: e1 00 00 78 a5 01 f8 bf 16 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		add	r11, r11, #-0x1;		nopm	;		nopv	
     130: 84 01 40 00 00 58    	jnz	 r11, #0x0
			00000130:  R_AIE_1	.LBB6_4
		...
     13e: 00 00        	nop	
     140: 7e 60 2b 00 04 00 00 00 00 20 00 f0 2c 00    	nopa	;		nopb	;		j	#0x0;		nops	
			00000140:  R_AIE_7	.LBB6_7
     14e: 00 00        	nop	
     150: 00 00        	nop	
     152: 00 00        	nop	
     154: 02 70 90 03 00 60 81 d1      	movs	p6, r12;		mov	m0, r14
     15c: 98 67 08 06  	padda	 [p6], m0

00000160 <.LBB6_6>:
     160: e1 00 00 78 10 33 03 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopx	;		mov	p6, r12;		nopv	

00000170 <.LBB6_7>:
     170: 7e 60 2b 00 af 34 80 a9 44 23 00 f0 2c 00    	nopa	;		nopb	;		ge	 r2, r13, r10;		nopm	;		nops	
     17e: 84 01 40 00 00 10    	jnz	 r2, #0x0
			0000017e:  R_AIE_1	.LBB6_2
		...
     18c: f8 20 55 18  	mov	r1, r10

00000190 <.LBB6_8>:
     190: 7e 60 2b 00 af 34 00 ff 43 20 00 f0 2c 00    	nopa	;		nopb	;		add	r1, r1, #-0x1;		nopm	;		nops	
     19e: 84 01 40 00 00 08    	jnz	 r1, #0x0
			0000019e:  R_AIE_1	.LBB6_8
     1a4: 00 00        	nop	
     1a6: 00 00        	nop	
     1a8: 00 00        	nop	
     1aa: 98 11 1c 0f  	st	 r0, [p7], #4
     1ae: 00 00        	nop	
     1b0: 84 00 00 00 00 00    	j	#0x0
			000001b0:  R_AIE_1	.LBB6_2
		...
     1be: 00 00        	nop	

000001c0 <.LBB6_9>:
     1c0: ba 78 a5 01 00 80 10 20 73 f8	lda	 p7, [sp, #-64];		event	#1;		nopm	
     1ca: 18 19 c7 07  	lda	 p6, [sp, #-60]
     1ce: 18 d1 c9 07  	lda	 r14, [sp, #-56]
     1d2: 18 39 e4 07  	lda	 lr, [sp, #-28]
     1d6: 18 b1 cd 07  	lda	 r13, [sp, #-52]
     1da: 18 91 d1 07  	lda	 r12, [sp, #-48]
     1de: 18 71 d5 07  	lda	 r11, [sp, #-44]
     1e2: 18 51 d9 07  	lda	 r10, [sp, #-40]
     1e6: 18 31 dd 07  	lda	 r9, [sp, #-36]
     1ea: 18 11 e1 07  	lda	 r8, [sp, #-32]
     1ee: 18 00 28 10  	ret	lr
     1f2: 00 00        	nop	
     1f4: 00 00        	nop	
     1f6: 00 00        	nop	
     1f8: c4 01 00 00 f8 ff    	paddxm	 [sp], #-0x40
     1fe: 00 00        	nop	
