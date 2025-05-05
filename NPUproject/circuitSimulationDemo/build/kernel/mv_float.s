
build/kernel/mv_float.o:	file format elf32-aie
architecture: aie2p
start address: 0x00000000

Program Header:

Dynamic Section:

Sections:
Idx Name                                                                     Size     VMA      Type
  0                                                                          00000000 00000000 
  1 .strtab                                                                  00000124 00000000 
  2 .text                                                                    00000110 00000000 TEXT
  3 .rela.text                                                               00000048 00000000 
  4 .group                                                                   0000000c 00000000 
  5 .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_      00000bc0 00000000 TEXT
  6 .rela.text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_ 00000024 00000000 
  7 .linker-options                                                          00000000 00000000 
  8 .comment                                                                 00000064 00000000 
  9 .note.GNU-stack                                                          00000000 00000000 
 10 .llvm_addrsig                                                            00000000 00000000 
 11 .symtab                                                                  000000d0 00000000 

SYMBOL TABLE:
00000000 l    df *ABS*	00000000 mv_float.cc
00000030 l       .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_	00000000 .LBB2_1
000000b0 l       .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_	00000000 .LBB2_2
00000b80 l       .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_	00000000 .L_LEnd0
00000000 g     F .text	000000d0 test_float_operation
00000000         *UND*	00000000 __addsf3
00000000         *UND*	00000000 __extendsfdf2
00000000         *UND*	00000000 __adddf3
00000000         *UND*	00000000 __truncdfsf2
000000d0 g     F .text	00000010 mv_float32
00000000  w    F .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_	00000bc0 _Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
000000e0 g     F .text	00000030 zero_m_float32

DYNAMIC SYMBOL TABLE:
Contents of section .strtab:
 0000 002e7265 6c612e74 65787400 2e636f6d  ..rela.text..com
 0010 6d656e74 002e6c69 6e6b6572 2d6f7074  ment..linker-opt
 0020 696f6e73 002e6772 6f757000 74657374  ions..group.test
 0030 5f666c6f 61745f6f 70657261 74696f6e  _float_operation
 0040 002e6e6f 74652e47 4e552d73 7461636b  ..note.GNU-stack
 0050 002e6c6c 766d5f61 64647273 6967006d  ..llvm_addrsig.m
 0060 765f666c 6f61742e 6363002e 73747274  v_float.cc..strt
 0070 6162002e 73796d74 6162002e 72656c61  ab..symtab..rela
 0080 2e746578 742e5f5a 31346d61 74566563  .text._Z14matVec
 0090 5f666c6f 61743332 49666675 31305f5f  _float32Iffu10__
 00a0 61636366 6c6f6174 4c6a3634 454c6a36  accfloatLj64ELj6
 00b0 34454c6a 31364545 7650545f 53315f50  4ELj16EEvPT_S1_P
 00c0 54305f00 5f5f6164 64736633 005f5f61  T0_.__addsf3.__a
 00d0 64646466 33005f5f 7472756e 63646673  dddf3.__truncdfs
 00e0 6632005f 5f657874 656e6473 66646632  f2.__extendsfdf2
 00f0 002e4c42 42325f32 006d765f 666c6f61  ..LBB2_2.mv_floa
 0100 74333200 7a65726f 5f6d5f66 6c6f6174  t32.zero_m_float
 0110 3332002e 4c424232 5f31002e 4c5f4c45  32..LBB2_1..L_LE
 0120 6e643000                             nd0.
Contents of section .text:
 0000 b6400000 00000020 00f02c00 0000c401  .@..... ..,.....
 0010 00000800 983dc40f 9815c10f f8a0111a  .....=..........
 0020 e1000040 00000000 005b0120 00f02c00  ...@.....[. ..,.
 0030 18000010 00000000 0000e441 28b14000  ...........A(.@.
 0040 e1000040 00000000 005b0120 00f02c00  ...@.....[. ..,.
 0050 2c0000f0 2c000000 00000000 f8209018  ,...,........ ..
 0060 ba400000 000000f0 2c000000 0000443e  .@......,.....D>
 0070 2a82eb51 4470bd02 5940e441 a1b18000  *..QDp..Y@.A....
 0080 e1000040 00000000 005b0120 00f02c00  ...@.....[. ..,.
 0090 18000010 00000000 0000e441 a0b08208  ...........A....
 00a0 e1000000 00000000 005b0120 002087f8  .........[. . ..
 00b0 00000000 00000000 00001811 c1071800  ................
 00c0 28100000 00000000 c4010000 f8ff0000  (...............
 00d0 84000000 00000000 00000000 00000000  ................
 00e0 2c000000 0000f872 02180000 982a1c08  ,......r.....*..
 00f0 982a1c08 982a1c08 5c005050 8503982a  .*...*..\.PP...*
 0100 1c08982a 1c08982a 1c08982a 04080000  ...*...*...*....
Contents of section .rela.text:
 0000 00000000 04060000 00000000 20000000  ............ ...
 0010 00060000 00000000 40000000 00070000  ........@.......
 0020 00000000 60000000 02080000 00000000  ....`...........
 0030 80000000 00090000 00000000 d0000000  ................
 0040 010b0000 00000000                    ........
Contents of section .group:
 0000 01000000 05000000 06000000           ............
Contents of section .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_:
 0000 b678a501 00800020 00f02c00 4400bf30  .x..... ..,.D..0
 0010 0000ba10 800f3e00 00000000 ba783901  ......>......x9.
 0020 08260000 03feba78 b9828800 00008107  .&.....x........
 0030 1800701d 4400e001 00004400 e0060000  ..p.D.....D.....
 0040 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0050 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0060 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0070 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0080 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 0090 e1000000 00000000 005b0120 00f02c00  .........[. ..,.
 00a0 e1000078 60b10100 005b0120 00b08240  ...x`....[. ...@
 00b0 1c000080 a6630000 00000000 98951c00  .....c..........
 00c0 00000000 b8811319 0000f872 121bf892  ...........r....
 00d0 0c1b1896 400c1896 410d3800 c0183800  ....@...A.8...8.
 00e0 d0194843 22094843 460af892 0c1a0000  ..HC".HCF.......
 00f0 00000000 1896c00a 1816c10b 3800a81c  ............8...
 0100 3800b81d 48433209 4843560a 00000000  8...HC2.HCV.....
 0110 00000000 1896400b 1816410c 3800301b  ......@...A.8.0.
 0120 3800401c 4861ed0a 4801ed09 00000000  8.@.Ha..H.......
 0130 483d2809 6201f30a 04b0a203 00000000  H=(.b...........
 0140 483d2809 0000f872 961af892 0a1c6201  H=(....r......b.
 0150 e30b02c0 22a81816 c20b6261 f30c2600  ....".....ba..&.
 0160 5005623d 2c092600 b8034843 540a4843  P.b=,.&...HCT.HC
 0170 6e09f892 0a1b483d 300c0000 000062c1  n.....H=0.....b.
 0180 e60b02c0 22681896 c00c6261 f20c2600  ...."h....ba..&.
 0190 3003623d 8c0b2600 c8044843 4c0a4843  0.b=..&...HCL.HC
 01a0 3209483d 700b4861 e30c0000 0000623d  2.H=p.Ha......b=
 01b0 700b02c0 22b86261 e20a02c0 12183800  p...".ba......8.
 01c0 d81d3800 8818483d 680a4821 f6094821  ..8...H=h.H!..H!
 01d0 f70a0000 483d0808 483d2809 6221ec0a  ....H=..H=(.b!..
 01e0 04b0a203 00000000 623d2809 a6831301  ........b=(.....
 01f0 0000f872 121cf892 101c6221 f40b02c0  ...r......b!....
 0200 22381816 c20a6221 ed0c2600 9801623d  "8....b!..&...b=
 0210 2c092600 a8024843 460a4843 6a09f892  ,.&...HCF.HCj...
 0220 101b483d 300c0000 00006261 ef0b02c0  ..H=0.....ba....
 0230 22b81896 400b62e1 ec0c2600 d805623d  "...@.b...&...b=
 0240 8c0b2600 30034843 560a4843 2c09483d  ..&.0.HCV.HC,.H=
 0250 700b4821 f50c0000 0000623d 700b02c0  p.H!......b=p...
 0260 229862e1 f40a02c0 12a83800 c81c3800  ".b.......8...8.
 0270 501d483d 680a4841 f30948c1 f20a0000  P.H=h.HA..H.....
 0280 483d0808 483d2809 6241f70a 04b0a203  H=..H=(.bA......
 0290 00000000 483d2809 0000f872 9618f892  ....H=(....r....
 02a0 021c6241 e70b02c0 22781816 420c62c1  ..bA...."x..B.b.
 02b0 f60c2600 b803623d 2c092600 40044843  ..&...b=,.&.@.HC
 02c0 4e0a4843 7009f892 021b483d 300c0000  N.HCp.....H=0...
 02d0 00006221 eb0b02c0 22981896 c00d62a1  ..b!....".....b.
 02e0 f60c2600 c804623d 8c0b2600 d8054843  ..&...b=..&...HC
 02f0 520a4843 3609483d 700b48c1 e60c0000  R.HC6.H=p.H.....
 0300 0000623d 700b02c0 226862a1 e60a02c0  ..b=p..."hb.....
 0310 12383800 301b3800 9819483d 680a4861  .88.0.8...H=h.Ha
 0320 ec094861 ed0a0000 483d0808 483d2809  ..Ha....H=..H=(.
 0330 6261f20a 04b0a203 00000000 623d2809  ba..........b=(.
 0340 a6851301 0000f872 121df892 141c6261  .......r......ba
 0350 ee0b02c0 22581816 c2086261 f30c2600  ...."X....ba..&.
 0360 a802623d 2c092600 88004843 4a0a4843  ..b=,.&...HCJ.HC
 0370 6209f892 141b483d 300c0000 000062c1  b.....H=0.....b.
 0380 f00b02c0 22681896 c00c6201 f30c2600  ...."h....b...&.
 0390 3003623d 8c0b2600 c8044843 4c0a4843  0.b=..&...HCL.HC
 03a0 3209483d 700b4861 ef0c0000 0000623d  2.H=p.Ha......b=
 03b0 700b02c0 22b86201 ef0a02c0 12783800  p...".b......x8.
 03c0 d81d3800 b81b483d 680a48e1 f6094821  ..8...H=h.H...H!
 03d0 f70a0000 483d0808 483d2809 62e1ec0a  ....H=..H=(.b...
 03e0 04b0a203 00000000 483d2809 0000f872  ........H=(....r
 03f0 9619f892 061c62e1 ea0b02c0 22881816  ......b....."...
 0400 420d6221 ed0c2600 4004623d 2c092600  B.b!..&.@.b=,.&.
 0410 50054843 500a4843 7409f892 061b483d  P.HCP.HCt.....H=
 0420 300c0000 00006261 e30b02c0 22b81896  0.....ba...."...
 0430 400b6221 ec0c2600 d805623d 8c0b2600  @.b!..&...b=..&.
 0440 30034843 560a4843 2c09483d 700b4821  0.HCV.HC,.H=p.H!
 0450 eb0c0000 0000623d 700b02c0 22986221  ......b=p...".b!
 0460 ea0a02c0 12583800 c81c3800 a81a483d  .....X8...8...H=
 0470 680a48a1 f20948c1 f20a0000 483d0808  h.H...H.....H=..
 0480 483d2809 62a1f60a 04b0a203 00000000  H=(.b...........
 0490 623d2809 a6871301 0000f872 921bf892  b=(........r....
 04a0 0e1c62a1 f00b02c0 22181816 c20962c1  ..b.....".....b.
 04b0 f60c2600 8800623d 2c092600 98014843  ..&...b=,.&...HC
 04c0 420a4843 6609f892 0e1b483d 300c0000  B.HCf.....H=0...
 04d0 00006221 f50b02c0 22981896 c00d6241  ..b!....".....bA
 04e0 f70c2600 c804623d 8c0b2600 d8054843  ..&...b=..&...HC
 04f0 520a4843 3609483d 700b48c1 f00c0000  R.HC6.H=p.H.....
 0500 0000623d 700b02c0 22686241 f10a02c0  ..b=p..."hbA....
 0510 12883800 301b3800 401c483d 680a4801  ..8.0.8.@.H=h.H.
 0520 ed094861 ed0a0000 483d0808 483d2809  ..Ha....H=..H=(.
 0530 6201f30a 04b0a203 00000000 483d2809  b...........H=(.
 0540 0000f872 961af892 0a1c6201 e30b02c0  ...r......b.....
 0550 22a81816 c20b6261 f30c2600 5005623d  ".....ba..&.P.b=
 0560 2c092600 b8034843 540a4843 6e09f892  ,.&...HCT.HCn...
 0570 0a1b483d 300c0000 000062c1 e60b02c0  ..H=0.....b.....
 0580 22681896 c00c6261 f20c2600 3003623d  "h....ba..&.0.b=
 0590 8c0b2600 c8044843 4c0a4843 3209483d  ..&...HCL.HC2.H=
 05a0 700b4861 e30c0000 0000623d 700b02c0  p.Ha......b=p...
 05b0 22b86261 e20a02c0 12183800 d81d3800  ".ba......8...8.
 05c0 8818483d 680a4821 f6094821 f70a0000  ..H=h.H!..H!....
 05d0 483d0808 483d2809 6221ec0a 04b0a203  H=..H=(.b!......
 05e0 00000000 623d2809 a6891301 0000f872  ....b=(........r
 05f0 121cf892 101c6221 f40b02c0 22381816  ......b!...."8..
 0600 c20a6221 ed0c2600 9801623d 2c092600  ..b!..&...b=,.&.
 0610 a8024843 460a4843 6a09f892 101b483d  ..HCF.HCj.....H=
 0620 300c0000 00006261 ef0b02c0 22b81896  0.....ba...."...
 0630 400b62e1 ec0c2600 d805623d 8c0b2600  @.b...&...b=..&.
 0640 30034843 560a4843 2c09483d 700b4821  0.HCV.HC,.H=p.H!
 0650 f50c0000 0000623d 700b02c0 229862e1  ......b=p...".b.
 0660 f40a02c0 12a83800 c81c3800 501d483d  ......8...8.P.H=
 0670 680a4841 f30948c1 f20a0000 483d0808  h.HA..H.....H=..
 0680 483d2809 6241f70a 04b0a203 00000000  H=(.bA..........
 0690 483d2809 0000f872 9618f892 021c6241  H=(....r......bA
 06a0 e70b02c0 22781816 420c62c1 f60c2600  ...."x..B.b...&.
 06b0 b803623d 2c092600 40044843 4e0a4843  ..b=,.&.@.HCN.HC
 06c0 7009f892 021b483d 300c0000 00006221  p.....H=0.....b!
 06d0 eb0b02c0 22981896 c00d62a1 f60c2600  ....".....b...&.
 06e0 c804623d 8c0b2600 d8054843 520a4843  ..b=..&...HCR.HC
 06f0 3609483d 700b48c1 e60c0000 0000623d  6.H=p.H.......b=
 0700 700b02c0 226862a1 e60a02c0 12383800  p..."hb......88.
 0710 301b3800 9819483d 680a4861 ec094861  0.8...H=h.Ha..Ha
 0720 ed0a0000 483d0808 483d2809 6261f20a  ....H=..H=(.ba..
 0730 04b0a203 00000000 623d2809 a68b1301  ........b=(.....
 0740 0000f872 121df892 141c6261 ee0b02c0  ...r......ba....
 0750 22581816 c2086261 f30c2600 a802623d  "X....ba..&...b=
 0760 2c092600 88004843 4a0a4843 6209f892  ,.&...HCJ.HCb...
 0770 141b483d 300c0000 000062c1 f00b02c0  ..H=0.....b.....
 0780 22681896 c00c6201 f30c2600 3003623d  "h....b...&.0.b=
 0790 8c0b2600 c8044843 4c0a4843 3209483d  ..&...HCL.HC2.H=
 07a0 700b4861 ef0c0000 0000623d 700b02c0  p.Ha......b=p...
 07b0 22b86201 ef0a02c0 12783800 d81d3800  ".b......x8...8.
 07c0 b81b483d 680a48e1 f6094821 f70a0000  ..H=h.H...H!....
 07d0 483d0808 483d2809 62e1ec0a 04b0a203  H=..H=(.b.......
 07e0 00000000 483d2809 0000f872 9619f892  ....H=(....r....
 07f0 061c62e1 ea0b02c0 22881816 420d6221  ..b....."...B.b!
 0800 ed0c2600 4004623d 2c092600 50054843  ..&.@.b=,.&.P.HC
 0810 500a4843 7409f892 061b483d 300c0000  P.HCt.....H=0...
 0820 00006261 e30b02c0 22b81896 400b6221  ..ba...."...@.b!
 0830 ec0c2600 d805623d 8c0b2600 30034843  ..&...b=..&.0.HC
 0840 560a4843 2c09483d 700b4821 eb0c0000  V.HC,.H=p.H!....
 0850 0000623d 700b02c0 22986221 ea0a02c0  ..b=p...".b!....
 0860 12583800 c81c3800 a81a483d 680a48a1  .X8...8...H=h.H.
 0870 f20948c1 f20a0000 483d0808 483d2809  ..H.....H=..H=(.
 0880 62a1f60a 04b0a203 00000000 623d2809  b...........b=(.
 0890 a68d1301 0000f872 921bf892 0e1c62a1  .......r......b.
 08a0 f00b02c0 22181816 c20962c1 f60c2600  ....".....b...&.
 08b0 8800623d 2c092600 98014843 420a4843  ..b=,.&...HCB.HC
 08c0 6609f892 0e1b483d 300c0000 00006221  f.....H=0.....b!
 08d0 f50b02c0 22981896 c00d6241 f70c2600  ....".....bA..&.
 08e0 c804623d 8c0b2600 d8054843 520a4843  ..b=..&...HCR.HC
 08f0 3609483d 700b48c1 f00c0000 0000623d  6.H=p.H.......b=
 0900 700b02c0 22686241 f10a02c0 12883800  p..."hbA......8.
 0910 301b3800 401c483d 680a4801 ed094861  0.8.@.H=h.H...Ha
 0920 ed0a0000 483d0808 483d2809 6201f30a  ....H=..H=(.b...
 0930 04b0a203 00000000 483d2809 0000f872  ........H=(....r
 0940 961af892 0a1c6201 e30b02c0 22a81816  ......b....."...
 0950 c20b6261 f30c2600 5005623d 2c092600  ..ba..&.P.b=,.&.
 0960 b8034843 540a4843 6e09f892 0a1b483d  ..HCT.HCn.....H=
 0970 300c0000 000062c1 e60b02c0 22681896  0.....b....."h..
 0980 c00c6261 f20c2600 3003623d 8c0b2600  ..ba..&.0.b=..&.
 0990 c8044843 4c0a4843 3209483d 700b4861  ..HCL.HC2.H=p.Ha
 09a0 e30c0000 0000623d 700b02c0 22b86261  ......b=p...".ba
 09b0 e20a02c0 12183800 d81d3800 8818483d  ......8...8...H=
 09c0 680a4821 f6094821 f70a0000 483d0808  h.H!..H!....H=..
 09d0 483d2809 6221ec0a 04b0a203 00000000  H=(.b!..........
 09e0 623d2809 a68f1301 0000f872 9219f892  b=(........r....
 09f0 061c6221 f40b02c0 22481816 420c6221  ..b!...."H..B.b!
 0a00 ed0c2600 2002623d 2c092600 40044843  ..&. .b=,.&.@.HC
 0a10 480a4843 7009f892 061b483d 300c0000  H.HCp.....H=0...
 0a20 00006261 ef0b02c0 22581896 400b62e1  ..ba...."X..@.b.
 0a30 ec0c2600 a802623d 8c0b2600 30034843  ..&...b=..&.0.HC
 0a40 4a0a4843 2c09483d 700b4821 f50c0000  J.HC,.H=p.H!....
 0a50 0000623d 700b02c0 229862e1 f40a02c0  ..b=p...".b.....
 0a60 12a83800 c81c3800 501d483d 680a4841  ..8...8.P.H=h.HA
 0a70 f30948c1 f20a0000 483d0808 483d2809  ..H.....H=..H=(.
 0a80 6241eb0a 04b0a203 00000000 483d2809  bA..........H=(.
 0a90 0000f872 961df892 161c6241 e90b02c0  ...r......bA....
 0aa0 22781816 c20862c1 ea0c2600 b803623d  "x....b...&...b=
 0ab0 2c092600 88004843 4e0a4843 6209f892  ,.&...HCN.HCb...
 0ac0 161b483d 300c0000 00006221 f10b02c0  ..H=0.....b!....
 0ad0 22381896 c00a6201 eb0c2600 9801623d  "8....b...&...b=
 0ae0 8c0b2600 a8024843 460a4843 2a09483d  ..&...HCF.HC*.H=
 0af0 700b48c1 e80c0000 0000623d 700b02c0  p.H.......b=p...
 0b00 22686201 e90a02c0 12483800 301b3800  "hb......H8.0.8.
 0b10 201a483d 680a4881 ec0948a1 ec0a0000   .H=h.H...H.....
 0b20 483d0808 483d2809 4881e60a 00000000  H=..H=(.H.......
 0b30 483d2809 4881ee0a 00000000 483d2809  H=(.H.......H=(.
 0b40 48a1e60a 00000000 483d2809 48c1e20a  H.......H=(.H...
 0b50 00000000 483d2809 4821e60a 00000000  ....H=(.H!......
 0b60 483d2809 48a1ee0a 00000000 483d2809  H=(.H.......H=(.
 0b70 4821ee0a 00000000 483d2809 00000000  H!......H=(.....
 0b80 eb214000 00000000 005b0120 00f02c00  .!@......[. ..,.
 0b90 ba78a501 183206f0 2c00982c c8108401  .x...2..,..,....
 0ba0 40000020 00000000 00009806 1c0a0000  @.. ............
 0bb0 18002810 00000000 00000000 18001012  ..(.............
Contents of section .rela.text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_:
 0000 34000000 2a030000 00000000 3a000000  4...*.......:...
 0010 2a040000 00000000 9e0b0000 01020000  *...............
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
 0010 5f000000 00000000 00000000 0400f1ff  _...............
 0020 13010000 30000000 00000000 00000500  ....0...........
 0030 f1000000 b0000000 00000000 00000500  ................
 0040 1b010000 800b0000 00000000 00000500  ................
 0050 2c000000 00000000 d0000000 12000200  ,...............
 0060 c4000000 00000000 00000000 10000000  ................
 0070 e3000000 00000000 00000000 10000000  ................
 0080 cd000000 00000000 00000000 10000000  ................
 0090 d6000000 00000000 00000000 10000000  ................
 00a0 f9000000 d0000000 10000000 12000200  ................
 00b0 86000000 00000000 c00b0000 22000500  ............"...
 00c0 04010000 e0000000 30000000 12000200  ........0.......

Disassembly of section .text:

00000000 <test_float_operation>:
       0: b6 40 00 00 00 00 00 20 00 f0 2c 00  	nopa	;		nopb	;		jl	#0x0
			00000000:  R_AIE_4	__addsf3
       c: 00 00        	nop	
       e: c4 01 00 00 08 00    	paddxm	 [sp], #0x40
      14: 98 3d c4 0f  	st	 lr, [sp, #-60]
      18: 98 15 c1 0f  	st	 r8, [sp, #-64]
      1c: f8 a0 11 1a  	mov	r8, r3
      20: e1 00 00 40 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		jl	#0x0;		nopv	
			00000020:  R_AIE_0	__addsf3
      30: 18 00 00 10  	nopx	
      34: 00 00        	nop	
      36: 00 00        	nop	
      38: 00 00        	nop	
      3a: e4 41 28 b1 40 00    	or	 r1, r0, r0;		mov	r2, r8
      40: e1 00 00 40 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		jl	#0x0;		nopv	
			00000040:  R_AIE_0	__extendsfdf2
      50: 2c 00 00 f0 2c 00    	nopa	;		nopx	
      56: 00 00        	nop	
      58: 00 00        	nop	
      5a: 00 00        	nop	
      5c: f8 20 90 18  	mov	r2, r0
      60: ba 40 00 00 00 00 00 f0 2c 00	nopa	;		jl	#0x0
			00000060:  R_AIE_2	__adddf3
      6a: 00 00        	nop	
      6c: 00 00        	nop	
      6e: 44 3e 2a 82 eb 51    	movxm	r4, #0x51eb851f
      74: 44 70 bd 02 59 40    	movxm	r5, #0x40590eb8
      7a: e4 41 a1 b1 80 00    	or	 r2, r0, r0;		mov	r3, r1
      80: e1 00 00 40 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		jl	#0x0;		nopv	
			00000080:  R_AIE_0	__truncdfsf2
      90: 18 00 00 10  	nopx	
      94: 00 00        	nop	
      96: 00 00        	nop	
      98: 00 00        	nop	
      9a: e4 41 a0 b0 82 08    	or	 r2, r1, r1;		mov	r1, r0
      a0: e1 00 00 00 00 00 00 00 00 5b 01 20 00 20 87 f8      	lda	 lr, [sp, #-60];		nopb	;		nops	;		nopxm	;		nopv	
		...
      b8: 00 00        	nop	
      ba: 18 11 c1 07  	lda	 r8, [sp, #-64]
      be: 18 00 28 10  	ret	lr
      c2: 00 00        	nop	
      c4: 00 00        	nop	
      c6: 00 00        	nop	
      c8: c4 01 00 00 f8 ff    	paddxm	 [sp], #-0x40
      ce: 00 00        	nop	

000000d0 <mv_float32>:
      d0: 84 00 00 00 00 00    	j	#0x0
			000000d0:  R_AIE_1	_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_
		...
      de: 00 00        	nop	

000000e0 <zero_m_float32>:
      e0: 2c 00 00 00 00 00    	mova	r0, #0x0;		nopx	
      e6: f8 72 02 18  	vbcst.32	 x0, r0
      ea: 00 00        	nop	
      ec: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      f0: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      f4: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
      f8: 5c 00 50 50 85 03    	vst	 wl0, [p0], #0x20;		ret	lr
      fe: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
     102: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
     106: 98 2a 1c 08  	vst	 wl0, [p0], #0x20
     10a: 98 2a 04 08  	vst	 wl0, [p0, #0x0]
     10e: 00 00        	nop	

Disassembly of section .text._Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_:

00000000 <_Z14matVec_float32Iffu10__accfloatLj64ELj64ELj16EEvPT_S1_PT0_>:
       0: b6 78 a5 01 00 80 00 20 00 f0 2c 00  	nopa	;		nopb	;		event	#0;		nopm	
       c: 44 00 bf 30 00 00    	movxm	r1, #0x3f80
      12: ba 10 80 0f 3e 00 00 00 00 00	mova	r0, #0x0;		movxm	r16, #0xff00
      1c: ba 78 39 01 08 26 00 00 03 fe	mova	r3, #-0x10;		movx	r2, #0x30;		vbcst.32	 x0, r0
      26: ba 78 b9 82 88 00 00 00 81 07	mova	r1, #0x3c;		movx	r0, #0x4;		vbcst.16	 x2, r1

00000030 <.LBB2_1>:
      30: 18 00 70 1d  	add.nc	lc, r0, #0x0
      34: 44 00 e0 01 00 00    	movxm	ls, #0x0
			00000034:  R_AIE_42	.LBB2_2
      3a: 44 00 e0 06 00 00    	movxm	le, #0x0
			0000003a:  R_AIE_42	.L_LEnd0
      40: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      50: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      60: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      70: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      80: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      90: e1 00 00 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		nopv	
      a0: e1 00 00 78 60 b1 01 00 00 5b 01 20 00 b0 82 40      	vlda	 bmll0, [p2, #0x0];		nopb	;		nops	;		nopx	;		mov	p3, p1;		nopv	

000000b0 <.LBB2_2>:
      b0: 1c 00 00 80 a6 63    	vldb	 x4, [p3], #0x40;		nopx	
      b6: 00 00        	nop	
      b8: 00 00        	nop	
      ba: 00 00        	nop	
      bc: 98 95 1c 00  	vlda	 bmll1, [p0], #0x40
      c0: 00 00        	nop	
      c2: 00 00        	nop	
      c4: b8 81 13 19  	vextract.64	 r5:r4, x4, #0x0, vaddsign1
      c8: 00 00        	nop	
      ca: f8 72 12 1b  	vbcst.32	 x6, r4
      ce: f8 92 0c 1b  	vmov	bmll3, x6
      d2: 18 96 40 0c  	vconv.bf16.fp32	 wl8, bmll1
      d6: 18 96 41 0d  	vconv.bf16.fp32	 wl10, bmll3
      da: 38 00 c0 18  	vsel.32	 x1, x8, x0, r16
      de: 38 00 d0 19  	vsel.32	 x3, x10, x0, r16
      e2: 48 43 22 09  	vmsc.f	dm1, dm1, x1, x2, r1
      e6: 48 43 46 0a  	vmsc.f	dm2, dm2, x3, x2, r1
      ea: f8 92 0c 1a  	vmov	bmll2, x6
      ee: 00 00        	nop	
      f0: 00 00        	nop	
      f2: 00 00        	nop	
      f4: 18 96 c0 0a  	vconv.bf16.fp32	 wl5, bmll1
      f8: 18 16 c1 0b  	vconv.bf16.fp32	 wl7, bmll2
      fc: 38 00 a8 1c  	vsel.32	 x9, x5, x0, r16
     100: 38 00 b8 1d  	vsel.32	 x11, x7, x0, r16
     104: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     108: 48 43 56 0a  	vmsc.f	dm2, dm2, x11, x2, r1
		...
     114: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     118: 18 16 41 0c  	vconv.bf16.fp32	 wl8, bmll2
     11c: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     120: 38 00 40 1c  	vsel.32	 x8, x8, x0, r16
     124: 48 61 ed 0a  	vmul.f	dm2, x6, x11, r1
     128: 48 01 ed 09  	vmul.f	dm1, x6, x8, r1
     12c: 00 00        	nop	
     12e: 00 00        	nop	
     130: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     134: 62 01 f3 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x9, x8, r1
     13c: 00 00        	nop	
     13e: 00 00        	nop	
     140: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     144: 00 00        	nop	
     146: f8 72 96 1a  	vbcst.32	 x5, r5
     14a: f8 92 0a 1c  	vmov	bmll4, x5
     14e: 62 01 e3 0b 02 c0 22 a8      	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
     156: 18 16 c2 0b  	vconv.bf16.fp32	 wl7, bmll4
     15a: 62 61 f3 0c 26 00 50 05      	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
     162: 62 3d 2c 09 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     16a: 48 43 54 0a  	vmsc.f	dm2, dm2, x10, x2, r1
     16e: 48 43 6e 09  	vmsc.f	dm1, dm3, x7, x2, r1
     172: f8 92 0a 1b  	vmov	bmll3, x5
     176: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     17a: 00 00        	nop	
     17c: 00 00        	nop	
     17e: 62 c1 e6 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
     186: 18 96 c0 0c  	vconv.bf16.fp32	 wl9, bmll1
     18a: 62 61 f2 0c 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
     192: 62 3d 8c 0b 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     19a: 48 43 4c 0a  	vmsc.f	dm2, dm2, x6, x2, r1
     19e: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     1a2: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     1a6: 48 61 e3 0c  	vmul.f	dm4, x1, x11, r1
     1aa: 00 00        	nop	
     1ac: 00 00        	nop	
     1ae: 62 3d 70 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
     1b6: 62 61 e2 0a 02 c0 12 18      	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
     1be: 38 00 d8 1d  	vsel.32	 x11, x11, x0, r16
     1c2: 38 00 88 18  	vsel.32	 x1, x1, x0, r16
     1c6: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     1ca: 48 21 f6 09  	vmul.f	dm1, x11, x1, r1
     1ce: 48 21 f7 0a  	vmul.f	dm2, x11, x9, r1
     1d2: 00 00        	nop	
     1d4: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     1d8: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     1dc: 62 21 ec 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x6, x1, r1
     1e4: 00 00        	nop	
     1e6: 00 00        	nop	
     1e8: 62 3d 28 09 a6 83 13 01      	vextract.64	 r5:r4, x4, #0x1, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     1f0: 00 00        	nop	
     1f2: f8 72 12 1c  	vbcst.32	 x8, r4
     1f6: f8 92 10 1c  	vmov	bmll4, x8
     1fa: 62 21 f4 0b 02 c0 22 38      	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x10, x1, r1
     202: 18 16 c2 0a  	vconv.bf16.fp32	 wl5, bmll4
     206: 62 21 ed 0c 26 00 98 01      	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x6, x9, r1
     20e: 62 3d 2c 09 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     216: 48 43 46 0a  	vmsc.f	dm2, dm2, x3, x2, r1
     21a: 48 43 6a 09  	vmsc.f	dm1, dm3, x5, x2, r1
     21e: f8 92 10 1b  	vmov	bmll3, x8
     222: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     226: 00 00        	nop	
     228: 00 00        	nop	
     22a: 62 61 ef 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x7, x11, r1
     232: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     236: 62 e1 ec 0c 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x7, r1
     23e: 62 3d 8c 0b 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     246: 48 43 56 0a  	vmsc.f	dm2, dm2, x11, x2, r1
     24a: 48 43 2c 09  	vmsc.f	dm1, dm1, x6, x2, r1
     24e: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     252: 48 21 f5 0c  	vmul.f	dm4, x10, x9, r1
     256: 00 00        	nop	
     258: 00 00        	nop	
     25a: 62 3d 70 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
     262: 62 e1 f4 0a 02 c0 12 a8      	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
     26a: 38 00 c8 1c  	vsel.32	 x9, x9, x0, r16
     26e: 38 00 50 1d  	vsel.32	 x10, x10, x0, r16
     272: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     276: 48 41 f3 09  	vmul.f	dm1, x9, x10, r1
     27a: 48 c1 f2 0a  	vmul.f	dm2, x9, x6, r1
     27e: 00 00        	nop	
     280: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     284: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     288: 62 41 f7 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x11, x10, r1
     290: 00 00        	nop	
     292: 00 00        	nop	
     294: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     298: 00 00        	nop	
     29a: f8 72 96 18  	vbcst.32	 x1, r5
     29e: f8 92 02 1c  	vmov	bmll4, x1
     2a2: 62 41 e7 0b 02 c0 22 78      	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x3, x10, r1
     2aa: 18 16 42 0c  	vconv.bf16.fp32	 wl8, bmll4
     2ae: 62 c1 f6 0c 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x11, x6, r1
     2b6: 62 3d 2c 09 26 00 40 04      	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     2be: 48 43 4e 0a  	vmsc.f	dm2, dm2, x7, x2, r1
     2c2: 48 43 70 09  	vmsc.f	dm1, dm3, x8, x2, r1
     2c6: f8 92 02 1b  	vmov	bmll3, x1
     2ca: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     2ce: 00 00        	nop	
     2d0: 00 00        	nop	
     2d2: 62 21 eb 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x5, x9, r1
     2da: 18 96 c0 0d  	vconv.bf16.fp32	 wl11, bmll1
     2de: 62 a1 f6 0c 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x5, r1
     2e6: 62 3d 8c 0b 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     2ee: 48 43 52 0a  	vmsc.f	dm2, dm2, x9, x2, r1
     2f2: 48 43 36 09  	vmsc.f	dm1, dm1, x11, x2, r1
     2f6: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     2fa: 48 c1 e6 0c  	vmul.f	dm4, x3, x6, r1
     2fe: 00 00        	nop	
     300: 00 00        	nop	
     302: 62 3d 70 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
     30a: 62 a1 e6 0a 02 c0 12 38      	vconv.bf16.fp32	 wl3, bmll1;		vmul.f	dm2, x3, x5, r1
     312: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     316: 38 00 98 19  	vsel.32	 x3, x3, x0, r16
     31a: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     31e: 48 61 ec 09  	vmul.f	dm1, x6, x3, r1
     322: 48 61 ed 0a  	vmul.f	dm2, x6, x11, r1
     326: 00 00        	nop	
     328: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     32c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     330: 62 61 f2 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x9, x3, r1
     338: 00 00        	nop	
     33a: 00 00        	nop	
     33c: 62 3d 28 09 a6 85 13 01      	vextract.64	 r5:r4, x4, #0x2, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     344: 00 00        	nop	
     346: f8 72 12 1d  	vbcst.32	 x10, r4
     34a: f8 92 14 1c  	vmov	bmll4, x10
     34e: 62 61 ee 0b 02 c0 22 58      	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x3, r1
     356: 18 16 c2 08  	vconv.bf16.fp32	 wl1, bmll4
     35a: 62 61 f3 0c 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x9, x11, r1
     362: 62 3d 2c 09 26 00 88 00      	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     36a: 48 43 4a 0a  	vmsc.f	dm2, dm2, x5, x2, r1
     36e: 48 43 62 09  	vmsc.f	dm1, dm3, x1, x2, r1
     372: f8 92 14 1b  	vmov	bmll3, x10
     376: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     37a: 00 00        	nop	
     37c: 00 00        	nop	
     37e: 62 c1 f0 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x8, x6, r1
     386: 18 96 c0 0c  	vconv.bf16.fp32	 wl9, bmll1
     38a: 62 01 f3 0c 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x8, r1
     392: 62 3d 8c 0b 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     39a: 48 43 4c 0a  	vmsc.f	dm2, dm2, x6, x2, r1
     39e: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     3a2: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     3a6: 48 61 ef 0c  	vmul.f	dm4, x7, x11, r1
     3aa: 00 00        	nop	
     3ac: 00 00        	nop	
     3ae: 62 3d 70 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
     3b6: 62 01 ef 0a 02 c0 12 78      	vconv.bf16.fp32	 wl7, bmll1;		vmul.f	dm2, x7, x8, r1
     3be: 38 00 d8 1d  	vsel.32	 x11, x11, x0, r16
     3c2: 38 00 b8 1b  	vsel.32	 x7, x7, x0, r16
     3c6: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     3ca: 48 e1 f6 09  	vmul.f	dm1, x11, x7, r1
     3ce: 48 21 f7 0a  	vmul.f	dm2, x11, x9, r1
     3d2: 00 00        	nop	
     3d4: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     3d8: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     3dc: 62 e1 ec 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x6, x7, r1
     3e4: 00 00        	nop	
     3e6: 00 00        	nop	
     3e8: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     3ec: 00 00        	nop	
     3ee: f8 72 96 19  	vbcst.32	 x3, r5
     3f2: f8 92 06 1c  	vmov	bmll4, x3
     3f6: 62 e1 ea 0b 02 c0 22 88      	vconv.bf16.fp32	 wl8, bmll2;		vmul.f	dm3, x5, x7, r1
     3fe: 18 16 42 0d  	vconv.bf16.fp32	 wl10, bmll4
     402: 62 21 ed 0c 26 00 40 04      	vsel.32	 x8, x8, x0, r16;		vmul.f	dm4, x6, x9, r1
     40a: 62 3d 2c 09 26 00 50 05      	vsel.32	 x10, x10, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     412: 48 43 50 0a  	vmsc.f	dm2, dm2, x8, x2, r1
     416: 48 43 74 09  	vmsc.f	dm1, dm3, x10, x2, r1
     41a: f8 92 06 1b  	vmov	bmll3, x3
     41e: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     422: 00 00        	nop	
     424: 00 00        	nop	
     426: 62 61 e3 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x1, x11, r1
     42e: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     432: 62 21 ec 0c 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x1, r1
     43a: 62 3d 8c 0b 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     442: 48 43 56 0a  	vmsc.f	dm2, dm2, x11, x2, r1
     446: 48 43 2c 09  	vmsc.f	dm1, dm1, x6, x2, r1
     44a: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     44e: 48 21 eb 0c  	vmul.f	dm4, x5, x9, r1
     452: 00 00        	nop	
     454: 00 00        	nop	
     456: 62 3d 70 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
     45e: 62 21 ea 0a 02 c0 12 58      	vconv.bf16.fp32	 wl5, bmll1;		vmul.f	dm2, x5, x1, r1
     466: 38 00 c8 1c  	vsel.32	 x9, x9, x0, r16
     46a: 38 00 a8 1a  	vsel.32	 x5, x5, x0, r16
     46e: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     472: 48 a1 f2 09  	vmul.f	dm1, x9, x5, r1
     476: 48 c1 f2 0a  	vmul.f	dm2, x9, x6, r1
     47a: 00 00        	nop	
     47c: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     480: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     484: 62 a1 f6 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x11, x5, r1
     48c: 00 00        	nop	
     48e: 00 00        	nop	
     490: 62 3d 28 09 a6 87 13 01      	vextract.64	 r5:r4, x4, #0x3, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     498: 00 00        	nop	
     49a: f8 72 92 1b  	vbcst.32	 x7, r4
     49e: f8 92 0e 1c  	vmov	bmll4, x7
     4a2: 62 a1 f0 0b 02 c0 22 18      	vconv.bf16.fp32	 wl1, bmll2;		vmul.f	dm3, x8, x5, r1
     4aa: 18 16 c2 09  	vconv.bf16.fp32	 wl3, bmll4
     4ae: 62 c1 f6 0c 26 00 88 00      	vsel.32	 x1, x1, x0, r16;		vmul.f	dm4, x11, x6, r1
     4b6: 62 3d 2c 09 26 00 98 01      	vsel.32	 x3, x3, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     4be: 48 43 42 0a  	vmsc.f	dm2, dm2, x1, x2, r1
     4c2: 48 43 66 09  	vmsc.f	dm1, dm3, x3, x2, r1
     4c6: f8 92 0e 1b  	vmov	bmll3, x7
     4ca: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     4ce: 00 00        	nop	
     4d0: 00 00        	nop	
     4d2: 62 21 f5 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x10, x9, r1
     4da: 18 96 c0 0d  	vconv.bf16.fp32	 wl11, bmll1
     4de: 62 41 f7 0c 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x10, r1
     4e6: 62 3d 8c 0b 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     4ee: 48 43 52 0a  	vmsc.f	dm2, dm2, x9, x2, r1
     4f2: 48 43 36 09  	vmsc.f	dm1, dm1, x11, x2, r1
     4f6: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     4fa: 48 c1 f0 0c  	vmul.f	dm4, x8, x6, r1
     4fe: 00 00        	nop	
     500: 00 00        	nop	
     502: 62 3d 70 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
     50a: 62 41 f1 0a 02 c0 12 88      	vconv.bf16.fp32	 wl8, bmll1;		vmul.f	dm2, x8, x10, r1
     512: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     516: 38 00 40 1c  	vsel.32	 x8, x8, x0, r16
     51a: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     51e: 48 01 ed 09  	vmul.f	dm1, x6, x8, r1
     522: 48 61 ed 0a  	vmul.f	dm2, x6, x11, r1
     526: 00 00        	nop	
     528: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     52c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     530: 62 01 f3 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x9, x8, r1
     538: 00 00        	nop	
     53a: 00 00        	nop	
     53c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     540: 00 00        	nop	
     542: f8 72 96 1a  	vbcst.32	 x5, r5
     546: f8 92 0a 1c  	vmov	bmll4, x5
     54a: 62 01 e3 0b 02 c0 22 a8      	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
     552: 18 16 c2 0b  	vconv.bf16.fp32	 wl7, bmll4
     556: 62 61 f3 0c 26 00 50 05      	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
     55e: 62 3d 2c 09 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     566: 48 43 54 0a  	vmsc.f	dm2, dm2, x10, x2, r1
     56a: 48 43 6e 09  	vmsc.f	dm1, dm3, x7, x2, r1
     56e: f8 92 0a 1b  	vmov	bmll3, x5
     572: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     576: 00 00        	nop	
     578: 00 00        	nop	
     57a: 62 c1 e6 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
     582: 18 96 c0 0c  	vconv.bf16.fp32	 wl9, bmll1
     586: 62 61 f2 0c 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
     58e: 62 3d 8c 0b 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     596: 48 43 4c 0a  	vmsc.f	dm2, dm2, x6, x2, r1
     59a: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     59e: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     5a2: 48 61 e3 0c  	vmul.f	dm4, x1, x11, r1
     5a6: 00 00        	nop	
     5a8: 00 00        	nop	
     5aa: 62 3d 70 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
     5b2: 62 61 e2 0a 02 c0 12 18      	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
     5ba: 38 00 d8 1d  	vsel.32	 x11, x11, x0, r16
     5be: 38 00 88 18  	vsel.32	 x1, x1, x0, r16
     5c2: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     5c6: 48 21 f6 09  	vmul.f	dm1, x11, x1, r1
     5ca: 48 21 f7 0a  	vmul.f	dm2, x11, x9, r1
     5ce: 00 00        	nop	
     5d0: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     5d4: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     5d8: 62 21 ec 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x6, x1, r1
     5e0: 00 00        	nop	
     5e2: 00 00        	nop	
     5e4: 62 3d 28 09 a6 89 13 01      	vextract.64	 r5:r4, x4, #0x4, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     5ec: 00 00        	nop	
     5ee: f8 72 12 1c  	vbcst.32	 x8, r4
     5f2: f8 92 10 1c  	vmov	bmll4, x8
     5f6: 62 21 f4 0b 02 c0 22 38      	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x10, x1, r1
     5fe: 18 16 c2 0a  	vconv.bf16.fp32	 wl5, bmll4
     602: 62 21 ed 0c 26 00 98 01      	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x6, x9, r1
     60a: 62 3d 2c 09 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     612: 48 43 46 0a  	vmsc.f	dm2, dm2, x3, x2, r1
     616: 48 43 6a 09  	vmsc.f	dm1, dm3, x5, x2, r1
     61a: f8 92 10 1b  	vmov	bmll3, x8
     61e: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     622: 00 00        	nop	
     624: 00 00        	nop	
     626: 62 61 ef 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x7, x11, r1
     62e: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     632: 62 e1 ec 0c 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x7, r1
     63a: 62 3d 8c 0b 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     642: 48 43 56 0a  	vmsc.f	dm2, dm2, x11, x2, r1
     646: 48 43 2c 09  	vmsc.f	dm1, dm1, x6, x2, r1
     64a: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     64e: 48 21 f5 0c  	vmul.f	dm4, x10, x9, r1
     652: 00 00        	nop	
     654: 00 00        	nop	
     656: 62 3d 70 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
     65e: 62 e1 f4 0a 02 c0 12 a8      	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
     666: 38 00 c8 1c  	vsel.32	 x9, x9, x0, r16
     66a: 38 00 50 1d  	vsel.32	 x10, x10, x0, r16
     66e: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     672: 48 41 f3 09  	vmul.f	dm1, x9, x10, r1
     676: 48 c1 f2 0a  	vmul.f	dm2, x9, x6, r1
     67a: 00 00        	nop	
     67c: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     680: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     684: 62 41 f7 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x11, x10, r1
     68c: 00 00        	nop	
     68e: 00 00        	nop	
     690: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     694: 00 00        	nop	
     696: f8 72 96 18  	vbcst.32	 x1, r5
     69a: f8 92 02 1c  	vmov	bmll4, x1
     69e: 62 41 e7 0b 02 c0 22 78      	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x3, x10, r1
     6a6: 18 16 42 0c  	vconv.bf16.fp32	 wl8, bmll4
     6aa: 62 c1 f6 0c 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x11, x6, r1
     6b2: 62 3d 2c 09 26 00 40 04      	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     6ba: 48 43 4e 0a  	vmsc.f	dm2, dm2, x7, x2, r1
     6be: 48 43 70 09  	vmsc.f	dm1, dm3, x8, x2, r1
     6c2: f8 92 02 1b  	vmov	bmll3, x1
     6c6: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     6ca: 00 00        	nop	
     6cc: 00 00        	nop	
     6ce: 62 21 eb 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x5, x9, r1
     6d6: 18 96 c0 0d  	vconv.bf16.fp32	 wl11, bmll1
     6da: 62 a1 f6 0c 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x5, r1
     6e2: 62 3d 8c 0b 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     6ea: 48 43 52 0a  	vmsc.f	dm2, dm2, x9, x2, r1
     6ee: 48 43 36 09  	vmsc.f	dm1, dm1, x11, x2, r1
     6f2: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     6f6: 48 c1 e6 0c  	vmul.f	dm4, x3, x6, r1
     6fa: 00 00        	nop	
     6fc: 00 00        	nop	
     6fe: 62 3d 70 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
     706: 62 a1 e6 0a 02 c0 12 38      	vconv.bf16.fp32	 wl3, bmll1;		vmul.f	dm2, x3, x5, r1
     70e: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     712: 38 00 98 19  	vsel.32	 x3, x3, x0, r16
     716: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     71a: 48 61 ec 09  	vmul.f	dm1, x6, x3, r1
     71e: 48 61 ed 0a  	vmul.f	dm2, x6, x11, r1
     722: 00 00        	nop	
     724: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     728: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     72c: 62 61 f2 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x9, x3, r1
     734: 00 00        	nop	
     736: 00 00        	nop	
     738: 62 3d 28 09 a6 8b 13 01      	vextract.64	 r5:r4, x4, #0x5, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     740: 00 00        	nop	
     742: f8 72 12 1d  	vbcst.32	 x10, r4
     746: f8 92 14 1c  	vmov	bmll4, x10
     74a: 62 61 ee 0b 02 c0 22 58      	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x3, r1
     752: 18 16 c2 08  	vconv.bf16.fp32	 wl1, bmll4
     756: 62 61 f3 0c 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x9, x11, r1
     75e: 62 3d 2c 09 26 00 88 00      	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     766: 48 43 4a 0a  	vmsc.f	dm2, dm2, x5, x2, r1
     76a: 48 43 62 09  	vmsc.f	dm1, dm3, x1, x2, r1
     76e: f8 92 14 1b  	vmov	bmll3, x10
     772: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     776: 00 00        	nop	
     778: 00 00        	nop	
     77a: 62 c1 f0 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x8, x6, r1
     782: 18 96 c0 0c  	vconv.bf16.fp32	 wl9, bmll1
     786: 62 01 f3 0c 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x8, r1
     78e: 62 3d 8c 0b 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     796: 48 43 4c 0a  	vmsc.f	dm2, dm2, x6, x2, r1
     79a: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     79e: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     7a2: 48 61 ef 0c  	vmul.f	dm4, x7, x11, r1
     7a6: 00 00        	nop	
     7a8: 00 00        	nop	
     7aa: 62 3d 70 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
     7b2: 62 01 ef 0a 02 c0 12 78      	vconv.bf16.fp32	 wl7, bmll1;		vmul.f	dm2, x7, x8, r1
     7ba: 38 00 d8 1d  	vsel.32	 x11, x11, x0, r16
     7be: 38 00 b8 1b  	vsel.32	 x7, x7, x0, r16
     7c2: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     7c6: 48 e1 f6 09  	vmul.f	dm1, x11, x7, r1
     7ca: 48 21 f7 0a  	vmul.f	dm2, x11, x9, r1
     7ce: 00 00        	nop	
     7d0: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     7d4: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     7d8: 62 e1 ec 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x6, x7, r1
     7e0: 00 00        	nop	
     7e2: 00 00        	nop	
     7e4: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     7e8: 00 00        	nop	
     7ea: f8 72 96 19  	vbcst.32	 x3, r5
     7ee: f8 92 06 1c  	vmov	bmll4, x3
     7f2: 62 e1 ea 0b 02 c0 22 88      	vconv.bf16.fp32	 wl8, bmll2;		vmul.f	dm3, x5, x7, r1
     7fa: 18 16 42 0d  	vconv.bf16.fp32	 wl10, bmll4
     7fe: 62 21 ed 0c 26 00 40 04      	vsel.32	 x8, x8, x0, r16;		vmul.f	dm4, x6, x9, r1
     806: 62 3d 2c 09 26 00 50 05      	vsel.32	 x10, x10, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     80e: 48 43 50 0a  	vmsc.f	dm2, dm2, x8, x2, r1
     812: 48 43 74 09  	vmsc.f	dm1, dm3, x10, x2, r1
     816: f8 92 06 1b  	vmov	bmll3, x3
     81a: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     81e: 00 00        	nop	
     820: 00 00        	nop	
     822: 62 61 e3 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vmul.f	dm3, x1, x11, r1
     82a: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     82e: 62 21 ec 0c 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vmul.f	dm4, x6, x1, r1
     836: 62 3d 8c 0b 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     83e: 48 43 56 0a  	vmsc.f	dm2, dm2, x11, x2, r1
     842: 48 43 2c 09  	vmsc.f	dm1, dm1, x6, x2, r1
     846: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     84a: 48 21 eb 0c  	vmul.f	dm4, x5, x9, r1
     84e: 00 00        	nop	
     850: 00 00        	nop	
     852: 62 3d 70 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
     85a: 62 21 ea 0a 02 c0 12 58      	vconv.bf16.fp32	 wl5, bmll1;		vmul.f	dm2, x5, x1, r1
     862: 38 00 c8 1c  	vsel.32	 x9, x9, x0, r16
     866: 38 00 a8 1a  	vsel.32	 x5, x5, x0, r16
     86a: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     86e: 48 a1 f2 09  	vmul.f	dm1, x9, x5, r1
     872: 48 c1 f2 0a  	vmul.f	dm2, x9, x6, r1
     876: 00 00        	nop	
     878: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     87c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     880: 62 a1 f6 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x11, x5, r1
     888: 00 00        	nop	
     88a: 00 00        	nop	
     88c: 62 3d 28 09 a6 8d 13 01      	vextract.64	 r5:r4, x4, #0x6, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     894: 00 00        	nop	
     896: f8 72 92 1b  	vbcst.32	 x7, r4
     89a: f8 92 0e 1c  	vmov	bmll4, x7
     89e: 62 a1 f0 0b 02 c0 22 18      	vconv.bf16.fp32	 wl1, bmll2;		vmul.f	dm3, x8, x5, r1
     8a6: 18 16 c2 09  	vconv.bf16.fp32	 wl3, bmll4
     8aa: 62 c1 f6 0c 26 00 88 00      	vsel.32	 x1, x1, x0, r16;		vmul.f	dm4, x11, x6, r1
     8b2: 62 3d 2c 09 26 00 98 01      	vsel.32	 x3, x3, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     8ba: 48 43 42 0a  	vmsc.f	dm2, dm2, x1, x2, r1
     8be: 48 43 66 09  	vmsc.f	dm1, dm3, x3, x2, r1
     8c2: f8 92 0e 1b  	vmov	bmll3, x7
     8c6: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     8ca: 00 00        	nop	
     8cc: 00 00        	nop	
     8ce: 62 21 f5 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vmul.f	dm3, x10, x9, r1
     8d6: 18 96 c0 0d  	vconv.bf16.fp32	 wl11, bmll1
     8da: 62 41 f7 0c 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vmul.f	dm4, x11, x10, r1
     8e2: 62 3d 8c 0b 26 00 d8 05      	vsel.32	 x11, x11, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     8ea: 48 43 52 0a  	vmsc.f	dm2, dm2, x9, x2, r1
     8ee: 48 43 36 09  	vmsc.f	dm1, dm1, x11, x2, r1
     8f2: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     8f6: 48 c1 f0 0c  	vmul.f	dm4, x8, x6, r1
     8fa: 00 00        	nop	
     8fc: 00 00        	nop	
     8fe: 62 3d 70 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
     906: 62 41 f1 0a 02 c0 12 88      	vconv.bf16.fp32	 wl8, bmll1;		vmul.f	dm2, x8, x10, r1
     90e: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     912: 38 00 40 1c  	vsel.32	 x8, x8, x0, r16
     916: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     91a: 48 01 ed 09  	vmul.f	dm1, x6, x8, r1
     91e: 48 61 ed 0a  	vmul.f	dm2, x6, x11, r1
     922: 00 00        	nop	
     924: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     928: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     92c: 62 01 f3 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x9, x8, r1
     934: 00 00        	nop	
     936: 00 00        	nop	
     938: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     93c: 00 00        	nop	
     93e: f8 72 96 1a  	vbcst.32	 x5, r5
     942: f8 92 0a 1c  	vmov	bmll4, x5
     946: 62 01 e3 0b 02 c0 22 a8      	vconv.bf16.fp32	 wl10, bmll2;		vmul.f	dm3, x1, x8, r1
     94e: 18 16 c2 0b  	vconv.bf16.fp32	 wl7, bmll4
     952: 62 61 f3 0c 26 00 50 05      	vsel.32	 x10, x10, x0, r16;		vmul.f	dm4, x9, x11, r1
     95a: 62 3d 2c 09 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     962: 48 43 54 0a  	vmsc.f	dm2, dm2, x10, x2, r1
     966: 48 43 6e 09  	vmsc.f	dm1, dm3, x7, x2, r1
     96a: f8 92 0a 1b  	vmov	bmll3, x5
     96e: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     972: 00 00        	nop	
     974: 00 00        	nop	
     976: 62 c1 e6 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vmul.f	dm3, x3, x6, r1
     97e: 18 96 c0 0c  	vconv.bf16.fp32	 wl9, bmll1
     982: 62 61 f2 0c 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vmul.f	dm4, x9, x3, r1
     98a: 62 3d 8c 0b 26 00 c8 04      	vsel.32	 x9, x9, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     992: 48 43 4c 0a  	vmsc.f	dm2, dm2, x6, x2, r1
     996: 48 43 32 09  	vmsc.f	dm1, dm1, x9, x2, r1
     99a: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     99e: 48 61 e3 0c  	vmul.f	dm4, x1, x11, r1
     9a2: 00 00        	nop	
     9a4: 00 00        	nop	
     9a6: 62 3d 70 0b 02 c0 22 b8      	vconv.bf16.fp32	 wl11, bmll2;		vadd.f	dm3, dm3, dm4, r1
     9ae: 62 61 e2 0a 02 c0 12 18      	vconv.bf16.fp32	 wl1, bmll1;		vmul.f	dm2, x1, x3, r1
     9b6: 38 00 d8 1d  	vsel.32	 x11, x11, x0, r16
     9ba: 38 00 88 18  	vsel.32	 x1, x1, x0, r16
     9be: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     9c2: 48 21 f6 09  	vmul.f	dm1, x11, x1, r1
     9c6: 48 21 f7 0a  	vmul.f	dm2, x11, x9, r1
     9ca: 00 00        	nop	
     9cc: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     9d0: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     9d4: 62 21 ec 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x6, x1, r1
     9dc: 00 00        	nop	
     9de: 00 00        	nop	
     9e0: 62 3d 28 09 a6 8f 13 01      	vextract.64	 r5:r4, x4, #0x7, vaddsign1;		vadd.f	dm1, dm1, dm2, r1
     9e8: 00 00        	nop	
     9ea: f8 72 92 19  	vbcst.32	 x3, r4
     9ee: f8 92 06 1c  	vmov	bmll4, x3
     9f2: 62 21 f4 0b 02 c0 22 48      	vconv.bf16.fp32	 wl4, bmll2;		vmul.f	dm3, x10, x1, r1
     9fa: 18 16 42 0c  	vconv.bf16.fp32	 wl8, bmll4
     9fe: 62 21 ed 0c 26 00 20 02      	vsel.32	 x4, x4, x0, r16;		vmul.f	dm4, x6, x9, r1
     a06: 62 3d 2c 09 26 00 40 04      	vsel.32	 x8, x8, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     a0e: 48 43 48 0a  	vmsc.f	dm2, dm2, x4, x2, r1
     a12: 48 43 70 09  	vmsc.f	dm1, dm3, x8, x2, r1
     a16: f8 92 06 1b  	vmov	bmll3, x3
     a1a: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     a1e: 00 00        	nop	
     a20: 00 00        	nop	
     a22: 62 61 ef 0b 02 c0 22 58      	vconv.bf16.fp32	 wl5, bmll2;		vmul.f	dm3, x7, x11, r1
     a2a: 18 96 40 0b  	vconv.bf16.fp32	 wl6, bmll1
     a2e: 62 e1 ec 0c 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vmul.f	dm4, x6, x7, r1
     a36: 62 3d 8c 0b 26 00 30 03      	vsel.32	 x6, x6, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     a3e: 48 43 4a 0a  	vmsc.f	dm2, dm2, x5, x2, r1
     a42: 48 43 2c 09  	vmsc.f	dm1, dm1, x6, x2, r1
     a46: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     a4a: 48 21 f5 0c  	vmul.f	dm4, x10, x9, r1
     a4e: 00 00        	nop	
     a50: 00 00        	nop	
     a52: 62 3d 70 0b 02 c0 22 98      	vconv.bf16.fp32	 wl9, bmll2;		vadd.f	dm3, dm3, dm4, r1
     a5a: 62 e1 f4 0a 02 c0 12 a8      	vconv.bf16.fp32	 wl10, bmll1;		vmul.f	dm2, x10, x7, r1
     a62: 38 00 c8 1c  	vsel.32	 x9, x9, x0, r16
     a66: 38 00 50 1d  	vsel.32	 x10, x10, x0, r16
     a6a: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     a6e: 48 41 f3 09  	vmul.f	dm1, x9, x10, r1
     a72: 48 c1 f2 0a  	vmul.f	dm2, x9, x6, r1
     a76: 00 00        	nop	
     a78: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     a7c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     a80: 62 41 eb 0a 04 b0 a2 03      	vlda	 bmll2, [p0], #0x40;		vmul.f	dm2, x5, x10, r1
     a88: 00 00        	nop	
     a8a: 00 00        	nop	
     a8c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     a90: 00 00        	nop	
     a92: f8 72 96 1d  	vbcst.32	 x11, r5
     a96: f8 92 16 1c  	vmov	bmll4, x11
     a9a: 62 41 e9 0b 02 c0 22 78      	vconv.bf16.fp32	 wl7, bmll2;		vmul.f	dm3, x4, x10, r1
     aa2: 18 16 c2 08  	vconv.bf16.fp32	 wl1, bmll4
     aa6: 62 c1 ea 0c 26 00 b8 03      	vsel.32	 x7, x7, x0, r16;		vmul.f	dm4, x5, x6, r1
     aae: 62 3d 2c 09 26 00 88 00      	vsel.32	 x1, x1, x0, r16;		vadd.f	dm1, dm1, dm3, r1
     ab6: 48 43 4e 0a  	vmsc.f	dm2, dm2, x7, x2, r1
     aba: 48 43 62 09  	vmsc.f	dm1, dm3, x1, x2, r1
     abe: f8 92 16 1b  	vmov	bmll3, x11
     ac2: 48 3d 30 0c  	vadd.f	dm4, dm1, dm4, r1
     ac6: 00 00        	nop	
     ac8: 00 00        	nop	
     aca: 62 21 f1 0b 02 c0 22 38      	vconv.bf16.fp32	 wl3, bmll2;		vmul.f	dm3, x8, x9, r1
     ad2: 18 96 c0 0a  	vconv.bf16.fp32	 wl5, bmll1
     ad6: 62 01 eb 0c 26 00 98 01      	vsel.32	 x3, x3, x0, r16;		vmul.f	dm4, x5, x8, r1
     ade: 62 3d 8c 0b 26 00 a8 02      	vsel.32	 x5, x5, x0, r16;		vadd.f	dm3, dm4, dm3, r1
     ae6: 48 43 46 0a  	vmsc.f	dm2, dm2, x3, x2, r1
     aea: 48 43 2a 09  	vmsc.f	dm1, dm1, x5, x2, r1
     aee: 48 3d 70 0b  	vadd.f	dm3, dm3, dm4, r1
     af2: 48 c1 e8 0c  	vmul.f	dm4, x4, x6, r1
     af6: 00 00        	nop	
     af8: 00 00        	nop	
     afa: 62 3d 70 0b 02 c0 22 68      	vconv.bf16.fp32	 wl6, bmll2;		vadd.f	dm3, dm3, dm4, r1
     b02: 62 01 e9 0a 02 c0 12 48      	vconv.bf16.fp32	 wl4, bmll1;		vmul.f	dm2, x4, x8, r1
     b0a: 38 00 30 1b  	vsel.32	 x6, x6, x0, r16
     b0e: 38 00 20 1a  	vsel.32	 x4, x4, x0, r16
     b12: 48 3d 68 0a  	vadd.f	dm2, dm3, dm2, r1
     b16: 48 81 ec 09  	vmul.f	dm1, x6, x4, r1
     b1a: 48 a1 ec 0a  	vmul.f	dm2, x6, x5, r1
     b1e: 00 00        	nop	
     b20: 48 3d 08 08  	vadd.f	dm0, dm0, dm2, r1
     b24: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b28: 48 81 e6 0a  	vmul.f	dm2, x3, x4, r1
     b2c: 00 00        	nop	
     b2e: 00 00        	nop	
     b30: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b34: 48 81 ee 0a  	vmul.f	dm2, x7, x4, r1
     b38: 00 00        	nop	
     b3a: 00 00        	nop	
     b3c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b40: 48 a1 e6 0a  	vmul.f	dm2, x3, x5, r1
     b44: 00 00        	nop	
     b46: 00 00        	nop	
     b48: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b4c: 48 c1 e2 0a  	vmul.f	dm2, x1, x6, r1
     b50: 00 00        	nop	
     b52: 00 00        	nop	
     b54: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b58: 48 21 e6 0a  	vmul.f	dm2, x3, x1, r1
     b5c: 00 00        	nop	
     b5e: 00 00        	nop	
     b60: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b64: 48 a1 ee 0a  	vmul.f	dm2, x7, x5, r1
     b68: 00 00        	nop	
     b6a: 00 00        	nop	
     b6c: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b70: 48 21 ee 0a  	vmul.f	dm2, x7, x1, r1
     b74: 00 00        	nop	
     b76: 00 00        	nop	
     b78: 48 3d 28 09  	vadd.f	dm1, dm1, dm2, r1
     b7c: 00 00        	nop	
     b7e: 00 00        	nop	

00000b80 <.L_LEnd0>:
     b80: eb 21 40 00 00 00 00 00 00 5b 01 20 00 f0 2c 00      	nopa	;		nopb	;		nops	;		nopxm	;		vadd.f	dm0, dm0, dm1, r1
     b90: ba 78 a5 01 18 32 06 f0 2c 00	nopa	;		add	r3, r3, #0x10;		nopm	
     b9a: 98 2c c8 10  	ltu	 r4, r3, r2
     b9e: 84 01 40 00 00 20    	jnz	 r4, #0x0
			00000b9e:  R_AIE_1	.LBB2_1
     ba4: 00 00        	nop	
     ba6: 00 00        	nop	
     ba8: 00 00        	nop	
     baa: 98 06 1c 0a  	vst	 bmll0, [p2], #0x40
     bae: 00 00        	nop	
     bb0: 18 00 28 10  	ret	lr
		...
     bbc: 18 00 10 12  	event	#1
