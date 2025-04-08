/*
 * Implementation file for: Full-bridge-llc-hil/Subsystem
 * Generated with         : PLECS 4.9.2
 * Generated on           : 8 Apr 2025 13:11:15
 */
#include "Subsystem.h"
#ifndef PLECS_HEADER_Subsystem_h_
#error The wrong header file "Subsystem.h" was included. Please check your
#error include path to see whether this file name conflicts with the name
#error of another header file.
#endif /* PLECS_HEADER_Subsystem_h_ */
#if defined(__GNUC__) && (__GNUC__ > 4)
#   define _ALIGNMENT 16
#   define _RESTRICT __restrict
#   define _ALIGN __attribute__((aligned(_ALIGNMENT)))
#   if defined(__clang__)
#      if __has_builtin(__builtin_assume_aligned)
#         define _ASSUME_ALIGNED(a) __builtin_assume_aligned(a, _ALIGNMENT)
#      else
#         define _ASSUME_ALIGNED(a) a
#      endif
#   else
#      define _ASSUME_ALIGNED(a) __builtin_assume_aligned(a, _ALIGNMENT)
#   endif
#else
#   ifndef _RESTRICT
#      define _RESTRICT
#   endif
#   ifndef _ALIGN
#      define _ALIGN
#   endif
#   ifndef _ASSUME_ALIGNED
#      define _ASSUME_ALIGNED(a) a
#   endif
#endif
#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#define PLECSRunTimeError(msg) Subsystem_errorStatus = msg
#define Subsystem_UNCONNECTED 0
static float * _RESTRICT Subsystem_PM0_x;
static float Subsystem_PM0_tmpX[6] _ALIGN;
static float Subsystem_PM0_prevX[6] _ALIGN;
static float Subsystem_PM0_u[1] _ALIGN;
static float Subsystem_PM0_prevU[1] _ALIGN;
static float Subsystem_PM0_y[12] _ALIGN;
static float Subsystem_PM0_gateSignalBuffer[2] _ALIGN;
static size_t Subsystem_PM0_topoIdx;
static char Subsystem_PM0_withDiracs;
static const size_t PM0_Ad_0_rowPtr[] = {
   0,0,1,2,3,4,4
};
static const size_t PM0_Ad_0_colIdx[] = {
   1,2,4,4
};
static const float PM0_Ad_0_data[] _ALIGN = {
   1.f,0.998667555f,-5.f,1.f
};
static const size_t PM0_Bd0_0_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_0_colIdx[] = {
   0
};
static const float PM0_Bd0_0_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_0_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_0_colIdx[] = {
   0
};
static const float PM0_Bd1_0_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_0_rowPtr[] = {
   0,1,1,1,1,1,2,3,4,5,5,6
};
static const size_t PM0_C_0_0_colIdx[] = {
   2,2,2,2,2,2
};
static const float PM0_C_0_0_data[] _ALIGN = {
   1.f,-0.5f,-0.5f,-0.5f,-0.5f,4.f
};
static const size_t PM0_D_0_0_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_0_colIdx[] = {
   0
};
static const float PM0_D_0_0_data[] _ALIGN = {
   0
};
static void PM0_collision_0()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.2f*x[3];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = 0.;
}
static size_t PM0_natPreComm_0_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 0; /* 0_0 */
}
static size_t PM0_natPostComm_0_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 0; /* 0_0 */
}
static size_t PM0_forcedComm_0_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 0; /* 0_0 */
      }
      else
      {
         if (x[2] >= 0)
         {
            if (x[1]-20.7070707f*x[2]-u[0] > 0)
            {
               return 5; /* 105_0 */
            }
            if (-x[1]-20.7070707f*x[2]+u[0] > 0)
            {
               return 8; /* 153_0 */
            }
         }
         if (-x[1]+20.7070707f*x[2]+u[0] >= 0)
         {
            if (x[1]+20.7070707f*x[2]-u[0] >= 0)
            {
               return 2; /* 9_0 */
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         {
            const char cond2 = -x[1]+20.7070707f*x[2]-u[0] >= 0;
            if (cond2)
            {
               if (x[1]+20.7070707f*x[2]+u[0] >= 0)
               {
                  return 1; /* 6_0 */
               }
            }
            else if (!cond2)
            {
               if (x[2] >= 0)
               {
                  return 4; /* 102_0 */
               }
            }
            if (-x[1]-20.7070707f*x[2]-u[0] > 0)
            {
               if (x[2] >= 0)
               {
                  return 7; /* 150_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 0_0";
   return 0; /* 0_0 */
}
static const size_t PM0_Ad_6_rowPtr[] = {
   0,3,6,7,8,11,11
};
static const size_t PM0_Ad_6_colIdx[] = {
   1,3,4,1,3,4,2,3,1,3,4
};
static const float PM0_Ad_6_data[] _ALIGN = {
   -0.00404967509f,0.988689109f,4.94344555f,0.988729606f,5.53455595f,
   27.6727797f,0.998667555f,1.f,-0.000809935017f,-0.00226217811f,0.988689109f
};
static const size_t PM0_Bd0_6_rowPtr[] = {
   0,1,2,2,2,3,3
};
static const size_t PM0_Bd0_6_colIdx[] = {
   0,0,0
};
static const float PM0_Bd0_6_data[] _ALIGN = {
   -0.00202100421f,-0.00751075143f,-0.000404200841f
};
static const size_t PM0_Bd1_6_rowPtr[] = {
   0,1,2,2,2,3,3
};
static const size_t PM0_Bd1_6_colIdx[] = {
   0,0,0
};
static const float PM0_Bd1_6_data[] _ALIGN = {
   -0.00202867088f,-0.00375964234f,-0.000405734176f
};
static const size_t PM0_C_0_6_rowPtr[] = {
   0,1,1,1,1,1,5,9,13,17,19,20
};
static const size_t PM0_C_0_6_colIdx[] = {
   2,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,3,4,2
};
static const float PM0_C_0_6_data[] _ALIGN = {
   1.f,-0.0241463415f,-0.5f,-0.000241463415f,-0.00120731707f,0.0241463415f,
   -0.5f,0.000241463415f,0.00120731707f,0.0241463415f,-0.5f,0.000241463415f,
   0.00120731707f,-0.0241463415f,-0.5f,-0.000241463415f,-0.00120731707f,1.f,
   5.f,4.f
};
static const size_t PM0_D_0_6_rowPtr[] = {
   0,0,0,0,0,0,1,2,3,4,4,4
};
static const size_t PM0_D_0_6_colIdx[] = {
   0,0,0,0
};
static const float PM0_D_0_6_data[] _ALIGN = {
   -0.0241463415f,0.0241463415f,0.0241463415f,-0.0241463415f
};
static void PM0_collision_6()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.0243902439f*x[0]+0.975609756f*x[3]+4.87804878f*x[4]+
             0.241463415f*x[5];
   tmpX[4] = 0.00487804878f*x[0]-0.00487804878f*x[3]+0.975609756f*x[4]+
             0.0482926829f*x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
}
static size_t PM0_natPreComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 1; /* 6_0 */
}
static size_t PM0_natPostComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (1.f*x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
          x[5]+4100.f*u[0] > 0)
      {
         return 4; /* 102_0 */
      }
      if (-1.f*x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
          x[5]-4100.f*u[0] > 0)
      {
         return 7; /* 150_0 */
      }
   }
   return 1; /* 6_0 */
}
static size_t PM0_forcedComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 1; /* 6_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         {
            const char cond2 = -x[0]-4100.f*x[1]+84898.9899f*x[2]-40.f*x[3]-
                               200.f*x[4]-9.9f*x[5]+4100.f*u[0] >= 0;
            if (cond2)
            {
               if (x[0]+4100.f*x[1]+84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+
                   9.9f*x[5]-4100.f*u[0] >= 0)
               {
                  return 2; /* 9_0 */
               }
            }
            else if (!cond2)
            {
               if (x[2] >= 0)
               {
                  return 5; /* 105_0 */
               }
            }
            if (-x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
                x[5]+4100.f*u[0] > 0)
            {
               if (x[2] >= 0)
               {
                  return 8; /* 153_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 6_0";
   return 1; /* 6_0 */
}
static const size_t PM0_Ad_9_rowPtr[] = {
   0,3,6,7,8,11,11
};
static const size_t PM0_Ad_9_colIdx[] = {
   1,3,4,1,3,4,2,3,1,3,4
};
static const float PM0_Ad_9_data[] _ALIGN = {
   -0.00404967509f,0.988689109f,4.94344555f,0.988729606f,5.53455595f,
   27.6727797f,0.998667555f,1.f,-0.000809935017f,-0.00226217811f,0.988689109f
};
static const size_t PM0_Bd0_9_rowPtr[] = {
   0,1,2,2,2,3,3
};
static const size_t PM0_Bd0_9_colIdx[] = {
   0,0,0
};
static const float PM0_Bd0_9_data[] _ALIGN = {
   0.00202100421f,0.00751075143f,0.000404200841f
};
static const size_t PM0_Bd1_9_rowPtr[] = {
   0,1,2,2,2,3,3
};
static const size_t PM0_Bd1_9_colIdx[] = {
   0,0,0
};
static const float PM0_Bd1_9_data[] _ALIGN = {
   0.00202867088f,0.00375964234f,0.000405734176f
};
static const size_t PM0_C_0_9_rowPtr[] = {
   0,1,1,1,1,1,5,9,13,17,19,20
};
static const size_t PM0_C_0_9_colIdx[] = {
   2,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,3,4,2
};
static const float PM0_C_0_9_data[] _ALIGN = {
   1.f,-0.0241463415f,-0.5f,-0.000241463415f,-0.00120731707f,0.0241463415f,
   -0.5f,0.000241463415f,0.00120731707f,0.0241463415f,-0.5f,0.000241463415f,
   0.00120731707f,-0.0241463415f,-0.5f,-0.000241463415f,-0.00120731707f,1.f,
   5.f,4.f
};
static const size_t PM0_D_0_9_rowPtr[] = {
   0,0,0,0,0,0,1,2,3,4,4,4
};
static const size_t PM0_D_0_9_colIdx[] = {
   0,0,0,0
};
static const float PM0_D_0_9_data[] _ALIGN = {
   0.0241463415f,-0.0241463415f,-0.0241463415f,0.0241463415f
};
static void PM0_collision_9()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.0243902439f*x[0]+0.975609756f*x[3]+4.87804878f*x[4]+
             0.241463415f*x[5];
   tmpX[4] = 0.00487804878f*x[0]-0.00487804878f*x[3]+0.975609756f*x[4]+
             0.0482926829f*x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
}
static size_t PM0_natPreComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 2; /* 9_0 */
}
static size_t PM0_natPostComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (1.f*x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
          x[5]-4100.f*u[0] > 0)
      {
         return 5; /* 105_0 */
      }
      if (-1.f*x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
          x[5]+4100.f*u[0] > 0)
      {
         return 8; /* 153_0 */
      }
   }
   return 2; /* 9_0 */
}
static size_t PM0_forcedComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         return 2; /* 9_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         {
            const char cond2 = -x[0]-4100.f*x[1]+84898.9899f*x[2]-40.f*x[3]-
                               200.f*x[4]-9.9f*x[5]-4100.f*u[0] >= 0;
            if (cond2)
            {
               if (x[0]+4100.f*x[1]+84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+
                   9.9f*x[5]+4100.f*u[0] >= 0)
               {
                  return 1; /* 6_0 */
               }
            }
            else if (!cond2)
            {
               if (x[2] >= 0)
               {
                  return 4; /* 102_0 */
               }
            }
            if (-x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
                x[5]-4100.f*u[0] > 0)
            {
               if (x[2] >= 0)
               {
                  return 7; /* 150_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 9_0";
   return 2; /* 9_0 */
}
static const size_t PM0_Ad_96_rowPtr[] = {
   0,0,1,3,5,8,10
};
static const size_t PM0_Ad_96_colIdx[] = {
   1,2,5,4,5,2,4,5,2,5
};
static const float PM0_Ad_96_data[] _ALIGN = {
   1.f,0.998410498f,0.000333082641f,-5.f,-0.198f,0.061087776f,1.f,
   1.01839953e-05f,-1.54262061f,0.999742828f
};
static const size_t PM0_Bd0_96_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_96_colIdx[] = {
   0
};
static const float PM0_Bd0_96_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_96_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_96_colIdx[] = {
   0
};
static const float PM0_Bd1_96_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_96_rowPtr[] = {
   0,1,1,2,3,3,4,4,4,5,5,6
};
static const size_t PM0_C_0_96_colIdx[] = {
   2,5,5,2,2,2
};
static const float PM0_C_0_96_data[] _ALIGN = {
   1.f,1.f,1.f,-1.f,-1.f,4.f
};
static const size_t PM0_D_0_96_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_96_colIdx[] = {
   0
};
static const float PM0_D_0_96_data[] _ALIGN = {
   0
};
static void PM0_collision_96()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.926268989f*x[3]-3.63134494f*x[4]-0.18340126f*x[5];
   tmpX[5] = 18.340126f*x[3]+91.7006299f*x[4]+4.63134494f*x[5];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_96_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[5] >= 0)
   {
      if (x[2] >= 0)
      {
         return 0; /* 0_0 */
      }
   }
   return 3; /* 96_0 */
}
static size_t PM0_natPostComm_96_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (-x[3]-5.f*x[4]-0.252525253f*x[5] > 0)
      {
         return 6; /* 144_0 */
      }
   }
   return 3; /* 96_0 */
}
static size_t PM0_forcedComm_96_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 3; /* 96_0 */
      }
      else
      {
         if (x[3]+5.f*x[4]+0.252525253f*x[5] > 0)
         {
            return 5; /* 105_0 */
         }
         if (x[2] >= 0)
         {
            if (-x[3]-5.f*x[4]-0.252525253f*x[5] > 0)
            {
               return 8; /* 153_0 */
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         if (x[3]+5.f*x[4]+0.252525253f*x[5] > 0)
         {
            return 4; /* 102_0 */
         }
         if (x[2] >= 0)
         {
            if (-x[3]-5.f*x[4]-0.252525253f*x[5] > 0)
            {
               return 7; /* 150_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 96_0";
   return 3; /* 96_0 */
}
static const size_t PM0_Ad_102_rowPtr[] = {
   0,5,10,15,16,21,26
};
static const size_t PM0_Ad_102_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_102_data[] _ALIGN = {
   -0.0343739307f,0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   0.000106826614f,0.996452246f,0.00020027161f,0.00100135805f,0.000372517294f,
   1.f,-0.0318373139f,0.644541065f,-0.0902808493f,0.548595753f,-0.0177664773f,
   0.630366864f,-13.0947766f,1.78754405f,8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_102_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd0_102_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_102_data[] _ALIGN = {
   -0.0168911093f,-0.0645302154f,7.09700122e-05f,-0.0156440682f,0.309743595f
};
static const size_t PM0_Bd1_102_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd1_102_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_102_data[] _ALIGN = {
   -0.0174828214f,-0.0325965701f,3.58566018e-05f,-0.0161932457f,0.320623269f
};
static const size_t PM0_C_0_102_rowPtr[] = {
   0,1,1,2,3,3,4,4,4,5,8,9
};
static const size_t PM0_C_0_102_colIdx[] = {
   2,5,5,2,2,3,4,5,2
};
static const float PM0_C_0_102_data[] _ALIGN = {
   1.f,1.f,1.f,-1.f,-1.f,1.f,5.f,0.198f,4.f
};
static const size_t PM0_D_0_102_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_102_colIdx[] = {
   0
};
static const float PM0_D_0_102_data[] _ALIGN = {
   0
};
static void PM0_collision_102()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_102_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[5] >= 0)
   {
      if (x[2] >= 0)
      {
         return 1; /* 6_0 */
      }
   }
   return 4; /* 102_0 */
}
static size_t PM0_natPostComm_102_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
      {
         return 7; /* 150_0 */
      }
   }
   return 4; /* 102_0 */
}
static size_t PM0_forcedComm_102_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 4; /* 102_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
         {
            return 5; /* 105_0 */
         }
         if (x[2] >= 0)
         {
            if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
            {
               return 8; /* 153_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 102_0";
   return 4; /* 102_0 */
}
static const size_t PM0_Ad_105_rowPtr[] = {
   0,5,10,15,16,21,26
};
static const size_t PM0_Ad_105_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_105_data[] _ALIGN = {
   -0.0343739307f,0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   0.000106826614f,0.996452246f,0.00020027161f,0.00100135805f,0.000372517294f,
   1.f,-0.0318373139f,0.644541065f,-0.0902808493f,0.548595753f,-0.0177664773f,
   0.630366864f,-13.0947766f,1.78754405f,8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_105_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd0_105_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_105_data[] _ALIGN = {
   0.0168911093f,0.0645302154f,-7.09700122e-05f,0.0156440682f,-0.309743595f
};
static const size_t PM0_Bd1_105_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd1_105_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_105_data[] _ALIGN = {
   0.0174828214f,0.0325965701f,-3.58566018e-05f,0.0161932457f,-0.320623269f
};
static const size_t PM0_C_0_105_rowPtr[] = {
   0,1,1,2,3,3,4,4,4,5,8,9
};
static const size_t PM0_C_0_105_colIdx[] = {
   2,5,5,2,2,3,4,5,2
};
static const float PM0_C_0_105_data[] _ALIGN = {
   1.f,1.f,1.f,-1.f,-1.f,1.f,5.f,0.198f,4.f
};
static const size_t PM0_D_0_105_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_105_colIdx[] = {
   0
};
static const float PM0_D_0_105_data[] _ALIGN = {
   0
};
static void PM0_collision_105()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_105_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[5] >= 0)
   {
      if (x[2] >= 0)
      {
         return 2; /* 9_0 */
      }
   }
   return 5; /* 105_0 */
}
static size_t PM0_natPostComm_105_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
      {
         return 8; /* 153_0 */
      }
   }
   return 5; /* 105_0 */
}
static size_t PM0_forcedComm_105_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         return 5; /* 105_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
         {
            return 4; /* 102_0 */
         }
         if (x[2] >= 0)
         {
            if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
            {
               return 7; /* 150_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 105_0";
   return 5; /* 105_0 */
}
static const size_t PM0_Ad_144_rowPtr[] = {
   0,0,1,3,5,8,10
};
static const size_t PM0_Ad_144_colIdx[] = {
   1,2,5,4,5,2,4,5,2,5
};
static const float PM0_Ad_144_data[] _ALIGN = {
   1.f,0.998410498f,-0.000333082641f,-5.f,-0.198f,-0.061087776f,1.f,
   1.01839953e-05f,1.54262061f,0.999742828f
};
static const size_t PM0_Bd0_144_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_144_colIdx[] = {
   0
};
static const float PM0_Bd0_144_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_144_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_144_colIdx[] = {
   0
};
static const float PM0_Bd1_144_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_144_rowPtr[] = {
   0,1,2,2,2,3,3,4,5,5,5,6
};
static const size_t PM0_C_0_144_colIdx[] = {
   2,5,5,2,2,2
};
static const float PM0_C_0_144_data[] _ALIGN = {
   1.f,-1.f,-1.f,-1.f,-1.f,4.f
};
static const size_t PM0_D_0_144_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_144_colIdx[] = {
   0
};
static const float PM0_D_0_144_data[] _ALIGN = {
   0
};
static void PM0_collision_144()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.926268989f*x[3]-3.63134494f*x[4]-0.18340126f*x[5];
   tmpX[5] = 18.340126f*x[3]+91.7006299f*x[4]+4.63134494f*x[5];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_144_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (x[5] >= 0)
      {
         return 0; /* 0_0 */
      }
   }
   return 6; /* 144_0 */
}
static size_t PM0_natPostComm_144_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3]+5.f*x[4]+0.252525253f*x[5] > 0)
   {
      if (x[2] >= 0)
      {
         return 3; /* 96_0 */
      }
   }
   return 6; /* 144_0 */
}
static size_t PM0_forcedComm_144_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 6; /* 144_0 */
      }
      else
      {
         if (x[3]+5.f*x[4]+0.252525253f*x[5] > 0)
         {
            if (x[2] >= 0)
            {
               return 5; /* 105_0 */
            }
         }
         if (-x[3]-5.f*x[4]-0.252525253f*x[5] > 0)
         {
            return 8; /* 153_0 */
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         if (x[3]+5.f*x[4]+0.252525253f*x[5] > 0)
         {
            if (x[2] >= 0)
            {
               return 4; /* 102_0 */
            }
         }
         if (-x[3]-5.f*x[4]-0.252525253f*x[5] > 0)
         {
            return 7; /* 150_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 144_0";
   return 6; /* 144_0 */
}
static const size_t PM0_Ad_150_rowPtr[] = {
   0,5,10,15,16,21,26
};
static const size_t PM0_Ad_150_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_150_data[] _ALIGN = {
   -0.0343739307f,-0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,-1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   -0.000106826614f,0.996452246f,-0.00020027161f,-0.00100135805f,
   -0.000372517294f,1.f,-0.0318373139f,-0.644541065f,-0.0902808493f,
   0.548595753f,-0.0177664773f,0.630366864f,13.0947766f,1.78754405f,
   8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_150_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd0_150_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_150_data[] _ALIGN = {
   -0.0168911093f,-0.0645302154f,-7.09700122e-05f,-0.0156440682f,0.309743595f
};
static const size_t PM0_Bd1_150_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd1_150_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_150_data[] _ALIGN = {
   -0.0174828214f,-0.0325965701f,-3.58566018e-05f,-0.0161932457f,0.320623269f
};
static const size_t PM0_C_0_150_rowPtr[] = {
   0,1,2,2,2,3,3,4,5,5,8,9
};
static const size_t PM0_C_0_150_colIdx[] = {
   2,5,5,2,2,3,4,5,2
};
static const float PM0_C_0_150_data[] _ALIGN = {
   1.f,-1.f,-1.f,-1.f,-1.f,1.f,5.f,0.198f,4.f
};
static const size_t PM0_D_0_150_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_150_colIdx[] = {
   0
};
static const float PM0_D_0_150_data[] _ALIGN = {
   0
};
static void PM0_collision_150()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_150_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (x[5] >= 0)
      {
         return 1; /* 6_0 */
      }
   }
   return 7; /* 150_0 */
}
static size_t PM0_natPostComm_150_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
   {
      if (x[2] >= 0)
      {
         return 4; /* 102_0 */
      }
   }
   return 7; /* 150_0 */
}
static size_t PM0_forcedComm_150_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[1])
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         return 7; /* 150_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
         {
            if (x[2] >= 0)
            {
               return 5; /* 105_0 */
            }
         }
         if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
         {
            return 8; /* 153_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 150_0";
   return 7; /* 150_0 */
}
static const size_t PM0_Ad_153_rowPtr[] = {
   0,5,10,15,16,21,26
};
static const size_t PM0_Ad_153_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_153_data[] _ALIGN = {
   -0.0343739307f,-0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,-1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   -0.000106826614f,0.996452246f,-0.00020027161f,-0.00100135805f,
   -0.000372517294f,1.f,-0.0318373139f,-0.644541065f,-0.0902808493f,
   0.548595753f,-0.0177664773f,0.630366864f,13.0947766f,1.78754405f,
   8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_153_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd0_153_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_153_data[] _ALIGN = {
   0.0168911093f,0.0645302154f,7.09700122e-05f,0.0156440682f,-0.309743595f
};
static const size_t PM0_Bd1_153_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd1_153_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_153_data[] _ALIGN = {
   0.0174828214f,0.0325965701f,3.58566018e-05f,0.0161932457f,-0.320623269f
};
static const size_t PM0_C_0_153_rowPtr[] = {
   0,1,2,2,2,3,3,4,5,5,8,9
};
static const size_t PM0_C_0_153_colIdx[] = {
   2,5,5,2,2,3,4,5,2
};
static const float PM0_C_0_153_data[] _ALIGN = {
   1.f,-1.f,-1.f,-1.f,-1.f,1.f,5.f,0.198f,4.f
};
static const size_t PM0_D_0_153_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,0,0
};
static const size_t PM0_D_0_153_colIdx[] = {
   0
};
static const float PM0_D_0_153_data[] _ALIGN = {
   0
};
static void PM0_collision_153()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
}
static size_t PM0_natPreComm_153_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (x[5] >= 0)
      {
         return 2; /* 9_0 */
      }
   }
   return 8; /* 153_0 */
}
static size_t PM0_natPostComm_153_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
   {
      if (x[2] >= 0)
      {
         return 5; /* 105_0 */
      }
   }
   return 8; /* 153_0 */
}
static size_t PM0_forcedComm_153_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[1])
   {
      if (Subsystem_PM0_gateSignalBuffer[0])
      {
         return 8; /* 153_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[0])
      {
         if (-x[0]+x[3]+5.f*x[4]+0.453535354f*x[5] > 0)
         {
            if (x[2] >= 0)
            {
               return 4; /* 102_0 */
            }
         }
         if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5] > 0)
         {
            return 7; /* 150_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 153_0";
   return 8; /* 153_0 */
}
static const size_t * const PM0_Ad_rowPtr[] = {
   PM0_Ad_0_rowPtr,PM0_Ad_6_rowPtr,PM0_Ad_9_rowPtr,PM0_Ad_96_rowPtr,
   PM0_Ad_102_rowPtr,PM0_Ad_105_rowPtr,PM0_Ad_144_rowPtr,PM0_Ad_150_rowPtr,
   PM0_Ad_153_rowPtr
};
static const size_t * const PM0_Ad_colIdx[] = {
   PM0_Ad_0_colIdx,PM0_Ad_6_colIdx,PM0_Ad_9_colIdx,PM0_Ad_96_colIdx,
   PM0_Ad_102_colIdx,PM0_Ad_105_colIdx,PM0_Ad_144_colIdx,PM0_Ad_150_colIdx,
   PM0_Ad_153_colIdx
};
static const float * const Subsystem_PM0_Ad_data[] = {
   PM0_Ad_0_data,PM0_Ad_6_data,PM0_Ad_9_data,PM0_Ad_96_data,PM0_Ad_102_data,
   PM0_Ad_105_data,PM0_Ad_144_data,PM0_Ad_150_data,PM0_Ad_153_data
};
static const size_t * const PM0_Bd0_rowPtr[] = {
   PM0_Bd0_0_rowPtr,PM0_Bd0_6_rowPtr,PM0_Bd0_9_rowPtr,PM0_Bd0_96_rowPtr,
   PM0_Bd0_102_rowPtr,PM0_Bd0_105_rowPtr,PM0_Bd0_144_rowPtr,
   PM0_Bd0_150_rowPtr,PM0_Bd0_153_rowPtr
};
static const size_t * const PM0_Bd0_colIdx[] = {
   PM0_Bd0_0_colIdx,PM0_Bd0_6_colIdx,PM0_Bd0_9_colIdx,PM0_Bd0_96_colIdx,
   PM0_Bd0_102_colIdx,PM0_Bd0_105_colIdx,PM0_Bd0_144_colIdx,
   PM0_Bd0_150_colIdx,PM0_Bd0_153_colIdx
};
static const float * const Subsystem_PM0_Bd0_data[] = {
   PM0_Bd0_0_data,PM0_Bd0_6_data,PM0_Bd0_9_data,PM0_Bd0_96_data,
   PM0_Bd0_102_data,PM0_Bd0_105_data,PM0_Bd0_144_data,PM0_Bd0_150_data,
   PM0_Bd0_153_data
};
static const size_t * const PM0_Bd1_rowPtr[] = {
   PM0_Bd1_0_rowPtr,PM0_Bd1_6_rowPtr,PM0_Bd1_9_rowPtr,PM0_Bd1_96_rowPtr,
   PM0_Bd1_102_rowPtr,PM0_Bd1_105_rowPtr,PM0_Bd1_144_rowPtr,
   PM0_Bd1_150_rowPtr,PM0_Bd1_153_rowPtr
};
static const size_t * const PM0_Bd1_colIdx[] = {
   PM0_Bd1_0_colIdx,PM0_Bd1_6_colIdx,PM0_Bd1_9_colIdx,PM0_Bd1_96_colIdx,
   PM0_Bd1_102_colIdx,PM0_Bd1_105_colIdx,PM0_Bd1_144_colIdx,
   PM0_Bd1_150_colIdx,PM0_Bd1_153_colIdx
};
static const float * const Subsystem_PM0_Bd1_data[] = {
   PM0_Bd1_0_data,PM0_Bd1_6_data,PM0_Bd1_9_data,PM0_Bd1_96_data,
   PM0_Bd1_102_data,PM0_Bd1_105_data,PM0_Bd1_144_data,PM0_Bd1_150_data,
   PM0_Bd1_153_data
};
static const size_t * const PM0_C_0_rowPtr[] = {
   PM0_C_0_0_rowPtr,PM0_C_0_6_rowPtr,PM0_C_0_9_rowPtr,PM0_C_0_96_rowPtr,
   PM0_C_0_102_rowPtr,PM0_C_0_105_rowPtr,PM0_C_0_144_rowPtr,
   PM0_C_0_150_rowPtr,PM0_C_0_153_rowPtr
};
static const size_t * const PM0_C_0_colIdx[] = {
   PM0_C_0_0_colIdx,PM0_C_0_6_colIdx,PM0_C_0_9_colIdx,PM0_C_0_96_colIdx,
   PM0_C_0_102_colIdx,PM0_C_0_105_colIdx,PM0_C_0_144_colIdx,
   PM0_C_0_150_colIdx,PM0_C_0_153_colIdx
};
static const float * const Subsystem_PM0_C_0_data[] = {
   PM0_C_0_0_data,PM0_C_0_6_data,PM0_C_0_9_data,PM0_C_0_96_data,
   PM0_C_0_102_data,PM0_C_0_105_data,PM0_C_0_144_data,PM0_C_0_150_data,
   PM0_C_0_153_data
};
static const size_t * const PM0_D_0_rowPtr[] = {
   PM0_D_0_0_rowPtr,PM0_D_0_6_rowPtr,PM0_D_0_9_rowPtr,PM0_D_0_96_rowPtr,
   PM0_D_0_102_rowPtr,PM0_D_0_105_rowPtr,PM0_D_0_144_rowPtr,
   PM0_D_0_150_rowPtr,PM0_D_0_153_rowPtr
};
static const size_t * const PM0_D_0_colIdx[] = {
   PM0_D_0_0_colIdx,PM0_D_0_6_colIdx,PM0_D_0_9_colIdx,PM0_D_0_96_colIdx,
   PM0_D_0_102_colIdx,PM0_D_0_105_colIdx,PM0_D_0_144_colIdx,
   PM0_D_0_150_colIdx,PM0_D_0_153_colIdx
};
static const float * const Subsystem_PM0_D_0_data[] = {
   PM0_D_0_0_data,PM0_D_0_6_data,PM0_D_0_9_data,PM0_D_0_96_data,
   PM0_D_0_102_data,PM0_D_0_105_data,PM0_D_0_144_data,PM0_D_0_150_data,
   PM0_D_0_153_data
};
static void (*const PM0_collision[9]) () = {
   PM0_collision_0,PM0_collision_6,PM0_collision_9,PM0_collision_96,
   PM0_collision_102,PM0_collision_105,PM0_collision_144,PM0_collision_150,
   PM0_collision_153
};
static size_t (*const PM0_natPreComm[9]) () = {
   PM0_natPreComm_0_0,PM0_natPreComm_6_0,PM0_natPreComm_9_0,
   PM0_natPreComm_96_0,PM0_natPreComm_102_0,PM0_natPreComm_105_0,
   PM0_natPreComm_144_0,PM0_natPreComm_150_0,PM0_natPreComm_153_0
};
static size_t (*const PM0_natPostComm[9]) () = {
   PM0_natPostComm_0_0,PM0_natPostComm_6_0,PM0_natPostComm_9_0,
   PM0_natPostComm_96_0,PM0_natPostComm_102_0,PM0_natPostComm_105_0,
   PM0_natPostComm_144_0,PM0_natPostComm_150_0,PM0_natPostComm_153_0
};
static size_t (*const PM0_forcedComm[9]) () = {
   PM0_forcedComm_0_0,PM0_forcedComm_6_0,PM0_forcedComm_9_0,
   PM0_forcedComm_96_0,PM0_forcedComm_102_0,PM0_forcedComm_105_0,
   PM0_forcedComm_144_0,PM0_forcedComm_150_0,PM0_forcedComm_153_0
};
static size_t Subsystem_PM0_conductionMasks[9]={
   0,6,9,96,102,105,144,150,153
};
static size_t Subsystem_PM0_directionMasks[9]={
   0,0,0,0,0,0,0,0,0
};
static void Subsystem_PM0_natComm()
{
   size_t oldTopo = Subsystem_PM0_topoIdx;
   size_t midTopo = Subsystem_PM0_topoIdx;
   size_t preConductionToggleMask = 0;
   size_t postConductionToggleMask = 0;
   size_t directionToggleMask = 0;
   Subsystem_PM0_topoIdx = PM0_natPreComm[Subsystem_PM0_topoIdx]();
   midTopo = Subsystem_PM0_topoIdx;
   Subsystem_PM0_topoIdx = PM0_natPostComm[Subsystem_PM0_topoIdx]();
   preConductionToggleMask = Subsystem_PM0_conductionMasks[midTopo] ^
                             Subsystem_PM0_conductionMasks[oldTopo];
   if (preConductionToggleMask)
   {
      postConductionToggleMask =
         Subsystem_PM0_conductionMasks[Subsystem_PM0_topoIdx] ^
         Subsystem_PM0_conductionMasks[midTopo];
      directionToggleMask =
         Subsystem_PM0_directionMasks[Subsystem_PM0_topoIdx] ^
         Subsystem_PM0_directionMasks[oldTopo];
      if (postConductionToggleMask &
          (~preConductionToggleMask | directionToggleMask))
      {
         PM0_collision[Subsystem_PM0_topoIdx]();
      }
      else
      {
         PM0_collision[midTopo]();
      }
   }
}
static void Subsystem_PM0_forcedComm()
{
   Subsystem_PM0_topoIdx = PM0_forcedComm[Subsystem_PM0_topoIdx]();
}
static void Subsystem_PM0_output_0()
{
   const float * _RESTRICT C_0_data =
      _ASSUME_ALIGNED(Subsystem_PM0_C_0_data[Subsystem_PM0_topoIdx]);
   const float * _RESTRICT D_0_data =
      _ASSUME_ALIGNED(Subsystem_PM0_D_0_data[Subsystem_PM0_topoIdx]);
   const size_t meterIdx[]={
      0,1,2,3,4,5,6,7,8,10,11
   };
   float y[11] _ALIGN;
   size_t i;
   for (i = 0; i < 11; ++i)
   {
      y[i] = 0;
      {
         const size_t *rowPtr = PM0_C_0_rowPtr[Subsystem_PM0_topoIdx];
         const size_t *colIdx = PM0_C_0_colIdx[Subsystem_PM0_topoIdx];
         size_t j;
         for (j = rowPtr[i]; j < rowPtr[i+1]; ++j)
            *(y+i) += C_0_data[j]*Subsystem_PM0_x[colIdx[j]];
      }
      {
         const size_t *rowPtr = PM0_D_0_rowPtr[Subsystem_PM0_topoIdx];
         const size_t *colIdx = PM0_D_0_colIdx[Subsystem_PM0_topoIdx];
         size_t j;
         for (j = rowPtr[i]; j < rowPtr[i+1]; ++j)
            *(y+i) += D_0_data[j]*Subsystem_PM0_u[colIdx[j]];
      }
   }
   for (i = 0; i < 11; ++i)
   {
      Subsystem_PM0_y[meterIdx[i]] = y[i];
   }
}
static void Subsystem_PM0_update(const float * _RESTRICT aAd_data,
                                 const float * _RESTRICT aBd0_data,
                                 const float * _RESTRICT aBd1_data,
                                 float * _RESTRICT x)
{
   const float * _RESTRICT Ad_data = _ASSUME_ALIGNED(aAd_data);
   const float * _RESTRICT Bd0_data = _ASSUME_ALIGNED(aBd0_data);
   const float * _RESTRICT Bd1_data = _ASSUME_ALIGNED(aBd1_data);
   const float * _RESTRICT prevX = Subsystem_PM0_prevX;
   size_t i;
   for (i = 0; i < 6; ++i)
   {
      x[i] = 0;
      {
         const size_t *rowPtr = PM0_Ad_rowPtr[Subsystem_PM0_topoIdx];
         const size_t *colIdx = PM0_Ad_colIdx[Subsystem_PM0_topoIdx];
         size_t j;
         for (j = rowPtr[i]; j < rowPtr[i+1]; ++j)
            *(x+i) += Ad_data[j]*prevX[colIdx[j]];
      }
      {
         const size_t *rowPtr = PM0_Bd0_rowPtr[Subsystem_PM0_topoIdx];
         const size_t *colIdx = PM0_Bd0_colIdx[Subsystem_PM0_topoIdx];
         size_t j;
         for (j = rowPtr[i]; j < rowPtr[i+1]; ++j)
            *(x+i) += Bd0_data[j]*Subsystem_PM0_prevU[colIdx[j]];
      }
      {
         const size_t *rowPtr = PM0_Bd1_rowPtr[Subsystem_PM0_topoIdx];
         const size_t *colIdx = PM0_Bd1_colIdx[Subsystem_PM0_topoIdx];
         size_t j;
         for (j = rowPtr[i]; j < rowPtr[i+1]; ++j)
            *(x+i) += Bd1_data[j]*Subsystem_PM0_u[colIdx[j]];
      }
   }
}
static char Subsystem_first;
static uint32_t Subsystem_tickLo;
static int32_t Subsystem_tickHi;
Subsystem_ExternalInputs Subsystem_U;
Subsystem_ExternalOutputs Subsystem_Y;
Subsystem_BlockOutputs Subsystem_B;
Subsystem_ModelStates Subsystem_X _ALIGN;
const char * Subsystem_errorStatus;
const float Subsystem_sampleTime = 3.33333333e-07f;
const char * const Subsystem_checksum =
   "2e52fe871bc9d7474a5e8cad0b4a9eff5d76f928";
void Subsystem_initialize(float time)
{
   float remainder;
   Subsystem_errorStatus = NULL;
   Subsystem_tickHi = floor(time/(4294967296.0*Subsystem_sampleTime));
   remainder = time - Subsystem_tickHi*4294967296.0*Subsystem_sampleTime;
   Subsystem_tickLo = floor(remainder/Subsystem_sampleTime + .5);
   remainder -= Subsystem_tickLo*Subsystem_sampleTime;
   if (fabsf(remainder) > 1e-6*fabsf(time))
   {
      Subsystem_errorStatus =
         "Start time must be an integer multiple of the base sample time.";
   }
   memset(&Subsystem_X, 0, sizeof(Subsystem_X));

   /* Initialization for Subsystem : 'Subsystem' */
   Subsystem_X.Subsystem_i1_PM0_s[0] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[1] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[2] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[3] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[4] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[5] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[6] = 0;
   Subsystem_X.Subsystem_i1_PM0_s[7] = 0;
   Subsystem_PM0_topoIdx = 0;
   Subsystem_X.Subsystem_PM0_x[0] = 0;
   Subsystem_X.Subsystem_PM0_x[1] = 0;
   Subsystem_X.Subsystem_PM0_x[2] = 0;
   Subsystem_X.Subsystem_PM0_x[3] = 0;
   Subsystem_X.Subsystem_PM0_x[4] = 0;
   Subsystem_X.Subsystem_PM0_x[5] = 0;
   Subsystem_PM0_x = &Subsystem_X.Subsystem_PM0_x[0];
   Subsystem_first = 1;
}

void Subsystem_step(void)
{
   if (Subsystem_errorStatus)
   {
      return;
   }

   /* Data Type : 'Subsystem/Data Type' */
   if (Subsystem_U.Pulse < 0.f || Subsystem_U.Pulse > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type'";
   }
   else
   {
      Subsystem_B.DataType = (bool)Subsystem_U.Pulse;
   }
   /* Data Type : 'Subsystem/Data Type1' */
   if (Subsystem_U.Pulse1 < 0.f || Subsystem_U.Pulse1 > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type1'";
   }
   else
   {
      Subsystem_B.DataType1 = (bool)Subsystem_U.Pulse1;
   }


   /* Electrical model */


   /* Electrical model input */
   /* Voltage Source DC : 'Subsystem/V_dc' */
   Subsystem_PM0_u[0]=600.f;
   /* End of electrical model input */
   if (!Subsystem_first)
   {
      memcpy(Subsystem_PM0_prevX,Subsystem_PM0_x,6*sizeof(float));
      Subsystem_PM0_update(Subsystem_PM0_Ad_data[Subsystem_PM0_topoIdx],
                           Subsystem_PM0_Bd0_data[Subsystem_PM0_topoIdx],
                           Subsystem_PM0_Bd1_data[Subsystem_PM0_topoIdx],
                           Subsystem_PM0_x);
   }


   /* Commutation */
   Subsystem_PM0_natComm();
   Subsystem_PM0_gateSignalBuffer[1] = Subsystem_B.DataType1;
   Subsystem_PM0_gateSignalBuffer[0] = Subsystem_B.DataType;
   Subsystem_PM0_forcedComm();

   /* Electrical model output */
   Subsystem_PM0_output_0();
   Subsystem_PM0_y[9] = 1.f*Subsystem_PM0_x[1];
   /* End of electrical model output */

   /* End of electrical model */


   /* Global output signals */
   Subsystem_Y.AMLr = Subsystem_PM0_y[10];
   Subsystem_Y.VMC = Subsystem_PM0_y[9];
   Subsystem_Y.VMD1 = Subsystem_PM0_y[5];
   Subsystem_Y.VMD2 = Subsystem_PM0_y[6];
   Subsystem_Y.VMD3 = Subsystem_PM0_y[7];
   Subsystem_Y.VMD4 = Subsystem_PM0_y[8];
   Subsystem_Y.VMOut = Subsystem_PM0_y[0];
   Subsystem_Y.AMD1 = Subsystem_PM0_y[1];
   Subsystem_Y.AMD2 = Subsystem_PM0_y[2];
   Subsystem_Y.AMD3 = Subsystem_PM0_y[3];
   Subsystem_Y.AMD4 = Subsystem_PM0_y[4];
   Subsystem_Y.AMIo = Subsystem_PM0_y[11];

   Subsystem_first = 0;
   if (Subsystem_errorStatus)
   {
      return;
   }

   /* Update for Subsystem : 'Subsystem' */
   memcpy(Subsystem_PM0_prevU,Subsystem_PM0_u,1*sizeof(float));
}

void Subsystem_terminate(void)
{
}
