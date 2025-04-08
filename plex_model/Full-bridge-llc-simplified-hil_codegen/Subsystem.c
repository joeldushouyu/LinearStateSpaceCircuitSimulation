/*
 * Implementation file for: Full-bridge-llc-simplified-hil/Subsystem
 * Generated with         : PLECS 4.9.2
 * Generated on           : 8 Apr 2025 13:07:06
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
static float Subsystem_PM0_tmpX[7] _ALIGN;
static float Subsystem_PM0_prevX[7] _ALIGN;
static float Subsystem_PM0_u[1] _ALIGN;
static float Subsystem_PM0_prevU[1] _ALIGN;
static float Subsystem_PM0_y[6] _ALIGN;
static float Subsystem_PM0_gateSignalBuffer[2] _ALIGN;
static size_t Subsystem_PM0_topoIdx;
static char Subsystem_PM0_withDiracs;
static const size_t PM0_Ad_0_rowPtr[] = {
   0,0,1,2,3,4,4,4
};
static const size_t PM0_Ad_0_colIdx[] = {
   1,2,4,4
};
static const float PM0_Ad_0_data[] _ALIGN = {
   1.f,0.998667555f,-5.f,1.f
};
static const size_t PM0_Bd0_0_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_0_colIdx[] = {
   0
};
static const float PM0_Bd0_0_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_0_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_0_colIdx[] = {
   0
};
static const float PM0_Bd1_0_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_0_rowPtr[] = {
   0,1,2,2,2,2
};
static const size_t PM0_C_0_0_colIdx[] = {
   2,2
};
static const float PM0_C_0_0_data[] _ALIGN = {
   -1.f,-1.f
};
static const size_t PM0_D_0_0_rowPtr[] = {
   0,0,0,0,0,0
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
   x[6] = 0.;
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
   if (-x[2] > 0)
   {
      return 9; /* 12_0 */
   }
   return 0; /* 0_0 */
}
static size_t PM0_forcedComm_0_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 0; /* 0_0 */
      }
      else
      {
         {
            const char cond6 = x[1]+20.7070707f*x[2]+u[0] >= 0;
            if (cond6)
            {
               if (-x[1]+20.7070707f*x[2]-u[0] >= 0)
               {
                  return 2; /* 2_0 */
               }
            }
            else if (!cond6)
            {
               if (-x[1]+81.5070707f*x[2]-u[0] >= 0)
               {
                  return 5; /* 6_0 */
               }
            }
            if (x[1]+81.5070707f*x[2]+u[0] >= 0)
            {
               if (x[1]-20.7070707f*x[2]+u[0] > 0)
               {
                  return 8; /* 10_0 */
               }
            }
            else
            {
               if (x[1]-81.5070707f*x[2]+u[0] > 0)
               {
                  return 11; /* 14_0 */
               }
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         {
            const char cond2 = x[1]+20.7070707f*x[2]-u[0] >= 0;
            if (cond2)
            {
               if (-x[1]+20.7070707f*x[2]+u[0] >= 0)
               {
                  return 1; /* 1_0 */
               }
            }
            else if (!cond2)
            {
               if (-x[1]+81.5070707f*x[2]+u[0] >= 0)
               {
                  return 4; /* 5_0 */
               }
            }
            if (x[1]+81.5070707f*x[2]-u[0] >= 0)
            {
               if (x[1]-20.7070707f*x[2]-u[0] > 0)
               {
                  return 7; /* 9_0 */
               }
            }
            else
            {
               if (x[1]-81.5070707f*x[2]-u[0] > 0)
               {
                  return 10; /* 13_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 0_0";
   return 0; /* 0_0 */
}
static const size_t PM0_Ad_1_rowPtr[] = {
   0,3,6,7,8,11,11,11
};
static const size_t PM0_Ad_1_colIdx[] = {
   1,3,4,1,3,4,2,3,1,3,4
};
static const float PM0_Ad_1_data[] _ALIGN = {
   -0.00404967509f,0.988689109f,4.94344555f,0.988729606f,5.53455595f,
   27.6727797f,0.998667555f,1.f,-0.000809935017f,-0.00226217811f,0.988689109f
};
static const size_t PM0_Bd0_1_rowPtr[] = {
   0,1,2,2,2,3,3,3
};
static const size_t PM0_Bd0_1_colIdx[] = {
   0,0,0
};
static const float PM0_Bd0_1_data[] _ALIGN = {
   0.00202100421f,0.00751075143f,0.000404200841f
};
static const size_t PM0_Bd1_1_rowPtr[] = {
   0,1,2,2,2,3,3,3
};
static const size_t PM0_Bd1_1_colIdx[] = {
   0,0,0
};
static const float PM0_Bd1_1_data[] _ALIGN = {
   0.00202867088f,0.00375964234f,0.000405734176f
};
static const size_t PM0_C_0_1_rowPtr[] = {
   0,4,8,8,8,10
};
static const size_t PM0_C_0_1_colIdx[] = {
   1,2,3,4,1,2,3,4,3,4
};
static const float PM0_C_0_1_data[] _ALIGN = {
   -0.0482926829f,-1.f,-0.000482926829f,-0.00241463415f,0.0482926829f,-1.f,
   0.000482926829f,0.00241463415f,1.f,5.f
};
static const size_t PM0_D_0_1_rowPtr[] = {
   0,1,2,2,2,2
};
static const size_t PM0_D_0_1_colIdx[] = {
   0,0
};
static const float PM0_D_0_1_data[] _ALIGN = {
   0.0482926829f,-0.0482926829f
};
static void PM0_collision_1()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.0243902439f*x[0]+0.975609756f*x[3]+4.87804878f*x[4]+
             0.241463415f*x[5]+0.241463415f*x[6];
   tmpX[4] = 0.00487804878f*x[0]-0.00487804878f*x[3]+0.975609756f*x[4]+
             0.0482926829f*x[5]+0.0482926829f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
   x[6] = 0.;
}
static size_t PM0_natPreComm_1_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 1; /* 1_0 */
}
static size_t PM0_natPostComm_1_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   {
      const char cond1 = -x[0]-4100.f*x[1]+334178.99f*x[2]-40.f*x[3]-200.f*
                         x[4]-9.9f*x[5]-9.9f*x[6]+4100.f*u[0] >= 0;
      if (cond1)
      {
         if (-1.f*x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
             x[5]-9.9f*x[6]+4100.f*u[0] > 0)
         {
            return 4; /* 5_0 */
         }
      }
      else if (!cond1)
      {
         if (-x[0]-4100.f*x[1]-334178.99f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*x[5]-
             9.9f*x[6]+4100.f*u[0] > 0)
         {
            return 10; /* 13_0 */
         }
      }
      if (x[0]+4100.f*x[1]+334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*x[5]+
          9.9f*x[6]-4100.f*u[0] >= 0)
      {
         if (1.f*x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
             x[5]+9.9f*x[6]-4100.f*u[0] > 0)
         {
            return 7; /* 9_0 */
         }
      }
   }
   return 1; /* 1_0 */
}
static size_t PM0_forcedComm_1_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 1; /* 1_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         {
            const char cond2 = x[0]+4100.f*x[1]+84898.9899f*x[2]+40.f*x[3]+
                               200.f*x[4]+9.9f*x[5]+9.9f*x[6]+4100.f*u[0] >=
                               0;
            if (cond2)
            {
               if (-x[0]-4100.f*x[1]+84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-
                   9.9f*x[5]-9.9f*x[6]-4100.f*u[0] >= 0)
               {
                  return 2; /* 2_0 */
               }
            }
            else if (!cond2)
            {
               if (-x[0]-4100.f*x[1]+334178.99f*x[2]-40.f*x[3]-200.f*x[4]-
                   9.9f*x[5]-9.9f*x[6]-4100.f*u[0] >= 0)
               {
                  return 5; /* 6_0 */
               }
            }
            if (x[0]+4100.f*x[1]+334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
                x[5]+9.9f*x[6]+4100.f*u[0] >= 0)
            {
               if (x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+
                   9.9f*x[5]+9.9f*x[6]+4100.f*u[0] > 0)
               {
                  return 8; /* 10_0 */
               }
            }
            else
            {
               if (x[0]+4100.f*x[1]-334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
                   x[5]+9.9f*x[6]+4100.f*u[0] > 0)
               {
                  return 11; /* 14_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 1_0";
   return 1; /* 1_0 */
}
static const size_t PM0_Ad_2_rowPtr[] = {
   0,3,6,7,8,11,11,11
};
static const size_t PM0_Ad_2_colIdx[] = {
   1,3,4,1,3,4,2,3,1,3,4
};
static const float PM0_Ad_2_data[] _ALIGN = {
   -0.00404967509f,0.988689109f,4.94344555f,0.988729606f,5.53455595f,
   27.6727797f,0.998667555f,1.f,-0.000809935017f,-0.00226217811f,0.988689109f
};
static const size_t PM0_Bd0_2_rowPtr[] = {
   0,1,2,2,2,3,3,3
};
static const size_t PM0_Bd0_2_colIdx[] = {
   0,0,0
};
static const float PM0_Bd0_2_data[] _ALIGN = {
   -0.00202100421f,-0.00751075143f,-0.000404200841f
};
static const size_t PM0_Bd1_2_rowPtr[] = {
   0,1,2,2,2,3,3,3
};
static const size_t PM0_Bd1_2_colIdx[] = {
   0,0,0
};
static const float PM0_Bd1_2_data[] _ALIGN = {
   -0.00202867088f,-0.00375964234f,-0.000405734176f
};
static const size_t PM0_C_0_2_rowPtr[] = {
   0,4,8,8,8,10
};
static const size_t PM0_C_0_2_colIdx[] = {
   1,2,3,4,1,2,3,4,3,4
};
static const float PM0_C_0_2_data[] _ALIGN = {
   -0.0482926829f,-1.f,-0.000482926829f,-0.00241463415f,0.0482926829f,-1.f,
   0.000482926829f,0.00241463415f,1.f,5.f
};
static const size_t PM0_D_0_2_rowPtr[] = {
   0,1,2,2,2,2
};
static const size_t PM0_D_0_2_colIdx[] = {
   0,0
};
static const float PM0_D_0_2_data[] _ALIGN = {
   -0.0482926829f,0.0482926829f
};
static void PM0_collision_2()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.0243902439f*x[0]+0.975609756f*x[3]+4.87804878f*x[4]+
             0.241463415f*x[5]+0.241463415f*x[6];
   tmpX[4] = 0.00487804878f*x[0]-0.00487804878f*x[3]+0.975609756f*x[4]+
             0.0482926829f*x[5]+0.0482926829f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
   x[6] = 0.;
}
static size_t PM0_natPreComm_2_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 2; /* 2_0 */
}
static size_t PM0_natPostComm_2_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   {
      const char cond1 = -x[0]-4100.f*x[1]+334178.99f*x[2]-40.f*x[3]-200.f*
                         x[4]-9.9f*x[5]-9.9f*x[6]-4100.f*u[0] >= 0;
      if (cond1)
      {
         if (-1.f*x[0]-4100.f*x[1]-84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*
             x[5]-9.9f*x[6]-4100.f*u[0] > 0)
         {
            return 5; /* 6_0 */
         }
      }
      else if (!cond1)
      {
         if (-x[0]-4100.f*x[1]-334178.99f*x[2]-40.f*x[3]-200.f*x[4]-9.9f*x[5]-
             9.9f*x[6]-4100.f*u[0] > 0)
         {
            return 11; /* 14_0 */
         }
      }
      if (x[0]+4100.f*x[1]+334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*x[5]+
          9.9f*x[6]+4100.f*u[0] >= 0)
      {
         if (1.f*x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
             x[5]+9.9f*x[6]+4100.f*u[0] > 0)
         {
            return 8; /* 10_0 */
         }
      }
   }
   return 2; /* 2_0 */
}
static size_t PM0_forcedComm_2_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         return 2; /* 2_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         {
            const char cond2 = x[0]+4100.f*x[1]+84898.9899f*x[2]+40.f*x[3]+
                               200.f*x[4]+9.9f*x[5]+9.9f*x[6]-4100.f*u[0] >=
                               0;
            if (cond2)
            {
               if (-x[0]-4100.f*x[1]+84898.9899f*x[2]-40.f*x[3]-200.f*x[4]-
                   9.9f*x[5]-9.9f*x[6]+4100.f*u[0] >= 0)
               {
                  return 1; /* 1_0 */
               }
            }
            else if (!cond2)
            {
               if (-x[0]-4100.f*x[1]+334178.99f*x[2]-40.f*x[3]-200.f*x[4]-
                   9.9f*x[5]-9.9f*x[6]+4100.f*u[0] >= 0)
               {
                  return 4; /* 5_0 */
               }
            }
            if (x[0]+4100.f*x[1]+334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
                x[5]+9.9f*x[6]-4100.f*u[0] >= 0)
            {
               if (x[0]+4100.f*x[1]-84898.9899f*x[2]+40.f*x[3]+200.f*x[4]+
                   9.9f*x[5]+9.9f*x[6]-4100.f*u[0] > 0)
               {
                  return 7; /* 9_0 */
               }
            }
            else
            {
               if (x[0]+4100.f*x[1]-334178.99f*x[2]+40.f*x[3]+200.f*x[4]+9.9f*
                   x[5]+9.9f*x[6]-4100.f*u[0] > 0)
               {
                  return 10; /* 13_0 */
               }
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 2_0";
   return 2; /* 2_0 */
}
static const size_t PM0_Ad_4_rowPtr[] = {
   0,0,1,3,5,8,10,10
};
static const size_t PM0_Ad_4_colIdx[] = {
   1,2,5,4,5,2,4,5,2,5
};
static const float PM0_Ad_4_data[] _ALIGN = {
   1.f,0.998410498f,-0.000333082641f,-5.f,-0.198f,-0.061087776f,1.f,
   1.01839953e-05f,1.54262061f,0.999742828f
};
static const size_t PM0_Bd0_4_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_4_colIdx[] = {
   0
};
static const float PM0_Bd0_4_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_4_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_4_colIdx[] = {
   0
};
static const float PM0_Bd1_4_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_4_rowPtr[] = {
   0,0,1,2,2,2
};
static const size_t PM0_C_0_4_colIdx[] = {
   2,5
};
static const float PM0_C_0_4_data[] _ALIGN = {
   -1.95368655f,-1.f
};
static const size_t PM0_D_0_4_rowPtr[] = {
   0,0,0,0,0,0
};
static const size_t PM0_D_0_4_colIdx[] = {
   0
};
static const float PM0_D_0_4_data[] _ALIGN = {
   0
};
static void PM0_collision_4()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.926268989f*x[3]-3.63134494f*x[4]-0.18340126f*x[5]-
             0.181567247f*x[6];
   tmpX[5] = 18.340126f*x[3]+91.7006299f*x[4]+4.63134494f*x[5]+4.58503149f*
             x[6];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = 0.;
}
static size_t PM0_natPreComm_4_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (x[2] >= 0)
      {
         return 0; /* 0_0 */
      }
      else
      {
         return 6; /* 8_0 */
      }
   }
   return 3; /* 4_0 */
}
static size_t PM0_natPostComm_4_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[3]-5.f*x[4]-0.252525253f*x[5]-0.25f*x[6] > 0)
   {
      if (-x[2] > 0)
      {
         return 9; /* 12_0 */
      }
   }
   return 3; /* 4_0 */
}
static size_t PM0_forcedComm_4_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 3; /* 4_0 */
      }
      else
      {
         if (-x[3]-5.f*x[4]-0.252525253f*x[5]-0.25f*x[6] > 0)
         {
            if (-x[1]+81.5070707f*x[2]-u[0] >= 0)
            {
               return 5; /* 6_0 */
            }
            else
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (-x[3]-5.f*x[4]-0.252525253f*x[5]-0.25f*x[6] > 0)
         {
            if (-x[1]+81.5070707f*x[2]+u[0] >= 0)
            {
               return 4; /* 5_0 */
            }
            else
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 4_0";
   return 3; /* 4_0 */
}
static const size_t PM0_Ad_5_rowPtr[] = {
   0,5,10,15,16,21,26,26
};
static const size_t PM0_Ad_5_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_5_data[] _ALIGN = {
   -0.0343739307f,-0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,-1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   -0.000106826614f,0.996452246f,-0.00020027161f,-0.00100135805f,
   -0.000372517294f,1.f,-0.0318373139f,-0.644541065f,-0.0902808493f,
   0.548595753f,-0.0177664773f,0.630366864f,13.0947766f,1.78754405f,
   8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_5_rowPtr[] = {
   0,1,2,3,3,4,5,5
};
static const size_t PM0_Bd0_5_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_5_data[] _ALIGN = {
   0.0168911093f,0.0645302154f,7.09700122e-05f,0.0156440682f,-0.309743595f
};
static const size_t PM0_Bd1_5_rowPtr[] = {
   0,1,2,3,3,4,5,5
};
static const size_t PM0_Bd1_5_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_5_data[] _ALIGN = {
   0.0174828214f,0.0325965701f,3.58566018e-05f,0.0161932457f,-0.320623269f
};
static const size_t PM0_C_0_5_rowPtr[] = {
   0,0,5,6,6,9
};
static const size_t PM0_C_0_5_colIdx[] = {
   1,2,3,4,5,5,3,4,5
};
static const float PM0_C_0_5_data[] _ALIGN = {
   0.0195667642f,-1.59482963f,0.000195667642f,0.000978338209f,3.87421931e-05f,
   -1.f,1.f,5.f,0.198f
};
static const size_t PM0_D_0_5_rowPtr[] = {
   0,0,1,1,1,1
};
static const size_t PM0_D_0_5_colIdx[] = {
   0
};
static const float PM0_D_0_5_data[] _ALIGN = {
   -0.0195667642f
};
static void PM0_collision_5()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5]+0.175318207f*x[6];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5]-0.0191754289f*x[6];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5]+1.36967349f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = 0.;
}
static size_t PM0_natPreComm_5_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (-x[1]+81.5070707f*x[2]-0.01f*x[3]-0.05f*x[4]-0.00198f*x[5]+u[0] >=
          0)
      {
         return 1; /* 1_0 */
      }
      else
      {
         return 7; /* 9_0 */
      }
   }
   return 4; /* 5_0 */
}
static size_t PM0_natPostComm_5_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5]-0.35f*x[6] > 0)
   {
      if (x[0]+468.655057f*x[1]-38198.7009f*x[2]+3.68655057f*x[3]+18.4327529f*
          x[4]+0.729937014f*x[5]+0.821637644f*x[6]-468.655057f*u[0] > 0)
      {
         return 10; /* 13_0 */
      }
   }
   return 4; /* 5_0 */
}
static size_t PM0_forcedComm_5_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 4; /* 5_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5]-0.35f*x[6] > 0)
         {
            if (-x[0]-468.655057f*x[1]+38198.7009f*x[2]-3.68655057f*x[3]-
                18.4327529f*x[4]-0.729937014f*x[5]-0.821637644f*x[6]-
                468.655057f*
                u[0] >= 0)
            {
               return 5; /* 6_0 */
            }
            else
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 5_0";
   return 4; /* 5_0 */
}
static const size_t PM0_Ad_6_rowPtr[] = {
   0,5,10,15,16,21,26,26
};
static const size_t PM0_Ad_6_colIdx[] = {
   1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,3,1,2,3,4,5,1,2,3,4,5
};
static const float PM0_Ad_6_data[] _ALIGN = {
   -0.0343739307f,-0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,-1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   -0.000106826614f,0.996452246f,-0.00020027161f,-0.00100135805f,
   -0.000372517294f,1.f,-0.0318373139f,-0.644541065f,-0.0902808493f,
   0.548595753f,-0.0177664773f,0.630366864f,13.0947766f,1.78754405f,
   8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_6_rowPtr[] = {
   0,1,2,3,3,4,5,5
};
static const size_t PM0_Bd0_6_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_6_data[] _ALIGN = {
   -0.0168911093f,-0.0645302154f,-7.09700122e-05f,-0.0156440682f,0.309743595f
};
static const size_t PM0_Bd1_6_rowPtr[] = {
   0,1,2,3,3,4,5,5
};
static const size_t PM0_Bd1_6_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_6_data[] _ALIGN = {
   -0.0174828214f,-0.0325965701f,-3.58566018e-05f,-0.0161932457f,0.320623269f
};
static const size_t PM0_C_0_6_rowPtr[] = {
   0,0,5,6,6,9
};
static const size_t PM0_C_0_6_colIdx[] = {
   1,2,3,4,5,5,3,4,5
};
static const float PM0_C_0_6_data[] _ALIGN = {
   0.0195667642f,-1.59482963f,0.000195667642f,0.000978338209f,3.87421931e-05f,
   -1.f,1.f,5.f,0.198f
};
static const size_t PM0_D_0_6_rowPtr[] = {
   0,0,1,1,1,1
};
static const size_t PM0_D_0_6_colIdx[] = {
   0
};
static const float PM0_D_0_6_data[] _ALIGN = {
   0.0195667642f
};
static void PM0_collision_6()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.155751443f*x[5]+0.175318207f*x[6];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0391335283f*x[5]-0.0191754289f*x[6];
   tmpX[5] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.77484386f*
             x[5]+1.36967349f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = 0.;
}
static size_t PM0_natPreComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (-x[1]+81.5070707f*x[2]-0.01f*x[3]-0.05f*x[4]-0.00198f*x[5]-u[0] >=
          0)
      {
         return 2; /* 2_0 */
      }
      else
      {
         return 8; /* 10_0 */
      }
   }
   return 5; /* 6_0 */
}
static size_t PM0_natPostComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5]-0.35f*x[6] > 0)
   {
      if (x[0]+468.655057f*x[1]-38198.7009f*x[2]+3.68655057f*x[3]+18.4327529f*
          x[4]+0.729937014f*x[5]+0.821637644f*x[6]+468.655057f*u[0] > 0)
      {
         return 11; /* 14_0 */
      }
   }
   return 5; /* 6_0 */
}
static size_t PM0_forcedComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         return 5; /* 6_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]-x[3]-5.f*x[4]-0.453535354f*x[5]-0.35f*x[6] > 0)
         {
            if (-x[0]-468.655057f*x[1]+38198.7009f*x[2]-3.68655057f*x[3]-
                18.4327529f*x[4]-0.729937014f*x[5]-0.821637644f*x[6]+
                468.655057f*
                u[0] >= 0)
            {
               return 4; /* 5_0 */
            }
            else
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 6_0";
   return 5; /* 6_0 */
}
static const size_t PM0_Ad_8_rowPtr[] = {
   0,0,1,3,5,8,8,10
};
static const size_t PM0_Ad_8_colIdx[] = {
   1,2,6,4,6,2,4,6,2,6
};
static const float PM0_Ad_8_data[] _ALIGN = {
   1.f,0.998410498f,0.000333082641f,-5.f,-0.198f,0.061087776f,1.f,
   1.01839953e-05f,-1.54262061f,0.999742828f
};
static const size_t PM0_Bd0_8_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_8_colIdx[] = {
   0
};
static const float PM0_Bd0_8_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_8_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_8_colIdx[] = {
   0
};
static const float PM0_Bd1_8_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_8_rowPtr[] = {
   0,1,1,1,2,2
};
static const size_t PM0_C_0_8_colIdx[] = {
   2,6
};
static const float PM0_C_0_8_data[] _ALIGN = {
   -1.95368655f,1.f
};
static const size_t PM0_D_0_8_rowPtr[] = {
   0,0,0,0,0,0
};
static const size_t PM0_D_0_8_colIdx[] = {
   0
};
static const float PM0_D_0_8_data[] _ALIGN = {
   0
};
static void PM0_collision_8()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.926268989f*x[3]-3.63134494f*x[4]-0.181567247f*x[5]-
             0.18340126f*x[6];
   tmpX[6] = 18.340126f*x[3]+91.7006299f*x[4]+4.58503149f*x[5]+4.63134494f*
             x[6];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = 0.;
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_8_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[2] >= 0)
   {
      if (-x[6] >= 0)
      {
         return 0; /* 0_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 3; /* 4_0 */
      }
   }
   return 6; /* 8_0 */
}
static size_t PM0_natPostComm_8_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[2] > 0)
   {
      if (x[3]+5.f*x[4]+0.25f*x[5]+0.252525253f*x[6] > 0)
      {
         return 9; /* 12_0 */
      }
   }
   return 6; /* 8_0 */
}
static size_t PM0_forcedComm_8_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 6; /* 8_0 */
      }
      else
      {
         if (x[3]+5.f*x[4]+0.25f*x[5]+0.252525253f*x[6] > 0)
         {
            if (x[1]+81.5070707f*x[2]+u[0] >= 0)
            {
               return 8; /* 10_0 */
            }
            else
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[1]+81.5070707f*x[2]-u[0] >= 0)
         {
            if (x[3]+5.f*x[4]+0.25f*x[5]+0.252525253f*x[6] > 0)
            {
               return 7; /* 9_0 */
            }
         }
         else
         {
            if (x[3]+5.f*x[4]+0.25f*x[5]+0.252525253f*x[6] > 0)
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 8_0";
   return 6; /* 8_0 */
}
static const size_t PM0_Ad_9_rowPtr[] = {
   0,5,10,15,16,21,21,26
};
static const size_t PM0_Ad_9_colIdx[] = {
   1,2,3,4,6,1,2,3,4,6,1,2,3,4,6,3,1,2,3,4,6,1,2,3,4,6
};
static const float PM0_Ad_9_data[] _ALIGN = {
   -0.0343739307f,0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   0.000106826614f,0.996452246f,0.00020027161f,0.00100135805f,0.000372517294f,
   1.f,-0.0318373139f,0.644541065f,-0.0902808493f,0.548595753f,-0.0177664773f,
   0.630366864f,-13.0947766f,1.78754405f,8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_9_rowPtr[] = {
   0,1,2,3,3,4,4,5
};
static const size_t PM0_Bd0_9_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_9_data[] _ALIGN = {
   0.0168911093f,0.0645302154f,-7.09700122e-05f,0.0156440682f,-0.309743595f
};
static const size_t PM0_Bd1_9_rowPtr[] = {
   0,1,2,3,3,4,4,5
};
static const size_t PM0_Bd1_9_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_9_data[] _ALIGN = {
   0.0174828214f,0.0325965701f,-3.58566018e-05f,0.0161932457f,-0.320623269f
};
static const size_t PM0_C_0_9_rowPtr[] = {
   0,5,5,5,6,9
};
static const size_t PM0_C_0_9_colIdx[] = {
   1,2,3,4,6,6,3,4,6
};
static const float PM0_C_0_9_data[] _ALIGN = {
   -0.0195667642f,-1.59482963f,-0.000195667642f,-0.000978338209f,
   -3.87421931e-05f,1.f,1.f,5.f,0.198f
};
static const size_t PM0_D_0_9_rowPtr[] = {
   0,1,1,1,1,1
};
static const size_t PM0_D_0_9_colIdx[] = {
   0
};
static const float PM0_D_0_9_data[] _ALIGN = {
   0.0195667642f
};
static void PM0_collision_9()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.175318207f*x[5]+0.155751443f*x[6];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0191754289f*x[5]-0.0391335283f*x[6];
   tmpX[6] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.36967349f*
             x[5]+1.77484386f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[1]+81.5070707f*x[2]+0.01f*x[3]+0.05f*x[4]+0.00198f*x[6]-u[0] >= 0)
   {
      if (-x[6] >= 0)
      {
         return 1; /* 1_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 4; /* 5_0 */
      }
   }
   return 7; /* 9_0 */
}
static size_t PM0_natPostComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[0]-468.655057f*x[1]-38198.7009f*x[2]-3.68655057f*x[3]-18.4327529f*
       x[4]-0.821637644f*x[5]-0.729937014f*x[6]+468.655057f*u[0] > 0)
   {
      if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
      {
         return 10; /* 13_0 */
      }
   }
   return 7; /* 9_0 */
}
static size_t PM0_forcedComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 7; /* 9_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]+468.655057f*x[1]+38198.7009f*x[2]+3.68655057f*x[3]+
             18.4327529f*x[4]+0.821637644f*x[5]+0.729937014f*x[6]+468.655057f*
             u[0] >= 0)
         {
            if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
            {
               return 8; /* 10_0 */
            }
         }
         else
         {
            if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 9_0";
   return 7; /* 9_0 */
}
static const size_t PM0_Ad_10_rowPtr[] = {
   0,5,10,15,16,21,21,26
};
static const size_t PM0_Ad_10_colIdx[] = {
   1,2,3,4,6,1,2,3,4,6,1,2,3,4,6,3,1,2,3,4,6,1,2,3,4,6
};
static const float PM0_Ad_10_data[] _ALIGN = {
   -0.0343739307f,0.629939557f,0.902529475f,4.51264738f,0.178807663f,
   0.902873215f,1.78044357f,5.37349223f,26.8674612f,1.06415067f,
   0.000106826614f,0.996452246f,0.00020027161f,0.00100135805f,0.000372517294f,
   1.f,-0.0318373139f,0.644541065f,-0.0902808493f,0.548595753f,-0.0177664773f,
   0.630366864f,-13.0947766f,1.78754405f,8.93772025f,1.35171742f
};
static const size_t PM0_Bd0_10_rowPtr[] = {
   0,1,2,3,3,4,4,5
};
static const size_t PM0_Bd0_10_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_10_data[] _ALIGN = {
   -0.0168911093f,-0.0645302154f,7.09700122e-05f,-0.0156440682f,0.309743595f
};
static const size_t PM0_Bd1_10_rowPtr[] = {
   0,1,2,3,3,4,4,5
};
static const size_t PM0_Bd1_10_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_10_data[] _ALIGN = {
   -0.0174828214f,-0.0325965701f,3.58566018e-05f,-0.0161932457f,0.320623269f
};
static const size_t PM0_C_0_10_rowPtr[] = {
   0,5,5,5,6,9
};
static const size_t PM0_C_0_10_colIdx[] = {
   1,2,3,4,6,6,3,4,6
};
static const float PM0_C_0_10_data[] _ALIGN = {
   -0.0195667642f,-1.59482963f,-0.000195667642f,-0.000978338209f,
   -3.87421931e-05f,1.f,1.f,5.f,0.198f
};
static const size_t PM0_D_0_10_rowPtr[] = {
   0,1,1,1,1,1
};
static const size_t PM0_D_0_10_colIdx[] = {
   0
};
static const float PM0_D_0_10_data[] _ALIGN = {
   -0.0195667642f
};
static void PM0_collision_10()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.213376552f*x[0]+0.786623448f*x[3]+3.93311724f*x[4]+
             0.175318207f*x[5]+0.155751443f*x[6];
   tmpX[4] = 0.197644083f*x[0]-0.197644083f*x[3]+0.0117795873f*x[4]-
             0.0191754289f*x[5]-0.0391335283f*x[6];
   tmpX[6] = -3.91335283f*x[0]+3.91335283f*x[3]+19.5667642f*x[4]+1.36967349f*
             x[5]+1.77484386f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = 0.;
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_10_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[1]+81.5070707f*x[2]+0.01f*x[3]+0.05f*x[4]+0.00198f*x[6]+u[0] >= 0)
   {
      if (-x[6] >= 0)
      {
         return 2; /* 2_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 5; /* 6_0 */
      }
   }
   return 8; /* 10_0 */
}
static size_t PM0_natPostComm_10_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (-x[0]-468.655057f*x[1]-38198.7009f*x[2]-3.68655057f*x[3]-18.4327529f*
       x[4]-0.821637644f*x[5]-0.729937014f*x[6]-468.655057f*u[0] > 0)
   {
      if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
      {
         return 11; /* 14_0 */
      }
   }
   return 8; /* 10_0 */
}
static size_t PM0_forcedComm_10_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         return 8; /* 10_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]+468.655057f*x[1]+38198.7009f*x[2]+3.68655057f*x[3]+
             18.4327529f*x[4]+0.821637644f*x[5]+0.729937014f*x[6]-468.655057f*
             u[0] >= 0)
         {
            if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
            {
               return 7; /* 9_0 */
            }
         }
         else
         {
            if (-x[0]+x[3]+5.f*x[4]+0.35f*x[5]+0.453535354f*x[6] > 0)
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 10_0";
   return 8; /* 10_0 */
}
static const size_t PM0_Ad_12_rowPtr[] = {
   0,0,1,4,7,8,11,14
};
static const size_t PM0_Ad_12_colIdx[] = {
   1,2,5,6,4,5,6,4,2,5,6,2,5,6
};
static const float PM0_Ad_12_data[] _ALIGN = {
   1.f,0.987586859f,-0.000331878834f,0.000331878834f,-5.f,-0.198f,-0.198f,1.f,
   33.1878834f,0.994457187f,0.00554281302f,-33.1878834f,0.00554281302f,
   0.994457187f
};
static const size_t PM0_Bd0_12_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_12_colIdx[] = {
   0
};
static const float PM0_Bd0_12_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_12_rowPtr[] = {
   0,0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_12_colIdx[] = {
   0
};
static const float PM0_Bd1_12_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_12_rowPtr[] = {
   0,0,0,1,2,2
};
static const size_t PM0_C_0_12_colIdx[] = {
   5,6
};
static const float PM0_C_0_12_data[] _ALIGN = {
   -1.f,1.f
};
static const size_t PM0_D_0_12_rowPtr[] = {
   0,0,0,0,0,0
};
static const size_t PM0_D_0_12_colIdx[] = {
   0
};
static const float PM0_D_0_12_data[] _ALIGN = {
   0
};
static void PM0_collision_12()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[4] = -0.943485682f*x[3]-3.71742841f*x[4]-0.186810165f*x[5]-
             0.186810165f*x[6];
   tmpX[5] = 9.38744548f*x[3]+46.9372274f*x[4]+2.8587142f*x[5]+1.8587142f*
             x[6];
   tmpX[6] = 9.38744548f*x[3]+46.9372274f*x[4]+1.8587142f*x[5]+2.8587142f*
             x[6];
   x[0] = 0.;
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_12_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (x[6] > 0)
      {
         return 6; /* 8_0 */
      }
      else
      {
         return 0; /* 0_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 3; /* 4_0 */
      }
   }
   return 9; /* 12_0 */
}
static size_t PM0_natPostComm_12_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 9; /* 12_0 */
}
static size_t PM0_forcedComm_12_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 9; /* 12_0 */
      }
      else
      {
         if (-x[3]-5.f*x[4]-0.304525253f*x[5]-0.198f*x[6] > 0)
         {
            if (x[3]+5.f*x[4]+0.198f*x[5]+0.304525253f*x[6] > 0)
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (-x[3]-5.f*x[4]-0.304525253f*x[5]-0.198f*x[6] > 0)
         {
            if (x[3]+5.f*x[4]+0.198f*x[5]+0.304525253f*x[6] > 0)
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 12_0";
   return 9; /* 12_0 */
}
static const size_t PM0_Ad_13_rowPtr[] = {
   0,5,10,16,17,23,29,35
};
static const size_t PM0_Ad_13_colIdx[] = {
   1,3,4,5,6,1,3,4,5,6,1,2,3,4,5,6,3,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6
};
static const float PM0_Ad_13_data[] _ALIGN = {
   -0.0418194605f,0.881005008f,4.40502504f,0.174438992f,0.174438992f,
   0.881423203f,5.33297918f,26.6648959f,1.05592988f,1.05592988f,
   -5.64237288e-34f,0.987586859f,-1.56933198e-33f,-5.6935304e-33f,
   -0.000331878834f,0.000331878834f,1.f,-0.0394560622f,-3.08148791e-33f,
   -0.112270071f,0.438649645f,-0.0222294741f,-0.0222294741f,0.392577905f,
   33.1878834f,1.117059f,5.58529499f,1.21563487f,0.226720495f,0.392577905f,
   -33.1878834f,1.117059f,5.58529499f,0.226720495f,1.21563487f
};
static const size_t PM0_Bd0_13_rowPtr[] = {
   0,1,2,3,3,4,5,6
};
static const size_t PM0_Bd0_13_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd0_13_data[] _ALIGN = {
   0.020475637f,0.0787264884f,2.36227345e-34f,0.0193184703f,-0.192213926f,
   -0.192213926f
};
static const size_t PM0_Bd1_13_rowPtr[] = {
   0,1,2,3,3,4,5,6
};
static const size_t PM0_Bd1_13_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd1_13_data[] _ALIGN = {
   0.0213438235f,0.0398503089f,-6.13137853e-35f,0.0201375919f,-0.20036398f,
   -0.20036398f
};
static const size_t PM0_C_0_13_rowPtr[] = {
   0,0,0,1,2,6
};
static const size_t PM0_C_0_13_colIdx[] = {
   5,6,3,4,5,6
};
static const float PM0_C_0_13_data[] _ALIGN = {
   -1.f,1.f,1.f,5.f,0.198f,0.198f
};
static const size_t PM0_D_0_13_rowPtr[] = {
   0,0,0,0,0,0
};
static const size_t PM0_D_0_13_colIdx[] = {
   0
};
static const float PM0_D_0_13_data[] _ALIGN = {
   0
};
static void PM0_collision_13()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.261388985f*x[0]+0.738611015f*x[3]+3.69305507f*x[4]+
             0.146244981f*x[5]+0.146244981f*x[6];
   tmpX[4] = 0.246616765f*x[0]-0.246616765f*x[3]-0.233083825f*x[4]-
             0.0488301195f*x[5]-0.0488301195f*x[6];
   tmpX[5] = -2.45377485f*x[0]+2.45377485f*x[3]+12.2688742f*x[4]+1.48584742f*
             x[5]+0.48584742f*x[6];
   tmpX[6] = -2.45377485f*x[0]+2.45377485f*x[3]+12.2688742f*x[4]+0.48584742f*
             x[5]+1.48584742f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_13_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (x[6] > 0)
      {
         return 7; /* 9_0 */
      }
      else
      {
         return 1; /* 1_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 4; /* 5_0 */
      }
   }
   return 10; /* 13_0 */
}
static size_t PM0_natPostComm_13_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 10; /* 13_0 */
}
static size_t PM0_forcedComm_13_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (Subsystem_PM0_gateSignalBuffer[0])
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 10; /* 13_0 */
      }
   }
   else
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]-x[3]-5.f*x[4]-0.605535354f*x[5]-0.198f*x[6] > 0)
         {
            if (-x[0]+x[3]+5.f*x[4]+0.198f*x[5]+0.605535354f*x[6] > 0)
            {
               return 11; /* 14_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 13_0";
   return 10; /* 13_0 */
}
static const size_t PM0_Ad_14_rowPtr[] = {
   0,5,10,16,17,23,29,35
};
static const size_t PM0_Ad_14_colIdx[] = {
   1,3,4,5,6,1,3,4,5,6,1,2,3,4,5,6,3,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6
};
static const float PM0_Ad_14_data[] _ALIGN = {
   -0.0418194605f,0.881005008f,4.40502504f,0.174438992f,0.174438992f,
   0.881423203f,5.33297918f,26.6648959f,1.05592988f,1.05592988f,
   -5.64237288e-34f,0.987586859f,-1.56933198e-33f,-5.6935304e-33f,
   -0.000331878834f,0.000331878834f,1.f,-0.0394560622f,-3.08148791e-33f,
   -0.112270071f,0.438649645f,-0.0222294741f,-0.0222294741f,0.392577905f,
   33.1878834f,1.117059f,5.58529499f,1.21563487f,0.226720495f,0.392577905f,
   -33.1878834f,1.117059f,5.58529499f,0.226720495f,1.21563487f
};
static const size_t PM0_Bd0_14_rowPtr[] = {
   0,1,2,3,3,4,5,6
};
static const size_t PM0_Bd0_14_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd0_14_data[] _ALIGN = {
   -0.020475637f,-0.0787264884f,-2.36227345e-34f,-0.0193184703f,0.192213926f,
   0.192213926f
};
static const size_t PM0_Bd1_14_rowPtr[] = {
   0,1,2,3,3,4,5,6
};
static const size_t PM0_Bd1_14_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd1_14_data[] _ALIGN = {
   -0.0213438235f,-0.0398503089f,6.13137853e-35f,-0.0201375919f,0.20036398f,
   0.20036398f
};
static const size_t PM0_C_0_14_rowPtr[] = {
   0,0,0,1,2,6
};
static const size_t PM0_C_0_14_colIdx[] = {
   5,6,3,4,5,6
};
static const float PM0_C_0_14_data[] _ALIGN = {
   -1.f,1.f,1.f,5.f,0.198f,0.198f
};
static const size_t PM0_D_0_14_rowPtr[] = {
   0,0,0,0,0,0
};
static const size_t PM0_D_0_14_colIdx[] = {
   0
};
static const float PM0_D_0_14_data[] _ALIGN = {
   0
};
static void PM0_collision_14()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[0] = 0.261388985f*x[0]+0.738611015f*x[3]+3.69305507f*x[4]+
             0.146244981f*x[5]+0.146244981f*x[6];
   tmpX[4] = 0.246616765f*x[0]-0.246616765f*x[3]-0.233083825f*x[4]-
             0.0488301195f*x[5]-0.0488301195f*x[6];
   tmpX[5] = -2.45377485f*x[0]+2.45377485f*x[3]+12.2688742f*x[4]+1.48584742f*
             x[5]+0.48584742f*x[6];
   tmpX[6] = -2.45377485f*x[0]+2.45377485f*x[3]+12.2688742f*x[4]+0.48584742f*
             x[5]+1.48584742f*x[6];
   x[0] = tmpX[0];
   x[4] = tmpX[4];
   x[5] = tmpX[5];
   x[6] = tmpX[6];
}
static size_t PM0_natPreComm_14_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (x[6] > 0)
      {
         return 8; /* 10_0 */
      }
      else
      {
         return 2; /* 2_0 */
      }
   }
   else
   {
      if (-x[6] >= 0)
      {
         return 5; /* 6_0 */
      }
   }
   return 11; /* 14_0 */
}
static size_t PM0_natPostComm_14_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   return 11; /* 14_0 */
}
static size_t PM0_forcedComm_14_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (!Subsystem_PM0_gateSignalBuffer[0])
   {
      if (Subsystem_PM0_gateSignalBuffer[1])
      {
         return 11; /* 14_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (x[0]-x[3]-5.f*x[4]-0.605535354f*x[5]-0.198f*x[6] > 0)
         {
            if (-x[0]+x[3]+5.f*x[4]+0.198f*x[5]+0.605535354f*x[6] > 0)
            {
               return 10; /* 13_0 */
            }
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 14_0";
   return 11; /* 14_0 */
}
static const size_t * const PM0_Ad_rowPtr[] = {
   PM0_Ad_0_rowPtr,PM0_Ad_1_rowPtr,PM0_Ad_2_rowPtr,PM0_Ad_4_rowPtr,
   PM0_Ad_5_rowPtr,PM0_Ad_6_rowPtr,PM0_Ad_8_rowPtr,PM0_Ad_9_rowPtr,
   PM0_Ad_10_rowPtr,PM0_Ad_12_rowPtr,PM0_Ad_13_rowPtr,PM0_Ad_14_rowPtr
};
static const size_t * const PM0_Ad_colIdx[] = {
   PM0_Ad_0_colIdx,PM0_Ad_1_colIdx,PM0_Ad_2_colIdx,PM0_Ad_4_colIdx,
   PM0_Ad_5_colIdx,PM0_Ad_6_colIdx,PM0_Ad_8_colIdx,PM0_Ad_9_colIdx,
   PM0_Ad_10_colIdx,PM0_Ad_12_colIdx,PM0_Ad_13_colIdx,PM0_Ad_14_colIdx
};
static const float * const Subsystem_PM0_Ad_data[] = {
   PM0_Ad_0_data,PM0_Ad_1_data,PM0_Ad_2_data,PM0_Ad_4_data,PM0_Ad_5_data,
   PM0_Ad_6_data,PM0_Ad_8_data,PM0_Ad_9_data,PM0_Ad_10_data,PM0_Ad_12_data,
   PM0_Ad_13_data,PM0_Ad_14_data
};
static const size_t * const PM0_Bd0_rowPtr[] = {
   PM0_Bd0_0_rowPtr,PM0_Bd0_1_rowPtr,PM0_Bd0_2_rowPtr,PM0_Bd0_4_rowPtr,
   PM0_Bd0_5_rowPtr,PM0_Bd0_6_rowPtr,PM0_Bd0_8_rowPtr,PM0_Bd0_9_rowPtr,
   PM0_Bd0_10_rowPtr,PM0_Bd0_12_rowPtr,PM0_Bd0_13_rowPtr,PM0_Bd0_14_rowPtr
};
static const size_t * const PM0_Bd0_colIdx[] = {
   PM0_Bd0_0_colIdx,PM0_Bd0_1_colIdx,PM0_Bd0_2_colIdx,PM0_Bd0_4_colIdx,
   PM0_Bd0_5_colIdx,PM0_Bd0_6_colIdx,PM0_Bd0_8_colIdx,PM0_Bd0_9_colIdx,
   PM0_Bd0_10_colIdx,PM0_Bd0_12_colIdx,PM0_Bd0_13_colIdx,PM0_Bd0_14_colIdx
};
static const float * const Subsystem_PM0_Bd0_data[] = {
   PM0_Bd0_0_data,PM0_Bd0_1_data,PM0_Bd0_2_data,PM0_Bd0_4_data,PM0_Bd0_5_data,
   PM0_Bd0_6_data,PM0_Bd0_8_data,PM0_Bd0_9_data,PM0_Bd0_10_data,
   PM0_Bd0_12_data,PM0_Bd0_13_data,PM0_Bd0_14_data
};
static const size_t * const PM0_Bd1_rowPtr[] = {
   PM0_Bd1_0_rowPtr,PM0_Bd1_1_rowPtr,PM0_Bd1_2_rowPtr,PM0_Bd1_4_rowPtr,
   PM0_Bd1_5_rowPtr,PM0_Bd1_6_rowPtr,PM0_Bd1_8_rowPtr,PM0_Bd1_9_rowPtr,
   PM0_Bd1_10_rowPtr,PM0_Bd1_12_rowPtr,PM0_Bd1_13_rowPtr,PM0_Bd1_14_rowPtr
};
static const size_t * const PM0_Bd1_colIdx[] = {
   PM0_Bd1_0_colIdx,PM0_Bd1_1_colIdx,PM0_Bd1_2_colIdx,PM0_Bd1_4_colIdx,
   PM0_Bd1_5_colIdx,PM0_Bd1_6_colIdx,PM0_Bd1_8_colIdx,PM0_Bd1_9_colIdx,
   PM0_Bd1_10_colIdx,PM0_Bd1_12_colIdx,PM0_Bd1_13_colIdx,PM0_Bd1_14_colIdx
};
static const float * const Subsystem_PM0_Bd1_data[] = {
   PM0_Bd1_0_data,PM0_Bd1_1_data,PM0_Bd1_2_data,PM0_Bd1_4_data,PM0_Bd1_5_data,
   PM0_Bd1_6_data,PM0_Bd1_8_data,PM0_Bd1_9_data,PM0_Bd1_10_data,
   PM0_Bd1_12_data,PM0_Bd1_13_data,PM0_Bd1_14_data
};
static const size_t * const PM0_C_0_rowPtr[] = {
   PM0_C_0_0_rowPtr,PM0_C_0_1_rowPtr,PM0_C_0_2_rowPtr,PM0_C_0_4_rowPtr,
   PM0_C_0_5_rowPtr,PM0_C_0_6_rowPtr,PM0_C_0_8_rowPtr,PM0_C_0_9_rowPtr,
   PM0_C_0_10_rowPtr,PM0_C_0_12_rowPtr,PM0_C_0_13_rowPtr,PM0_C_0_14_rowPtr
};
static const size_t * const PM0_C_0_colIdx[] = {
   PM0_C_0_0_colIdx,PM0_C_0_1_colIdx,PM0_C_0_2_colIdx,PM0_C_0_4_colIdx,
   PM0_C_0_5_colIdx,PM0_C_0_6_colIdx,PM0_C_0_8_colIdx,PM0_C_0_9_colIdx,
   PM0_C_0_10_colIdx,PM0_C_0_12_colIdx,PM0_C_0_13_colIdx,PM0_C_0_14_colIdx
};
static const float * const Subsystem_PM0_C_0_data[] = {
   PM0_C_0_0_data,PM0_C_0_1_data,PM0_C_0_2_data,PM0_C_0_4_data,PM0_C_0_5_data,
   PM0_C_0_6_data,PM0_C_0_8_data,PM0_C_0_9_data,PM0_C_0_10_data,
   PM0_C_0_12_data,PM0_C_0_13_data,PM0_C_0_14_data
};
static const size_t * const PM0_D_0_rowPtr[] = {
   PM0_D_0_0_rowPtr,PM0_D_0_1_rowPtr,PM0_D_0_2_rowPtr,PM0_D_0_4_rowPtr,
   PM0_D_0_5_rowPtr,PM0_D_0_6_rowPtr,PM0_D_0_8_rowPtr,PM0_D_0_9_rowPtr,
   PM0_D_0_10_rowPtr,PM0_D_0_12_rowPtr,PM0_D_0_13_rowPtr,PM0_D_0_14_rowPtr
};
static const size_t * const PM0_D_0_colIdx[] = {
   PM0_D_0_0_colIdx,PM0_D_0_1_colIdx,PM0_D_0_2_colIdx,PM0_D_0_4_colIdx,
   PM0_D_0_5_colIdx,PM0_D_0_6_colIdx,PM0_D_0_8_colIdx,PM0_D_0_9_colIdx,
   PM0_D_0_10_colIdx,PM0_D_0_12_colIdx,PM0_D_0_13_colIdx,PM0_D_0_14_colIdx
};
static const float * const Subsystem_PM0_D_0_data[] = {
   PM0_D_0_0_data,PM0_D_0_1_data,PM0_D_0_2_data,PM0_D_0_4_data,PM0_D_0_5_data,
   PM0_D_0_6_data,PM0_D_0_8_data,PM0_D_0_9_data,PM0_D_0_10_data,
   PM0_D_0_12_data,PM0_D_0_13_data,PM0_D_0_14_data
};
static void (*const PM0_collision[12]) () = {
   PM0_collision_0,PM0_collision_1,PM0_collision_2,PM0_collision_4,
   PM0_collision_5,PM0_collision_6,PM0_collision_8,PM0_collision_9,
   PM0_collision_10,PM0_collision_12,PM0_collision_13,PM0_collision_14
};
static size_t (*const PM0_natPreComm[12]) () = {
   PM0_natPreComm_0_0,PM0_natPreComm_1_0,PM0_natPreComm_2_0,
   PM0_natPreComm_4_0,PM0_natPreComm_5_0,PM0_natPreComm_6_0,
   PM0_natPreComm_8_0,PM0_natPreComm_9_0,PM0_natPreComm_10_0,
   PM0_natPreComm_12_0,PM0_natPreComm_13_0,PM0_natPreComm_14_0
};
static size_t (*const PM0_natPostComm[12]) () = {
   PM0_natPostComm_0_0,PM0_natPostComm_1_0,PM0_natPostComm_2_0,
   PM0_natPostComm_4_0,PM0_natPostComm_5_0,PM0_natPostComm_6_0,
   PM0_natPostComm_8_0,PM0_natPostComm_9_0,PM0_natPostComm_10_0,
   PM0_natPostComm_12_0,PM0_natPostComm_13_0,PM0_natPostComm_14_0
};
static size_t (*const PM0_forcedComm[12]) () = {
   PM0_forcedComm_0_0,PM0_forcedComm_1_0,PM0_forcedComm_2_0,
   PM0_forcedComm_4_0,PM0_forcedComm_5_0,PM0_forcedComm_6_0,
   PM0_forcedComm_8_0,PM0_forcedComm_9_0,PM0_forcedComm_10_0,
   PM0_forcedComm_12_0,PM0_forcedComm_13_0,PM0_forcedComm_14_0
};
static size_t Subsystem_PM0_conductionMasks[12]={
   0,1,2,4,5,6,8,9,10,12,13,14
};
static size_t Subsystem_PM0_directionMasks[12]={
   0,0,0,0,0,0,0,0,0,0,0,0
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
      1,2,3,4,5
   };
   float y[5] _ALIGN;
   size_t i;
   for (i = 0; i < 5; ++i)
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
   for (i = 0; i < 5; ++i)
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
   for (i = 0; i < 7; ++i)
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
   "531d73db5d84d2fc1d6b759cc3f3c8de9ccfe1b7";
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
   Subsystem_PM0_topoIdx = 0;
   Subsystem_X.Subsystem_PM0_x[0] = 0;
   Subsystem_X.Subsystem_PM0_x[1] = 0;
   Subsystem_X.Subsystem_PM0_x[2] = 0;
   Subsystem_X.Subsystem_PM0_x[3] = 0;
   Subsystem_X.Subsystem_PM0_x[4] = 0;
   Subsystem_X.Subsystem_PM0_x[5] = 0;
   Subsystem_X.Subsystem_PM0_x[6] = 0;
   Subsystem_PM0_x = &Subsystem_X.Subsystem_PM0_x[0];
   Subsystem_first = 1;
}

void Subsystem_output(void)
{
   if (Subsystem_errorStatus)
   {
      return;
   }

   /* Data Type : 'Subsystem/Data Type' */
   if (Subsystem_U.SW1 < 0.f || Subsystem_U.SW1 > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type'";
   }
   else
   {
      Subsystem_B.DataType = (bool)Subsystem_U.SW1;
   }
   /* Data Type : 'Subsystem/Data Type1' */
   if (Subsystem_U.SW2 < 0.f || Subsystem_U.SW2 > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type1'";
   }
   else
   {
      Subsystem_B.DataType1 = (bool)Subsystem_U.SW2;
   }


   /* Electrical model */


   /* Electrical model input */
   /* Voltage Source DC : 'Subsystem/V_dc' */
   Subsystem_PM0_u[0]=600.f;
   /* End of electrical model input */
   if (!Subsystem_first)
   {
      memcpy(Subsystem_PM0_prevX,Subsystem_PM0_x,7*sizeof(float));
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
   Subsystem_PM0_y[0] = 1.f*Subsystem_PM0_x[2];
   /* End of electrical model output */

   /* End of electrical model */


   /* Global output signals */
   Subsystem_Y.VMOut = Subsystem_PM0_y[0];
   Subsystem_Y.VMD1 = Subsystem_PM0_y[1];
   Subsystem_Y.VMD2 = Subsystem_PM0_y[2];
   Subsystem_Y.AMLr = Subsystem_PM0_y[5];
   Subsystem_Y.AMD1 = Subsystem_PM0_y[3];
   Subsystem_Y.AMD2 = Subsystem_PM0_y[4];

   Subsystem_first = 0;
}

void Subsystem_update(void)
{
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
