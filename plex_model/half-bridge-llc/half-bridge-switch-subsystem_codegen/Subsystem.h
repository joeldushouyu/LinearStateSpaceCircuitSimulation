/*
 * Header file for: half-bridge-switch-subsystem/Subsystem
 * Generated with : PLECS 4.9.2
 * Generated on   : 8 Apr 2025 10:50:31
 */
#ifndef PLECS_HEADER_Subsystem_h_
#define PLECS_HEADER_Subsystem_h_

#include <stdbool.h>
#include <stdint.h>

/* Model floating point type */
typedef float Subsystem_FloatType;

/* Model checksum */
extern const char * const Subsystem_checksum;

/* Model error status */
extern const char * Subsystem_errorStatus;


/* Model sample time */
extern const float Subsystem_sampleTime;


/*
 * Model states */
typedef struct
{
   float Subsystem_PM0_x[6];        /* Subsystem */
   bool Subsystem_i1_PM0_s[4];      /* Subsystem */
} Subsystem_ModelStates;
extern Subsystem_ModelStates Subsystem_X;


/* External inputs */
typedef struct
{
   float Sw1;                       /* Subsystem/Sw1 */
   float Sw2;                       /* Subsystem/Sw2 */
} Subsystem_ExternalInputs;
extern Subsystem_ExternalInputs Subsystem_U;


/* External outputs */
typedef struct
{
   float Vc;                        /* Subsystem/Vc */
   float AMIO;                      /* Subsystem/AMIO */
   float VSwitch1;                  /* Subsystem/VSwitch1 */
   float VSwitch2;                  /* Subsystem/VSwitch2 */
   float VL1;                       /* Subsystem/V L1 */
   float VC1;                       /* Subsystem/V C1 */
   float VP;                        /* Subsystem/V p */
   float VS1;                       /* Subsystem/V s1 */
   float VS2;                       /* Subsystem/V s2 */
   float VD1;                       /* Subsystem/V D1 */
   float VD2;                       /* Subsystem/V D2 */
   float AMD1;                      /* Subsystem/AM D1 */
   float AMD2;                      /* Subsystem/AM D2 */
   float AML1;                      /* Subsystem/AM L1 */
} Subsystem_ExternalOutputs;
extern Subsystem_ExternalOutputs Subsystem_Y;


/* Block outputs */
typedef struct
{
   bool DataType;                   /* Subsystem/Data Type */
   bool DataType1;                  /* Subsystem/Data Type1 */
} Subsystem_BlockOutputs;
extern Subsystem_BlockOutputs Subsystem_B;

/* Entry point functions */
void Subsystem_initialize(float time);
void Subsystem_output(void);
void Subsystem_update(void);
void Subsystem_terminate(void);

#endif /* PLECS_HEADER_Subsystem_h_ */
