/*
 * Implementation file for: half-bridge-switch-subsystem/Subsystem
 * Generated with         : PLECS 4.9.2
 * Generated on           : 8 Apr 2025 10:50:31
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
static float Subsystem_PM0_y[14] _ALIGN;
static float Subsystem_PM0_gateSignalBuffer[2] _ALIGN;
static size_t Subsystem_PM0_topoIdx;
static char Subsystem_PM0_withDiracs;
static const size_t PM0_Ad_0_rowPtr[] = {
   0,1,1,1,1,1,2
};
static const size_t PM0_Ad_0_colIdx[] = {
   0,5
};
static const float PM0_Ad_0_data[] _ALIGN = {
   1.f,0.999305797f
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
   0,0,0,0,0,0,1,2,2,2,3,4,4
};
static const size_t PM0_C_0_0_colIdx[] = {
   5,5,0,0
};
static const float PM0_C_0_0_data[] _ALIGN = {
   -1.f,-1.f,-1.f,1.f
};
static const size_t PM0_D_0_0_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_0_colIdx[] = {
   0
};
static const float PM0_D_0_0_data[] _ALIGN = {
   1.f
};
static void PM0_collision_0()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   x[1] = 0.;
   x[2] = 0.;
   x[3] = 0.;
   x[4] = 0.;
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
   if (-x[5] > 0)
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
            const char cond6 = x[0]+20.8614554f*x[5] >= 0;
            if (cond6)
            {
               if (-x[0]+20.8614554f*x[5] >= 0)
               {
                  return 2; /* 2_0 */
               }
            }
            else if (!cond6)
            {
               if (-1.f*x[0]+784.074251f*x[5] >= 0)
               {
                  return 5; /* 6_0 */
               }
            }
            if (1.f*x[0]+784.074251f*x[5] >= 0)
            {
               if (x[0]-20.8614554f*x[5] > 0)
               {
                  return 8; /* 10_0 */
               }
            }
            else
            {
               if (1.f*x[0]-784.074251f*x[5] > 0)
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
            const char cond2 = x[0]+20.8614554f*x[5]-u[0] >= 0;
            if (cond2)
            {
               if (-x[0]+20.8614554f*x[5]+u[0] >= 0)
               {
                  return 1; /* 1_0 */
               }
            }
            else if (!cond2)
            {
               if (-1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0)
               {
                  return 4; /* 5_0 */
               }
            }
            if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
            {
               if (x[0]-20.8614554f*x[5]-u[0] > 0)
               {
                  return 7; /* 9_0 */
               }
            }
            else
            {
               if (1.f*x[0]-784.074251f*x[5]-1.f*u[0] > 0)
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
   0,2,4,6,6,6,7
};
static const size_t PM0_Ad_1_colIdx[] = {
   0,2,0,2,0,2,5
};
static const float PM0_Ad_1_data[] _ALIGN = {
   0.993199443f,13.8573905f,-0.000978168743f,0.993199443f,-0.000978168743f,
   0.993199443f,0.999305797f
};
static const size_t PM0_Bd0_1_rowPtr[] = {
   0,1,2,3,3,3,3
};
static const size_t PM0_Bd0_1_colIdx[] = {
   0,0,0
};
static const float PM0_Bd0_1_data[] _ALIGN = {
   0.00453267517f,0.000488528619f,0.000488528619f
};
static const size_t PM0_Bd1_1_rowPtr[] = {
   0,1,2,3,3,3,3
};
static const size_t PM0_Bd1_1_colIdx[] = {
   0,0,0
};
static const float PM0_Bd1_1_data[] _ALIGN = {
   0.00226788211f,0.000489640124f,0.000489640124f
};
static const size_t PM0_C_0_1_rowPtr[] = {
   0,0,0,1,2,3,5,7,8,8,8,8,9
};
static const size_t PM0_C_0_1_colIdx[] = {
   0,0,0,0,5,0,5,2,0
};
static const float PM0_C_0_1_data[] _ALIGN = {
   -0.823529412f,-0.0479352941f,0.0479352941f,-0.0479352941f,-1.f,
   0.0479352941f,-1.f,1.f,-0.176470588f
};
static const size_t PM0_D_0_1_rowPtr[] = {
   0,0,0,1,2,3,4,5,5,5,5,6,7
};
static const size_t PM0_D_0_1_colIdx[] = {
   0,0,0,0,0,0,0
};
static const float PM0_D_0_1_data[] _ALIGN = {
   0.823529412f,0.0479352941f,-0.0479352941f,0.0479352941f,-0.0479352941f,1.f,
   0.176470588f
};
static void PM0_collision_1()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.176470588f*x[1]+0.823529412f*x[2]+0.0479352941f*x[3]+
             0.0479352941f*x[4];
   tmpX[2] = 0.176470588f*x[1]+0.823529412f*x[2]+0.0479352941f*x[3]+
             0.0479352941f*x[4];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[3] = 0.;
   x[4] = 0.;
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
      const char cond1 = -1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0;
      if (cond1)
      {
         if (-x[0]-20.8614554f*x[5]+u[0] > 0)
         {
            return 4; /* 5_0 */
         }
      }
      else if (!cond1)
      {
         if (-1.f*x[0]-784.074251f*x[5]+1.f*u[0] > 0)
         {
            return 10; /* 13_0 */
         }
      }
      if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
      {
         if (x[0]-20.8614554f*x[5]-u[0] > 0)
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
            const char cond2 = x[0]+20.8614554f*x[5] >= 0;
            if (cond2)
            {
               if (-x[0]+20.8614554f*x[5] >= 0)
               {
                  return 2; /* 2_0 */
               }
            }
            else if (!cond2)
            {
               if (-1.f*x[0]+784.074251f*x[5] >= 0)
               {
                  return 5; /* 6_0 */
               }
            }
            if (1.f*x[0]+784.074251f*x[5] >= 0)
            {
               if (x[0]-20.8614554f*x[5] > 0)
               {
                  return 8; /* 10_0 */
               }
            }
            else
            {
               if (1.f*x[0]-784.074251f*x[5] > 0)
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
   0,2,4,6,6,6,7
};
static const size_t PM0_Ad_2_colIdx[] = {
   0,2,0,2,0,2,5
};
static const float PM0_Ad_2_data[] _ALIGN = {
   0.993199443f,13.8573905f,-0.000978168743f,0.993199443f,-0.000978168743f,
   0.993199443f,0.999305797f
};
static const size_t PM0_Bd0_2_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_2_colIdx[] = {
   0
};
static const float PM0_Bd0_2_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_2_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_2_colIdx[] = {
   0
};
static const float PM0_Bd1_2_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_2_rowPtr[] = {
   0,0,0,1,2,3,5,7,8,8,8,8,9
};
static const size_t PM0_C_0_2_colIdx[] = {
   0,0,0,0,5,0,5,2,0
};
static const float PM0_C_0_2_data[] _ALIGN = {
   -0.823529412f,-0.0479352941f,0.0479352941f,-0.0479352941f,-1.f,
   0.0479352941f,-1.f,1.f,-0.176470588f
};
static const size_t PM0_D_0_2_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_2_colIdx[] = {
   0
};
static const float PM0_D_0_2_data[] _ALIGN = {
   1.f
};
static void PM0_collision_2()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.176470588f*x[1]+0.823529412f*x[2]+0.0479352941f*x[3]+
             0.0479352941f*x[4];
   tmpX[2] = 0.176470588f*x[1]+0.823529412f*x[2]+0.0479352941f*x[3]+
             0.0479352941f*x[4];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[3] = 0.;
   x[4] = 0.;
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
      const char cond1 = -1.f*x[0]+784.074251f*x[5] >= 0;
      if (cond1)
      {
         if (-x[0]-20.8614554f*x[5] > 0)
         {
            return 5; /* 6_0 */
         }
      }
      else if (!cond1)
      {
         if (-1.f*x[0]-784.074251f*x[5] > 0)
         {
            return 11; /* 14_0 */
         }
      }
      if (1.f*x[0]+784.074251f*x[5] >= 0)
      {
         if (x[0]-20.8614554f*x[5] > 0)
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
            const char cond2 = x[0]+20.8614554f*x[5]-u[0] >= 0;
            if (cond2)
            {
               if (-x[0]+20.8614554f*x[5]+u[0] >= 0)
               {
                  return 1; /* 1_0 */
               }
            }
            else if (!cond2)
            {
               if (-1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0)
               {
                  return 4; /* 5_0 */
               }
            }
            if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
            {
               if (x[0]-20.8614554f*x[5]-u[0] > 0)
               {
                  return 7; /* 9_0 */
               }
            }
            else
            {
               if (1.f*x[0]-784.074251f*x[5]-1.f*u[0] > 0)
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
   0,1,1,1,3,3,5
};
static const size_t PM0_Ad_4_colIdx[] = {
   0,3,5,3,5
};
static const float PM0_Ad_4_data[] _ALIGN = {
   1.f,0.999942622f,0.344226492f,-0.000333211245f,0.999248432f
};
static const size_t PM0_Bd0_4_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_4_colIdx[] = {
   0
};
static const float PM0_Bd0_4_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_4_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_4_colIdx[] = {
   0
};
static const float PM0_Bd1_4_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_4_rowPtr[] = {
   0,1,1,2,3,4,4,5,5,6,8,10,10
};
static const size_t PM0_C_0_4_colIdx[] = {
   3,5,5,5,5,3,0,5,0,5
};
static const float PM0_C_0_4_data[] _ALIGN = {
   -1.f,16.8367769f,1.f,-0.99f,-1.99f,-1.f,-1.f,-16.8367769f,1.f,16.8367769f
};
static const size_t PM0_D_0_4_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_4_colIdx[] = {
   0
};
static const float PM0_D_0_4_data[] _ALIGN = {
   1.f
};
static void PM0_collision_4()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   x[1] = 0.;
   x[2] = 0.;
   x[4] = 0.;
}
static size_t PM0_natPreComm_4_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (x[5] >= 0)
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
   if (-x[3] > 0)
   {
      if (-x[5] > 0)
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
         if (-1.f*x[0]+784.074251f*x[5] >= 0)
         {
            return 5; /* 6_0 */
         }
         else
         {
            return 11; /* 14_0 */
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (-1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0)
         {
            return 4; /* 5_0 */
         }
         else
         {
            return 10; /* 13_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 4_0";
   return 3; /* 4_0 */
}
static const size_t PM0_Ad_5_rowPtr[] = {
   0,4,8,12,16,16,20
};
static const size_t PM0_Ad_5_colIdx[] = {
   0,2,3,5,0,2,3,5,0,2,3,5,0,2,3,5,0,2,3,5
};
static const float PM0_Ad_5_data[] _ALIGN = {
   0.964918508f,13.7260883f,6.57730768e-05f,-0.590516554f,-0.00502177766f,
   0.964918508f,1.41723973e-05f,-0.0845193933f,-0.00502177766f,0.964918508f,
   1.41723973e-05f,-0.0845193933f,0.0845489191f,0.590653581f,0.999704007f,
   1.76723321f,-1.41723973e-05f,-6.57730768e-05f,-0.000333184672f,0.999009872f
};
static const size_t PM0_Bd0_5_rowPtr[] = {
   0,1,2,3,4,4,5
};
static const size_t PM0_Bd0_5_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_5_data[] _ALIGN = {
   0.0233598508f,0.00249591025f,0.00249591025f,-0.0420218612f,9.43673577e-06f
};
static const size_t PM0_Bd1_5_rowPtr[] = {
   0,1,2,3,4,4,5
};
static const size_t PM0_Bd1_5_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_5_data[] _ALIGN = {
   0.011721641f,0.00252586741f,0.00252586741f,-0.0425270579f,4.73566153e-06f
};
static const size_t PM0_C_0_5_rowPtr[] = {
   0,1,1,3,4,6,6,8,9,10,10,10,12
};
static const size_t PM0_C_0_5_colIdx[] = {
   3,0,5,5,0,5,0,5,2,3,0,5
};
static const float PM0_C_0_5_data[] _ALIGN = {
   -1.f,-0.0852851293f,15.4008502f,1.f,0.00248467049f,-0.948166157f,
   0.00248467049f,-1.94816616f,1.f,-1.f,-0.914714871f,-15.4008502f
};
static const size_t PM0_D_0_5_rowPtr[] = {
   0,0,0,1,1,2,2,3,3,3,3,4,5
};
static const size_t PM0_D_0_5_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_D_0_5_data[] _ALIGN = {
   0.0852851293f,-0.00248467049f,-0.00248467049f,1.f,0.914714871f
};
static void PM0_collision_5()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[4];
   tmpX[2] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[4];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[4] = 0.;
}
static size_t PM0_natPreComm_5_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (-1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0)
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
   if (-x[3] > 0)
   {
      if (x[0]-784.074251f*x[5]-u[0] > 0)
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
         if (-1.f*x[0]+784.074251f*x[5] >= 0)
         {
            return 5; /* 6_0 */
         }
         else
         {
            return 11; /* 14_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 5_0";
   return 4; /* 5_0 */
}
static const size_t PM0_Ad_6_rowPtr[] = {
   0,4,8,12,16,16,20
};
static const size_t PM0_Ad_6_colIdx[] = {
   0,2,3,5,0,2,3,5,0,2,3,5,0,2,3,5,0,2,3,5
};
static const float PM0_Ad_6_data[] _ALIGN = {
   0.964918508f,13.7260883f,6.57730768e-05f,-0.590516554f,-0.00502177766f,
   0.964918508f,1.41723973e-05f,-0.0845193933f,-0.00502177766f,0.964918508f,
   1.41723973e-05f,-0.0845193933f,0.0845489191f,0.590653581f,0.999704007f,
   1.76723321f,-1.41723973e-05f,-6.57730768e-05f,-0.000333184672f,0.999009872f
};
static const size_t PM0_Bd0_6_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_6_colIdx[] = {
   0
};
static const float PM0_Bd0_6_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_6_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_6_colIdx[] = {
   0
};
static const float PM0_Bd1_6_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_6_rowPtr[] = {
   0,1,1,3,4,6,6,8,9,10,10,10,12
};
static const size_t PM0_C_0_6_colIdx[] = {
   3,0,5,5,0,5,0,5,2,3,0,5
};
static const float PM0_C_0_6_data[] _ALIGN = {
   -1.f,-0.0852851293f,15.4008502f,1.f,0.00248467049f,-0.948166157f,
   0.00248467049f,-1.94816616f,1.f,-1.f,-0.914714871f,-15.4008502f
};
static const size_t PM0_D_0_6_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_6_colIdx[] = {
   0
};
static const float PM0_D_0_6_data[] _ALIGN = {
   1.f
};
static void PM0_collision_6()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[4];
   tmpX[2] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[4];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[4] = 0.;
}
static size_t PM0_natPreComm_6_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (-1.f*x[0]+784.074251f*x[5] >= 0)
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
   if (-x[3] > 0)
   {
      if (x[0]-784.074251f*x[5] > 0)
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
         if (-1.f*x[0]+784.074251f*x[5]+1.f*u[0] >= 0)
         {
            return 4; /* 5_0 */
         }
         else
         {
            return 10; /* 13_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 6_0";
   return 5; /* 6_0 */
}
static const size_t PM0_Ad_8_rowPtr[] = {
   0,1,1,1,1,3,5
};
static const size_t PM0_Ad_8_colIdx[] = {
   0,4,5,4,5
};
static const float PM0_Ad_8_data[] _ALIGN = {
   1.f,0.999942622f,-0.344226492f,0.000333211245f,0.999248432f
};
static const size_t PM0_Bd0_8_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_8_colIdx[] = {
   0
};
static const float PM0_Bd0_8_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_8_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_8_colIdx[] = {
   0
};
static const float PM0_Bd1_8_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_8_rowPtr[] = {
   0,0,1,2,3,4,5,5,5,6,8,10,10
};
static const size_t PM0_C_0_8_colIdx[] = {
   4,5,5,5,5,4,0,5,0,5
};
static const float PM0_C_0_8_data[] _ALIGN = {
   1.f,-16.8367769f,-0.99f,1.f,-1.99f,1.f,-1.f,16.8367769f,1.f,-16.8367769f
};
static const size_t PM0_D_0_8_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_8_colIdx[] = {
   0
};
static const float PM0_D_0_8_data[] _ALIGN = {
   1.f
};
static void PM0_collision_8()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   x[1] = 0.;
   x[2] = 0.;
   x[3] = 0.;
}
static size_t PM0_natPreComm_8_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[5] >= 0)
   {
      if (-x[4] >= 0)
      {
         return 0; /* 0_0 */
      }
   }
   else
   {
      if (-x[4] >= 0)
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
   if (-x[5] > 0)
   {
      if (x[4] > 0)
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
         if (1.f*x[0]+784.074251f*x[5] >= 0)
         {
            return 8; /* 10_0 */
         }
         else
         {
            return 11; /* 14_0 */
         }
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
         {
            return 7; /* 9_0 */
         }
         else
         {
            return 10; /* 13_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 8_0";
   return 6; /* 8_0 */
}
static const size_t PM0_Ad_9_rowPtr[] = {
   0,4,8,12,12,16,20
};
static const size_t PM0_Ad_9_colIdx[] = {
   0,2,4,5,0,2,4,5,0,2,4,5,0,2,4,5,0,2,4,5
};
static const float PM0_Ad_9_data[] _ALIGN = {
   0.964918508f,13.7260883f,6.57730768e-05f,0.590516554f,-0.00502177766f,
   0.964918508f,1.41723973e-05f,0.0845193933f,-0.00502177766f,0.964918508f,
   1.41723973e-05f,0.0845193933f,0.0845489191f,0.590653581f,0.999704007f,
   -1.76723321f,1.41723973e-05f,6.57730768e-05f,0.000333184672f,0.999009872f
};
static const size_t PM0_Bd0_9_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd0_9_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd0_9_data[] _ALIGN = {
   0.0233598508f,0.00249591025f,0.00249591025f,-0.0420218612f,-9.43673577e-06f
};
static const size_t PM0_Bd1_9_rowPtr[] = {
   0,1,2,3,3,4,5
};
static const size_t PM0_Bd1_9_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_Bd1_9_data[] _ALIGN = {
   0.011721641f,0.00252586741f,0.00252586741f,-0.0425270579f,-4.73566153e-06f
};
static const size_t PM0_C_0_9_rowPtr[] = {
   0,0,1,3,5,6,8,8,9,10,10,10,12
};
static const size_t PM0_C_0_9_colIdx[] = {
   4,0,5,0,5,5,0,5,2,4,0,5
};
static const float PM0_C_0_9_data[] _ALIGN = {
   1.f,-0.0852851293f,-15.4008502f,-0.00248467049f,-0.948166157f,1.f,
   -0.00248467049f,-1.94816616f,1.f,1.f,-0.914714871f,15.4008502f
};
static const size_t PM0_D_0_9_rowPtr[] = {
   0,0,0,1,2,2,3,3,3,3,3,4,5
};
static const size_t PM0_D_0_9_colIdx[] = {
   0,0,0,0,0
};
static const float PM0_D_0_9_data[] _ALIGN = {
   0.0852851293f,0.00248467049f,0.00248467049f,1.f,0.914714871f
};
static void PM0_collision_9()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[3];
   tmpX[2] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[3];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[3] = 0.;
}
static size_t PM0_natPreComm_9_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
   {
      if (-x[4] >= 0)
      {
         return 1; /* 1_0 */
      }
   }
   else
   {
      if (-x[4] >= 0)
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
   if (-x[0]-784.074251f*x[5]+u[0] > 0)
   {
      if (x[4] > 0)
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
         if (1.f*x[0]+784.074251f*x[5] >= 0)
         {
            return 8; /* 10_0 */
         }
         else
         {
            return 11; /* 14_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 9_0";
   return 7; /* 9_0 */
}
static const size_t PM0_Ad_10_rowPtr[] = {
   0,4,8,12,12,16,20
};
static const size_t PM0_Ad_10_colIdx[] = {
   0,2,4,5,0,2,4,5,0,2,4,5,0,2,4,5,0,2,4,5
};
static const float PM0_Ad_10_data[] _ALIGN = {
   0.964918508f,13.7260883f,6.57730768e-05f,0.590516554f,-0.00502177766f,
   0.964918508f,1.41723973e-05f,0.0845193933f,-0.00502177766f,0.964918508f,
   1.41723973e-05f,0.0845193933f,0.0845489191f,0.590653581f,0.999704007f,
   -1.76723321f,1.41723973e-05f,6.57730768e-05f,0.000333184672f,0.999009872f
};
static const size_t PM0_Bd0_10_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_10_colIdx[] = {
   0
};
static const float PM0_Bd0_10_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_10_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_10_colIdx[] = {
   0
};
static const float PM0_Bd1_10_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_10_rowPtr[] = {
   0,0,1,3,5,6,8,8,9,10,10,10,12
};
static const size_t PM0_C_0_10_colIdx[] = {
   4,0,5,0,5,5,0,5,2,4,0,5
};
static const float PM0_C_0_10_data[] _ALIGN = {
   1.f,-0.0852851293f,-15.4008502f,-0.00248467049f,-0.948166157f,1.f,
   -0.00248467049f,-1.94816616f,1.f,1.f,-0.914714871f,15.4008502f
};
static const size_t PM0_D_0_10_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_10_colIdx[] = {
   0
};
static const float PM0_D_0_10_data[] _ALIGN = {
   1.f
};
static void PM0_collision_10()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[3];
   tmpX[2] = 0.914714871f*x[1]+0.0852851293f*x[2]+0.00248467049f*x[3];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
   x[3] = 0.;
}
static size_t PM0_natPreComm_10_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (1.f*x[0]+784.074251f*x[5] >= 0)
   {
      if (-x[4] >= 0)
      {
         return 2; /* 2_0 */
      }
   }
   else
   {
      if (-x[4] >= 0)
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
   if (-x[0]-784.074251f*x[5] > 0)
   {
      if (x[4] > 0)
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
         if (1.f*x[0]+784.074251f*x[5]-1.f*u[0] >= 0)
         {
            return 7; /* 9_0 */
         }
         else
         {
            return 10; /* 13_0 */
         }
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 10_0";
   return 8; /* 10_0 */
}
static const size_t PM0_Ad_12_rowPtr[] = {
   0,1,1,1,4,7,10
};
static const size_t PM0_Ad_12_colIdx[] = {
   0,3,4,5,3,4,5,3,4,5
};
static const float PM0_Ad_12_data[] _ALIGN = {
   1.f,0.994273085f,0.00572691475f,34.2917504f,0.00572691475f,0.994273085f,
   -34.2917504f,-0.000331944144f,0.000331944144f,0.98785462f
};
static const size_t PM0_Bd0_12_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_12_colIdx[] = {
   0
};
static const float PM0_Bd0_12_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_12_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_12_colIdx[] = {
   0
};
static const float PM0_Bd1_12_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_12_rowPtr[] = {
   0,1,2,2,3,4,4,4,4,6,7,8,8
};
static const size_t PM0_C_0_12_colIdx[] = {
   3,4,5,5,3,4,0,0
};
static const float PM0_C_0_12_data[] _ALIGN = {
   -1.f,1.f,1.f,1.f,-1.f,1.f,-1.f,1.f
};
static const size_t PM0_D_0_12_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_12_colIdx[] = {
   0
};
static const float PM0_D_0_12_data[] _ALIGN = {
   1.f
};
static void PM0_collision_12()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   x[1] = 0.;
   x[2] = 0.;
}
static size_t PM0_natPreComm_12_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (x[4] > 0)
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
      if (-x[4] >= 0)
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
         return 11; /* 14_0 */
      }
   }
   else
   {
      if (!Subsystem_PM0_gateSignalBuffer[1])
      {
         return 10; /* 13_0 */
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 12_0";
   return 9; /* 12_0 */
}
static const size_t PM0_Ad_13_rowPtr[] = {
   0,2,4,6,11,16,21
};
static const size_t PM0_Ad_13_colIdx[] = {
   0,2,0,2,0,2,0,2,3,4,5,0,2,3,4,5,0,2,3,4,5
};
static const float PM0_Ad_13_data[] _ALIGN = {
   0.964168282f,13.722601f,-0.00512872306f,0.964168282f,-0.00512872306f,
   0.964168282f,0.0433925456f,0.303161126f,0.994273085f,0.00572691475f,
   34.2917504f,0.0433925456f,0.303161126f,0.00572691475f,0.994273085f,
   -34.2917504f,4.67071562e-38f,7.473145e-37f,-0.000331944144f,
   0.000331944144f,0.98785462f
};
static const size_t PM0_Bd0_13_rowPtr[] = {
   0,1,2,3,4,5,6
};
static const size_t PM0_Bd0_13_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd0_13_data[] _ALIGN = {
   0.0238589912f,0.00254883937f,0.00254883937f,-0.0215649446f,-0.0215649446f,
   -9.34143124e-38f
};
static const size_t PM0_Bd1_13_rowPtr[] = {
   0,1,2,3,4,5,6
};
static const size_t PM0_Bd1_13_colIdx[] = {
   0,0,0,0,0,0
};
static const float PM0_Bd1_13_data[] _ALIGN = {
   0.0119727268f,0.0025798837f,0.0025798837f,-0.0218276011f,-0.0218276011f,
   -4.67071562e-38f
};
static const size_t PM0_C_0_13_rowPtr[] = {
   0,1,2,3,4,5,5,5,6,8,8,8,9
};
static const size_t PM0_C_0_13_colIdx[] = {
   3,4,0,5,5,2,3,4,0
};
static const float PM0_C_0_13_data[] _ALIGN = {
   -1.f,1.f,-0.065643048f,1.f,1.f,1.f,-1.f,1.f,-0.934356952f
};
static const size_t PM0_D_0_13_rowPtr[] = {
   0,0,0,1,1,1,1,1,1,1,1,2,3
};
static const size_t PM0_D_0_13_colIdx[] = {
   0,0,0
};
static const float PM0_D_0_13_data[] _ALIGN = {
   0.065643048f,1.f,0.934356952f
};
static void PM0_collision_13()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.934356952f*x[1]+0.065643048f*x[2];
   tmpX[2] = 0.934356952f*x[1]+0.065643048f*x[2];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
}
static size_t PM0_natPreComm_13_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (x[4] > 0)
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
      if (-x[4] >= 0)
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
         return 11; /* 14_0 */
      }
   }
   Subsystem_errorStatus =
      "Illegal transition conditions in forced commutation for topology 13_0";
   return 10; /* 13_0 */
}
static const size_t PM0_Ad_14_rowPtr[] = {
   0,2,4,6,11,16,21
};
static const size_t PM0_Ad_14_colIdx[] = {
   0,2,0,2,0,2,0,2,3,4,5,0,2,3,4,5,0,2,3,4,5
};
static const float PM0_Ad_14_data[] _ALIGN = {
   0.964168282f,13.722601f,-0.00512872306f,0.964168282f,-0.00512872306f,
   0.964168282f,0.0433925456f,0.303161126f,0.994273085f,0.00572691475f,
   34.2917504f,0.0433925456f,0.303161126f,0.00572691475f,0.994273085f,
   -34.2917504f,4.67071562e-38f,7.473145e-37f,-0.000331944144f,
   0.000331944144f,0.98785462f
};
static const size_t PM0_Bd0_14_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd0_14_colIdx[] = {
   0
};
static const float PM0_Bd0_14_data[] _ALIGN = {
   0
};
static const size_t PM0_Bd1_14_rowPtr[] = {
   0,0,0,0,0,0,0
};
static const size_t PM0_Bd1_14_colIdx[] = {
   0
};
static const float PM0_Bd1_14_data[] _ALIGN = {
   0
};
static const size_t PM0_C_0_14_rowPtr[] = {
   0,1,2,3,4,5,5,5,6,8,8,8,9
};
static const size_t PM0_C_0_14_colIdx[] = {
   3,4,0,5,5,2,3,4,0
};
static const float PM0_C_0_14_data[] _ALIGN = {
   -1.f,1.f,-0.065643048f,1.f,1.f,1.f,-1.f,1.f,-0.934356952f
};
static const size_t PM0_D_0_14_rowPtr[] = {
   0,0,0,0,0,0,0,0,0,0,1,1,1
};
static const size_t PM0_D_0_14_colIdx[] = {
   0
};
static const float PM0_D_0_14_data[] _ALIGN = {
   1.f
};
static void PM0_collision_14()
{
   float * _RESTRICT x = Subsystem_PM0_x;
   float * _RESTRICT tmpX = Subsystem_PM0_tmpX;
   tmpX[1] = 0.934356952f*x[1]+0.065643048f*x[2];
   tmpX[2] = 0.934356952f*x[1]+0.065643048f*x[2];
   x[1] = tmpX[1];
   x[2] = tmpX[2];
}
static size_t PM0_natPreComm_14_0()
{
   const float * const x = Subsystem_PM0_x;
   const float * const u = Subsystem_PM0_u;
   if (x[3] >= 0)
   {
      if (x[4] > 0)
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
      if (-x[4] >= 0)
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
         return 10; /* 13_0 */
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
      1,2,3,4,5,6,7,9,10,11,12,13
   };
   float y[12] _ALIGN;
   size_t i;
   for (i = 0; i < 12; ++i)
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
   for (i = 0; i < 12; ++i)
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
   "1e06750d2cc48ac96bf7b8cf361d881552fa1ed1";
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
   if (Subsystem_U.Sw1 < 0.f || Subsystem_U.Sw1 > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type'";
   }
   else
   {
      Subsystem_B.DataType = (bool)Subsystem_U.Sw1;
   }
   /* Data Type : 'Subsystem/Data Type1' */
   if (Subsystem_U.Sw2 < 0.f || Subsystem_U.Sw2 > 1.f)
   {
      Subsystem_errorStatus = "Data type overflow in 'Subsystem/Data Type1'";
   }
   else
   {
      Subsystem_B.DataType1 = (bool)Subsystem_U.Sw2;
   }


   /* Electrical model */


   /* Electrical model input */
   /* Voltage Source DC : 'Subsystem/Vin' */
   Subsystem_PM0_u[0]=1000.f;
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
   Subsystem_PM0_y[0] = 1.f*Subsystem_PM0_x[5];
   Subsystem_PM0_y[8] = 1.f*Subsystem_PM0_x[0];
   /* End of electrical model output */

   /* End of electrical model */


   /* Global output signals */
   Subsystem_Y.Vc = Subsystem_PM0_y[0];
   Subsystem_Y.AMIO = Subsystem_PM0_y[10];
   Subsystem_Y.VSwitch1 = Subsystem_PM0_y[11];
   Subsystem_Y.VSwitch2 = Subsystem_PM0_y[12];
   Subsystem_Y.VL1 = Subsystem_PM0_y[13];
   Subsystem_Y.VC1 = Subsystem_PM0_y[8];
   Subsystem_Y.VP = Subsystem_PM0_y[3];
   Subsystem_Y.VS1 = Subsystem_PM0_y[4];
   Subsystem_Y.VS2 = Subsystem_PM0_y[5];
   Subsystem_Y.VD1 = Subsystem_PM0_y[6];
   Subsystem_Y.VD2 = Subsystem_PM0_y[7];
   Subsystem_Y.AMD1 = Subsystem_PM0_y[1];
   Subsystem_Y.AMD2 = Subsystem_PM0_y[2];
   Subsystem_Y.AML1 = Subsystem_PM0_y[9];

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
